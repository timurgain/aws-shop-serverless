
# Serverless AWS backend for a shop

## Description
Serverless microservice backend for a shop. Study project at EPAM RS School to learn AWS Cloud Development.  

[CloudFront Frontend](https://d2lgf1k5v7ufib.cloudfront.net)

## Architecture & Technologies
The backend is built using the following AWS services:
- AWS API Gateway
- AWS Lambda
- AWS DynamoDB
- AWS S3 Bucket
- AWS CDK
- Python
- unittest
- ...

## API Documentation
Use [Swagger Web](https://editor.swagger.io) to view the API documentation. Copy the content of the file `openapi.yaml` and paste it into the editor.

## Run and Deploy on AWS

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## CDK commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
