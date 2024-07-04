import unittest
from unittest.mock import patch, MagicMock
import json

from import_service.import_service.lambda_functions.import_products_file import lambda_handler


class TestImportProductsFile(unittest.TestCase):

    @patch("lambda_function.boto3.client")
    @patch("lambda_function.os.environ.get")
    def test_lambda_handler_success(self, mock_get_env, mock_boto3_client):
        """Should return status code 200"""
        mock_presigned_url = "https://example.com/presigned-url"
        mock_get_env.return_value = "test-bucket"
        mock_s3_client = MagicMock()
        mock_boto3_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.return_value = mock_presigned_url

        event = {
            "queryStringParameters": {
                "name": "testfile.csv"
            }
        }
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), mock_presigned_url)


    def test_lambda_handler_missing_name(self):
        """Should return status code 400 if name is missing"""
        event = {
            "queryStringParameters": {}
        }
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Invalid request query parameters: name is required", json.loads(response["body"])["error"])


    @patch("lambda_function.boto3.client")
    @patch("lambda_function.os.environ.get")
    def test_lambda_handler_internal_server_error(self, mock_get_env, mock_boto3_client):
        """Should return status code 500 if an exception is raised"""

        mock_get_env.return_value = "test-bucket"
        mock_boto3_client.side_effect = Exception("Something went wrong")

        event = {
            "queryStringParameters": {
                "name": "testfile.csv"
            }
        }
        context = {}

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Something went wrong", json.loads(response["body"])["error"])
