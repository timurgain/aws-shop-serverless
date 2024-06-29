import os
import json
import http
import boto3
from utils.constants import headers_safe_methods
from utils.logging import log_request
from utils.errors import BadRequestError

def lambda_handler(event, context):
    """Import products file Lambda function handler."""
    log_request(event)

    try:
        # 1. Read request queryStringParameters

        query_params = event.get("queryStringParameters", {})
        file_name = query_params.get("name", None)
        if not file_name:
            raise BadRequestError("Invalid request query parameters: name is required")

        # 2. Generate a presigned URL for the S3 bucket

        s3_client = boto3.client("s3")
        bucket_name = os.environ.get("BUCKET_NAME")
        object_key = f"uploaded/{file_name}"
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600,  # seconds
        )

        # 3. Return the presigned URL

        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.OK,
            "body": json.dumps(presigned_url),
        }

    except BadRequestError as err:
        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.BAD_REQUEST,
            "body": json.dumps({"error": str(err)}),
        }
    
    except Exception as err:
        return {
            "headers": headers_safe_methods,
            "statusCode": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({"error": str(err)}),
        }
