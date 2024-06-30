import unittest
import json

from ..get_products_list import lambda_handler as get_products_list
from ..mocks.production_list import mock_production_list


class TestGetProductsList(unittest.TestCase):
    def setUp(self) -> None:
        """Set up common test data."""
        self.event = {}
        self.context = {}
        self.mock_data_length = len(mock_production_list)
        self.response = get_products_list(self.event, self.context)
    
    def test_get_products_list_status_code(self) -> None:
        """
        Should return a response with status code 200.
        """
        status = self.response.get("statusCode")

        self.assertEqual(status, 200)

    def test_get_products_list_body(self) -> None:
        """
        Should return a response with a body containing products data.
        """
        body = json.loads(self.response.get("body"))

        self.assertEqual(body, mock_production_list)
