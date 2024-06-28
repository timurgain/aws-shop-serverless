import json
import http
from utils.constants import headers_mutating_methods
from utils.logging import log_request
from utils.errors import BadRequestError

def lambda_handler(event, context):
    """Import products file Lambda function handler."""
    log_request(event)

    try:
        # 1. Read request body

        try:
            body = json.loads(event.get("body", "{}"))
        except json.JSONDecodeError as e:
            raise BadRequestError(f"Invalid JSON payload: {str(e)}")

        file_url = body.get("file_url")

        if not file_url:
            raise BadRequestError("Invalid request body: file_url is required")

    except BadRequestError as err:
        return {
            "headers": headers_mutating_methods,
            "statusCode": http.HTTPStatus.BAD_REQUEST,
            "body": json.dumps({"error": str(err)}),
        }
    
    except Exception as err:
        return {
            "headers": headers_mutating_methods,
            "statusCode": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({"error": str(err)}),
        }
