import os

import boto3
from PIL import Image, ImageFont, ImageDraw

from src import config

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    aws_access_key_id=config.S3_ACCESS_KEY,
    aws_secret_access_key=config.S3_SECRET_KEY,
)


def upload_image_to_s3(image_name):
    s3.upload_file(
        Filename=image_name,
        Bucket=config.BUCKET_NAME,
        Key=image_name,
    )


# Number of digits to font size
FONT_SIZES = {
    1: 650,
    2: 550,
    3: 450,
    4: 350,
}

BACKGROUND_COLORS = {
    "RED": (196, 85, 77),
    "YELLOW": (194, 147, 67),
    "BLUE": (72, 124, 165),
    "GREEN": (84, 129, 100),
}


def generate_number_image(number, image_name, image_size=(1000, 1000), background_color="RED", text_color="white"):
    text = str(number)

    image = Image.new('RGBA', image_size, (255, 0, 0, 0))

    draw = ImageDraw.Draw(image)
    draw.ellipse((100, 100, image_size[0]-100, image_size[1]-100), fill=BACKGROUND_COLORS[background_color])

    font = ImageFont.truetype(os.path.join("fonts", "arial.ttf"), FONT_SIZES[len(text)])

    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text(((image_size[0] - w) / 2, (image_size[1] - h) / 2), text, font=font, fill=text_color)

    image.save(image_name)

    return image_name


# generate_number_image(1, "1_RED.png")
# generate_number_image(11, "11_RED.png")
# generate_number_image(111, "111_RED.png")
# generate_number_image(1111, "1111_RED.png")


def image_exists(image_name):
    try:
        s3.head_object(Bucket=config.BUCKET_NAME, Key=image_name)
        return True
    finally:
        return False


def get_number_image(number: int, background_color: str):
    image_name = f"image_{number}_{background_color}.png"
    if not image_exists(image_name):
        generate_number_image(number, image_name, background_color=background_color)
        upload_image_to_s3(image_name)

    image_url = f"https://{config.BUCKET_NAME}.s3.amazonaws.com/{image_name}"
    return image_url

