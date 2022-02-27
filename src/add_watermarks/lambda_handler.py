import contextlib
import io
import typing

import boto3
from PIL import Image, ImageFont, ImageDraw
import requests
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging.correlation_paths import S3_OBJECT_LAMBDA
from aws_lambda_powertools.utilities.data_classes.s3_object_event import \
    S3ObjectLambdaEvent

logger = Logger()
session = boto3.Session()
s3_client = boto3.client("s3")


@logger.inject_lambda_context(correlation_id_path=S3_OBJECT_LAMBDA, log_event=True)
def lambda_handler(event, context):
    event = S3ObjectLambdaEvent(event)

    with load_object_image(event) as img:
        draw_watermark(img)
        update_response(event, img)

    return {"status_code": 200}


@contextlib.contextmanager
def load_object_image(event: S3ObjectLambdaEvent):
    """
    Loads the event as a PIL Image

    :param event:
    """
    response = requests.get(event.input_s3_url)
    with Image.open(io.BytesIO(response.content)) as img:
        try:
            yield img
        finally:
            pass


def draw_watermark(img: Image.Image):
    """Add a white "watermark" text on the top left of the image."""
    draw = ImageDraw.ImageDraw(img)
    font = ImageFont.load_default()
    draw.text(
        (0, 0),
        "watermark",
        (128, 128, 128),
        font=font,
    )


def update_response(event: S3ObjectLambdaEvent, img: Image.Image):
    """
    Updates the S3 GetObject Response.

    Saving in /tmp/<filename>.<ext> to let PIL decide the format. Then reload the file.
    """
    filename = f"/tmp/{event.input_s3_url[event.input_s3_url.rfind('/'):]}"
    filename = filename[:filename.find("?")]
    with open(filename, "wb+") as fp:
        img.save(fp)
        fp.seek(0)

        s3_client.write_get_object_response(
            Body=fp.read(),
            RequestRoute=event.request_route,
            RequestToken=event.request_token,
        )
