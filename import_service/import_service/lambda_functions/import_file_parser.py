import boto3
import csv
import os

from utils.logging import log_info

s3 = boto3.client("s3")


def lambda_handler(event, context):
    """
    Uses a readable stream to get an object from S3,
    parse it using csv-parser package and log each record to be shown in CloudWatch.
    """
    try:
        # 0. Get the bucket name and file_key from the event

        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"]
        if not file_key.startswith("uploaded/") or not file_key.endswith(".csv"):
            log_info(
                f"File {file_key} is not processed. Expected .csv in the 'uploaded' folder."
            )
            return

        # 1. Read the file row by row

        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        lines = response["Body"].read().decode("utf-8").splitlines()
        reader = csv.reader(lines)

        for row in reader:
            log_info(row)

        # 2. Move the file from 'uploaded' to 'parsed' folder

        new_file_key = file_key.replace("uploaded", "parsed")
        s3.copy_object(
            Bucket=bucket_name,
            CopySource={"Bucket": bucket_name, "Key": file_key},
            Key=new_file_key,
        )
        s3.delete_object(Bucket=bucket_name, Key=file_key)

        log_info(f"File {file_key} was parsed and moved to 'parsed' folder.")
    
    except Exception as err:
        log_info(f"Error parsing file: {str(err)}")
        raise err
    
    # finally:
    #     s3.delete_object(Bucket=bucket_name, Key=file_key)
        
