from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_s3objectlambda,
    aws_lambda,
    aws_s3,
    aws_iam,
)
from constructs import Construct

from .code_from_asset2 import include_requirements


class AwsLambdaObjectDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creates Transform Lambda
        self.aws_lambda = aws_lambda.Function(
            self,
            "S3ObjectTransformLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_9,  # type: ignore
            # architecture=aws_lambda.Architecture.ARM_64,  # type: ignore
            memory_size=256,  # Checkout https://github.com/alexcasalboni/aws-lambda-power-tuning
            handler="lambda_handler.lambda_handler",
            code=include_requirements("src/add_watermarks/", "add_watermarks"),
            timeout=Duration.seconds(30),  # Lambda Object must complete within 30 seconds.
        )
        self.aws_lambda.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["s3-object-lambda:WriteGetObjectResponse"],
            effect=aws_iam.Effect.ALLOW,
            resources=["*"]
        ))

        # Create S3 Bucket
        self.s3_bucket = aws_s3.Bucket(
            self,
            "S3ObjectLambdaDemoBucket",
        )
        self.s3_bucket.grant_read(self.aws_lambda)

        self.s3_bucket_ap = aws_s3.CfnAccessPoint(
            self,
            "S3ObjectLambdaBucketAP",
            bucket=self.s3_bucket.bucket_name,
        )

        # Creates AWS S3 Lambda Object Access Point
        ObjectLambdaConfigurationProperty = aws_s3objectlambda.CfnAccessPoint.\
            ObjectLambdaConfigurationProperty
        TransformationConfigurations = aws_s3objectlambda.CfnAccessPoint.\
            TransformationConfigurationProperty

        lo_ap_props = ObjectLambdaConfigurationProperty(
            supporting_access_point=self.s3_bucket_ap.attr_arn,
            transformation_configurations=[
                TransformationConfigurations(
                    actions=["GetObject"],
                    content_transformation={
                        "AwsLambda": {
                            "FunctionArn": self.aws_lambda.function_arn,
                        }
                    }
                )
            ]
        )

        self.lambda_object_ap = aws_s3objectlambda.CfnAccessPoint(
            self,
            "S3LambdaObjectAP",
            object_lambda_configuration=lo_ap_props,
        )

        # Output
        CfnOutput(self, "S3Bucket", value=self.s3_bucket.bucket_arn)
        CfnOutput(self, "S3ObjectAP", value=self.s3_bucket_ap.ref)
