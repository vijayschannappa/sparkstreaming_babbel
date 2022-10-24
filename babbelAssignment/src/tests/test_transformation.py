from ast import Str
import pytest
import os, sys
import datetime
from pyspark.sql.types import StructType, StructField, StringType, IntegerType,TimestampType
from chispa.dataframe_comparer import assert_df_equality
parentdir = os.path.dirname(__file__)
parent = os.path.dirname(parentdir)
print(parent)
sys.path.append(parent)
from etl import get_transformed_df

@pytest.fixture(scope="session")
def sample_event_data(spark):
    input_schema = StructType([
        StructField("EventUUID", StringType(), False),
        StructField("UserUUID", StringType(), False),
        StructField("EventName", StringType(), False),
        StructField("CreatedAt", StringType(), False)
    ])

    input_data = [("d73d8691c6ba47f2b95466ad36d3b3ea","83e6fef6c0ff4f8b919fdacdb1b70cfb","LessonStarted","2021-04-08T22:15:55.992605+02:00"),
                  ("acb73ae754ad4fc4a5c8099f8332b7e3","83e6fef6c0ff4f8b919fdacdb1b70cfb","LessonStarted","2021-04-09T06:16:55.992666+00:00"),
                  ("d73d8691c6ba47f2b95466ad36d3b3ea","83e6fef6c0ff4f8b919fdacdb1b70cfb","LessonStarted","2021-04-08T22:15:55.992605+02:00")]
    
    df = spark.createDataFrame(data = input_data ,schema=input_schema)
    return df

def test_transformation(spark, sample_event_data):
    expected_schema =  StructType([
        StructField("EventUUID", StringType(), False),
        StructField("UserUUID", StringType(), False),
        StructField("EventName", StringType(), False),
        StructField("CreatedAt", StringType(), False),
        StructField("ts",TimestampType(),False),
        StructField("ts_utc",TimestampType(),False)
    ])

    expected_data = [
        ("d73d8691c6ba47f2b95466ad36d3b3ea","83e6fef6c0ff4f8b919fdacdb1b70cfb","LessonStarted","2021-04-08T22:15:55.992605+02:00",datetime.datetime.strptime("2021-04-09 01:45:55.992605","%Y-%m-%d %H:%M:%S.%f"),datetime.datetime.strptime("2021-04-08 20:15:55.992605","%Y-%m-%d %H:%M:%S.%f")),
        ("acb73ae754ad4fc4a5c8099f8332b7e3","83e6fef6c0ff4f8b919fdacdb1b70cfb","LessonStarted","2021-04-09T06:16:55.992666+00:00",datetime.datetime.strptime("2021-04-09 11:46:55.992666","%Y-%m-%d %H:%M:%S.%f"),datetime.datetime.strptime("2021-04-09 06:16:55.992666","%Y-%m-%d %H:%M:%S.%f")),
        ("d73d8691c6ba47f2b95466ad36d3b3ea","83e6fef6c0ff4f8b919fdacdb1b70cfb","LessonStarted","2021-04-08T22:15:55.992605+02:00",datetime.datetime.strptime("2021-04-09 01:45:55.992605","%Y-%m-%d %H:%M:%S.%f"),datetime.datetime.strptime("2021-04-08 20:15:55.992605","%Y-%m-%d %H:%M:%S.%f"))]
       
    expected_result = spark.createDataFrame(data = expected_data ,schema=expected_schema)
    result = get_transformed_df(sample_event_data)
    assert_df_equality(result, expected_result)

