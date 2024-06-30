import boto3
from faker import Faker
from faker_vehicle import VehicleProvider
import uuid

def item_exists(table, key):
    """Check if an item with the specific key already exists in the DynamoDB."""
    response = table.get_item(Key=key)
    return 'Item' in response

def populate_dynamodb():
    """Pre-populate DynamoDB Tables: products and stocks."""

    # 0. Init

    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    products_table = dynamodb.Table('Shop-DynamoDB-products606FDFD3-121663T88JT6V')
    stocks_table = dynamodb.Table('Shop-DynamoDB-stocks999A5704-1Q9SRX76SVUH')
    fake = Faker()
    fake.add_provider(VehicleProvider)

    # 1. Generate mock data

    products = [
        {
            'id': str(uuid.uuid4()),
            'title': fake.vehicle_make_model(),
            'description': f"{fake.machine_category()}, {fake.machine_year()}",
            'price': fake.random_int(min=10, max=500)
        }
        for _ in range(10)
    ]

    stocks = [
        {
            'product_id': product['id'],
            'count': fake.random_int(min=0, max=100)
        }
        for product in products
    ]

    # 2. Put mock data into tables

    for product in products:
        if not item_exists(products_table, {'id': product['id']}):
            products_table.put_item(Item=product)
        else:
            print(f"Product with id {product['id']} already exists.")

    for stock in stocks:
        if not item_exists(stocks_table, {'product_id': stock['product_id']}):
            stocks_table.put_item(Item=stock)
        else:
            print(f"Stock with product_id {stock['product_id']} already exists.")
    
    print('Done')


if __name__ == "__main__":
    populate_dynamodb()
