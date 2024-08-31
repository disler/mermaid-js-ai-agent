import base64
from typing import Optional
import requests
from PIL import Image, UnidentifiedImageError
import io
from mermaid_agent.modules.utils import build_file_path


def build_image(graph, filename):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")

    width = 500
    height = 500
    scale = 2
    theme = "dark"  # Options: "default", "neutral", "dark", "forest", "base"

    url = (
        "https://mermaid.ink/img/"
        + base64_string
        + f"?width={width}&height={height}&scale={scale}&theme={theme}&bgColor=2a303c"
    )

    response = requests.get(url)
    try:
        return Image.open(io.BytesIO(response.content))
    except UnidentifiedImageError:
        print(
            f"Error: Unable to identify the image. The Mermaid diagram might be invalid. '{filename}'"
        )
        return None


def save_image_locally(img, filename):
    img.save(filename)


def show_image(img):
    if img:
        img.show()
    else:
        print("Error: No image to display")


def mm(graph, filename) -> Optional[Image.Image]:
    img = build_image(graph, filename)
    if img:
        output_path = build_file_path(filename)
        save_image_locally(img, output_path)
        return img
    else:
        return None
