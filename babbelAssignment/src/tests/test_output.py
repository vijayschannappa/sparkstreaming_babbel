import pytest
import sys, os
import datetime
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, DateType
from chispa.dataframe_comparer import assert_df_equality

parentdir = os.path.dirname(__file__)
parent = os.path.dirname(parentdir)
sys.path.append(parent)
from etl import convert_and_filter_columns
# from src.etl import convert_and_filter_columns

@pytest.fixture(scope="session")
def sample_event_data(spark):
    input_schema = StructType([
        StructField("UserUUID", StringType(), False),
        StructField("start",TimestampType(), False),
        StructField("end", TimestampType(), False),
        StructField("count", IntegerType(),False)
    ])

    input_data = [("83e6fef6c0ff4f8b919fdacdb1b70cfb",datetime.datetime.strptime("2021-04-08 05:30:00","%Y-%m-%d %H:%M:%S"),datetime.datetime.strptime("2021-04-09 05:30:00","%Y-%m-%d %H:%M:%S"),1),
                    ("650fc9cb143c46549f54c3419765bc81",datetime.datetime.strptime("2021-04-09 05:30:00","%Y-%m-%d %H:%M:%S"),datetime.datetime.strptime("2021-04-10 05:30:00","%Y-%m-%d %H:%M:%S"),2),
                    ("83e6fef6c0ff4f8b919fdacdb1b70cfb",datetime.datetime.strptime("2021-04-09 05:30:00","%Y-%m-%d %H:%M:%S"),datetime.datetime.strptime("2021-04-10 05:30:00","%Y-%m-%d %H:%M:%S"),1),
                    ("83e6fef6c0ff4f8b919fdacdb1b70cfb",datetime.datetime.strptime("2021-04-10 05:30:00","%Y-%m-%d %H:%M:%S"),datetime.datetime.strptime("2021-04-11 05:30:00","%Y-%m-%d %H:%M:%S"),1)
                 ]
    
   
    df = spark.createDataFrame(data = input_data ,schema=input_schema)
    return df

def test_output(spark, sample_event_data):
    expected_schema =  StructType([
        StructField("UserUUID", StringType(), False),
        StructField("CreatedDate",DateType(), False),
        StructField("count", IntegerType(),False)
    ])

    expected_data = [("83e6fef6c0ff4f8b919fdacdb1b70cfb",datetime.datetime.strptime("2021-04-08","%Y-%m-%d"),1),
                    ("650fc9cb143c46549f54c3419765bc81",datetime.datetime.strptime("2021-04-09","%Y-%m-%d"),2),
                    ("83e6fef6c0ff4f8b919fdacdb1b70cfb",datetime.datetime.strptime("2021-04-09","%Y-%m-%d"),1),
                    ("83e6fef6c0ff4f8b919fdacdb1b70cfb",datetime.datetime.strptime("2021-04-10","%Y-%m-%d"),1)
                 ]
    expected_result = spark.createDataFrame(data = expected_data ,schema=expected_schema)
    result = convert_and_filter_columns(sample_event_data)
    assert_df_equality(result, expected_result)