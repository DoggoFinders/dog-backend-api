import os

import logging
import requests
from flask import current_app


def _get_inference_url():
    api_root = current_app.config.get('INFERENCE_API')
    print(api_root)
    return f"{api_root}/api/infer"


def send_dog_image(image_bytes):
    return requests.post(
        _get_inference_url(),
        files=({"image": image_bytes}),
    )
