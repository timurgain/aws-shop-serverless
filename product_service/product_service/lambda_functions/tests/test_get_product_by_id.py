import unittest
import json

from ..get_product_by_id import lambda_handler as get_product_by_id
from ..mocks.production_list import mock_production_list


class TestGetProductByID(unittest.TestCase):

    def setUp(self) -> None:
        """Set up common test data."""

        self.event_success = {
            "pathParameters": {"product_id": 3},
        }
        self.event_404 = {
            "pathParameters": {"product_id": 50},
        }
        self.event_400 = {
            "pathParameters": {"product_id": "not_a_number"},
        }
        self.context = {}

    def test_get_product_by_id_status_code_200(self):
        """Should return status code 200"""
        response = get_product_by_id(self.event_success, self.context)
        self.assertEqual(response.get("statusCode"), 200)

    def test_get_product_by_id_success_data(self):
        """Should return product data."""
        response = get_product_by_id(self.event_success, self.context)
        response_data = json.loads(response.get('body'))

        expected_data = next((item for item in mock_production_list if item['id'] == 3), None)

        self.assertDictEqual(response_data, expected_data)

    def test_get_product_by_id_status_code_404(self):
        """Should return status code 404 if there is no product with that ID"""
        response = get_product_by_id(self.event_404, self.context)
        self.assertEqual(response.get("statusCode"), 404)

    def test_get_product_by_id_status_code_400(self):
        """Should return status code 400 if wrong ID type"""
        response = get_product_by_id(self.event_400, self.context)
        self.assertEqual(response.get("statusCode"), 400)
