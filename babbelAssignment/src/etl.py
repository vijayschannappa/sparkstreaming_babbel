from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import from_json, col, to_timestamp, window, expr, sum, to_date,to_utc_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark import SparkConf
from lib.logger import Log4j

def get_transformed_df(event_df):
    event_df = event_df.withColumn("ts", to_timestamp(col("CreatedAt")))
    event_df = event_df.withColumn("ts_utc", to_utc_timestamp(col("ts"),'Asia/Calcutta'))
    event_df.schema['ts'].nullable = False
    event_df.schema['ts_utc'].nullable = False
    return event_df

def extract_values_fromm_stream(kafka_df):
    value_df = kafka_df.select(from_json(col("value").cast("string"), event_schema).alias("value"))
    event_df = value_df.select("value.*")
    return event_df

def convert_and_filter_columns(watermarked_df):
    output_df = watermarked_df
    # output_df = watermarked_df.select("UserUUID", "window.start","window.end", "count")
    output_df = output_df.withColumn('CreatedDate',to_date(col("start")))
    output_df = output_df.select("UserUUID", "CreatedDate", "count")
    return output_df

if __name__ == "__main__":
    conf = SparkConf()
    conf.set("spark.streaming.stopGracefullyOnShutdown", "true")
    conf.set("spark.sql.shuffle.partitions", 2)
    conf.set("spark.jars.packages", 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0') #for Kafka
    # conf.set("spark.jars.packages", "org.apache.spark:spark-streaming-kinesis-asl_2.12:3.3.0") #for kinesis

    spark = SparkSession \
        .builder \
        .appName("babbelAssignment") \
        .master("local[3]") \
        .config(conf=conf)\
        .getOrCreate()

    logger = Log4j(spark)

    event_schema = StructType([
        StructField("EventUUID", StringType(), False),
        StructField("UserUUID", StringType(), False),
        StructField("EventName", StringType(), False),
        StructField("CreatedAt", StringType(), False)
    ])

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "babbel") \
        .option("startingOffsets", "earliest") \
        .load()
    
    event_df = extract_values_fromm_stream(kafka_df)

    event_df = get_transformed_df(event_df)

    watermarked_df = event_df.withWatermark("ts_utc", "7 days").dropDuplicates(['EventUUID'])\
        .groupBy("UserUUID", window(col("ts_utc"), "24 hours")).count()

    water_df = watermarked_df.select("UserUUID", "window.start", "window.end", "count")

    output_df = convert_and_filter_columns(water_df)

    #check output in console
    # output_query = output_df.writeStream.format("console").outputMode("update")\
    #     .option("checkpointLocation", "chk-point-dir")\
    #     .trigger(processingTime="10 second")\
    #     .start()
    output_query = output_df.writeStream \
        .trigger(processingTime="5 seconds") \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="tablename", keyspace="kafkaspark") \
        .mode("update") \
        .start()
    output_query.awaitTermination()
