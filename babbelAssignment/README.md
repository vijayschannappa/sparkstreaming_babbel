# sparkStreaming 
The repository includes the script for streaming kafka data from spark and writing it to cassandra (AWS Keyspaces). Also it comprises Terraform scripts for deploying EMR cluster and AWS Keyspace (AWS managed Apache Cassandra).

<img width="916" alt="image" src="https://user-images.githubusercontent.com/77616210/197401087-57ca206b-40c1-452a-86a8-24e036b75885.png">


# Assumptions
Data stream is published to the Kafka topic - babbel

# Key Requirements
Components used in the architecture should be SCALABLE and FAULT TOLERANT.

# Features of Chosen Components
As shown in the architecture diagram the pipeline requires AWS EMR cluster where we can deploy and run our streaming application, and also an amazon managed Cassandra database which will support update mode in write stream.

Why Spark?
Spark is a highly scalable, configurable and fault tolerant big data processing framework. Additionally structured streaming of spark supports windowing aggregations within specified time period which can be easily configured based on our requirements. In our case time period for state retention is 7 days.
With respect to scalability we can integrate auto-scaling policy of AWS EMR to terraform script through which we can cater to the increasing traffic and also we pay for the resources we use. Spark streaming can also be seamlessly integrated with any Spark components like MLlib. Additionally, Spark is an open source and cloud agnostic framework which can be deployed on the cloud provider of our choice.


Why AWS Keyspace (Cassandra)?
AWS Keyspace can be readily integrated with spark structured streaming and supports update mode which is a requirement in the project. It is also higly scalable as Amazon Keyspaces automatic scaling can increase read capacity or write capacity as often as necessary, in accordance with our scaling policy policy attached to the service in terraform script. Additionally, unlike DynamoDB which is native to AWS, AWS Keyspace is just a managed Cassandra and so it's near to cloud agnostic policy.

# How to run the Project?
If you want to test the project locally, the install kafka and spark in your local system. Please start the Kafka zookeeper and broker. The run the python based producer 'python_producer.py' which produces messages to the mentioned topic - babbel. Then run the spark streaming script and print the outptu in console to see the processed data. the stream trigger frequency and state retention period can be adjusted as per our requirements.





