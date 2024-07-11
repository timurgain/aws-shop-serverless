import os
import json
import unittest
from unittest.mock import patch, MagicMock
from moto import mock_aws
from product_service.product_service.lambda_functions.catalog_batch_process import lambda_handler


class TestLambdaHandler(unittest.TestCase):

    @mock_aws
    @patch.dict(os.environ, {'PRODUCTS_TABLE_NAME': 'test_table'})
    @patch('product_service.product_service.lambda_functions.utils.logging.log_request')
    @patch('product_service.product_service.lambda_functions.utils.logging.log_info')
    @patch('product_service.product_service.lambda_functions.utils.dynamodb.execute_transact_write')
    @patch('product_service.product_service.lambda_functions.utils.dynamodb.prepare_product_stock_data')
    def test_lambda_handler_success(self, mock_log_request, mock_log_info, mock_execute, mock_prepare, mock_publish):
    # Your test code here
        """Should execute the lambda handler successfully."""
        
        # 0. Mocks

        mock_publish.return_value = {'MessageId': 'test_message_id'}
        mock_prepare.return_value = ({}, {})
        mock_execute.return_value = True

        # 1. Test event

        mock_event = {
            "Records": [
                {
                    "body": json.dumps({
                        "title": "Test Product",
                        "description": "Test Description",
                        "price": 100,
                        "count": 10
                    })
                }
            ]
        }
        context = {}

        # 2. Invoke the lambda handler

        lambda_handler(mock_event, context)

        # 3. Assertions

        mock_log_request.assert_called_once()
        mock_prepare.assert_called_once()
        mock_execute.assert_called_once()
        mock_log_info.assert_called()

if __name__ == '__main__':
    unittest.main()