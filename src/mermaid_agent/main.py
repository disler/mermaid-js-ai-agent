import base64
import requests
from PIL import Image, UnidentifiedImageError
import io
from . import examples as ex


def build_image(graph, filename):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    print("base64_bytes", base64_bytes)
    base64_string = base64_bytes.decode("ascii")
    url = "https://mermaid.ink/img/" + base64_string

    response = requests.get(url)
    try:
        return Image.open(io.BytesIO(response.content))
    except UnidentifiedImageError:
        print(
            f"Error: Unable to identify the image. The Mermaid diagram might be invalid. '{filename}'"
        )
        return None


def save_image_locally(img, filename="mermaid_graph.png"):
    img.save(filename)


def show_image(img):
    if img:
        img.show()
    else:
        print("Error: No image to display")


def mm(graph, filename="mermaid_graph.png"):
    img = build_image(graph, filename)
    if img:
        save_image_locally(img, filename)
        show_image(img)
    else:
        print("Error: Failed to generate Mermaid diagram")


def main():
    mm(ex.graph, "graph.png")
    mm(ex.pie_chart, "pie_chart.png")
    mm(ex.sequence_diagram, "sequence_diagram.png")
    mm(ex.gantt_chart, "gantt_chart.png")
    mm(ex.class_diagram, "class_diagram.png")
