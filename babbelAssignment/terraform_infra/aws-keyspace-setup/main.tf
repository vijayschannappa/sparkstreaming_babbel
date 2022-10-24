terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    awscc = {
      source  = "hashicorp/awscc"
      version = "~> 0.1.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_kms_key" "terraform" {
  description = "Example key for Cassandra table"
}

provider "awscc" {
  region = "eu-central-1"
}

provider "random" {}

resource "awscc_cassandra_keyspace" "terraform" {
  keyspace_name = "kafkaspark"
}

resource "awscc_cassandra_table" "events" {
  keyspace_name = awscc_cassandra_keyspace.terraform.keyspace_name
  table_name    = "events"

  partition_key_columns = [
    {
      column_name : "UserUUID"
      column_type : "text"
    }
  ]
  regular_columns = [
    {
      column_name : "UserUUID"
      column_type : "text"
    },
    {
      column_name : "CreatedAt"
      column_type : "date"
    },
    {
      column_name : "count"
      column_type : "int"
    }
  ]
  encryption_specification = {
    encryption_type : "AWS_OWNED_KMS_KEY"
    kms_key_identifier : aws_kms_key.terraform.key_id
  }
}