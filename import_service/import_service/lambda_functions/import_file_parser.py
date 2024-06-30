def lambda_handler(event, context):
    """
    Uses a readable stream to get an object from S3,
    parse it using csv-parser package and log each record to be shown in CloudWatch.
    """
    try:
        print("Event triggered by s3:ObjectCreated:* ", event)
    except Exception as err:
        pass