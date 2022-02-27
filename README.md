# AWS Lambda Object demo
![PythonSupported](https://img.shields.io/static/v1?label=Python&message=3.9&color=green&logo=Python)
![AWS-CDK](https://img.shields.io/static/v1?label=CDK&message=2.12.0&color=green&logo=amazonaws)
![AWS-S3-Objects](https://img.shields.io/static/v1?label=S3-Objects&message=%e2%9c%94&color=blue&logo=amazons3)

This repository contains demonstrates a use case for AWS S3 Lambda Objects.

The S3 Object will hold images, and the lambda object will dynamically add watermarks to the item prior delivery.

It uses CDK to deploy the stack.

# Deploy and experiment

After [installing CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

````bash
git clone -v https://github.com/HanaPoulpe/AWSLambdaObject.git
cd AWSLambdaObject
pip install -rrequirements.txt
# First bootstrap you AWS account
cdk boostrap
# Then deploy the stack
cdk deploy
````

# Read more

For more information about S3 Lambda Objects:
* [AWS Lambda Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transforming-objects.html)
* [My blog Article](https://www.hanaburtin.net/) <!--TODO: Complete URL-->
