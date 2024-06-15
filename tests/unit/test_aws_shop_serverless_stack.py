import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_shop_serverless.get_products_list_stack import AwsShopServerlessStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_shop_serverless/aws_shop_serverless_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsShopServerlessStack(app, "aws-shop-serverless")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
