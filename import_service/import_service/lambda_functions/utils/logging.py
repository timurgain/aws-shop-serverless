import json
import logging

logger = logging.getLogger("product_service")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def log_request(event):
    """Log request (Lambda event) data:
    - body
    - path params"""

    try:
        body = json.dumps(event.get("body", {}), indent=2)
        path_params = json.dumps(event.get("pathParameters", {}), indent=2)
        query_params = json.dumps(event.get("queryStringParameters", {}), indent=2)

        logger.info(f"Request body: {body}")
        logger.info(f"Request path params: {path_params}")
        logger.info(f"Request query params: {query_params}")
        
    except Exception as e:
        logger.error(f"Error logging request: {str(e)}")

def log_info(message: str):
    """Log info message"""
    logger.info(message)
