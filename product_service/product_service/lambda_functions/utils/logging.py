import json
import logging

logger_request = logging.getLogger("product_service")
logger_request.setLevel(logging.INFO)
logger_request.addHandler(logging.StreamHandler())


def log_request(event):
    """Log request (Lambda event) data:
    - body
    - path params"""

    try:
        body = json.dumps(event.get("body", {}), indent=2)
        path_params = json.dumps(event.get("pathParameters", {}), indent=2)
        query_params = json.dumps(event.get("queryStringParameters", {}), indent=2)

        logger_request.info(f"Request body: {body}")
        logger_request.info(f"Request path params: {path_params}")
        logger_request.info(f"Request query params: {query_params}")
        
    except Exception as e:
        logger_request.error(f"Error logging request: {str(e)}")
