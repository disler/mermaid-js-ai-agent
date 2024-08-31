import base64
from typing import Optional
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO


def build_image(graph, filename) -> Optional[Image.Image]:
    graphbytes = graph.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    url = "https://mermaidapi.com/api/v1"
    body = {"mermaid": graph, "base64": base64_string}
    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        image_data = response.content
        try:
            img = Image.open(BytesIO(image_data))
            return img
        except UnidentifiedImageError:
            print(f"Error: Could not open image from {filename}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not generate Mermaid diagram: {e}")
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
        save_image_locally(img, filename)
        return img
    else:
        return None
