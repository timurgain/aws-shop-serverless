# import aws_cdk as core
# import aws_cdk.assertions as assertions

# from product_service.get_products_list_stack import AwsShopServerlessStack

# example tests. To run these tests, uncomment this file along with the example
# resource in product_service/product_service_stack.py
# def test_sqs_queue_created():
#     app = core.App()
#     stack = AwsShopServerlessStack(app, "aws-shop-serverless")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
