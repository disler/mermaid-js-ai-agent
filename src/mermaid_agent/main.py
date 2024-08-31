from mermaid_agent import mermaid_agent
from mermaid_agent.modules import llm_module
from mermaid_agent.modules import mermaid
from mermaid_agent.modules import chain
from mermaid_agent.modules.typings import (
    OneShotMermaidParams,
    IterateMermaidParams,
    MermaidAgentResponse,
)

import typer
from jinja2 import Template
from PIL import Image

app = typer.Typer()

# Constants for reusable options
PROMPT_OPTION = typer.Option(
    ..., "--prompt", "-p", help="The prompt for generating the Mermaid chart"
)
OUTPUT_FILE_OPTION = typer.Option(
    "mermaid.png", "--output", "-o", help="Output file name for the generated chart"
)
INPUT_FILE_OPTION = typer.Option(
    None, "--input", "-i", help="Input file containing additional content"
)


@app.command()
def mer(
    prompt: str = PROMPT_OPTION,
    output_file: str = OUTPUT_FILE_OPTION,
    input_file: str = INPUT_FILE_OPTION,
):
    params = OneShotMermaidParams(
        prompt=prompt, output_file=output_file, input_file=input_file
    )
    response: MermaidAgentResponse = mermaid_agent.one_shot_mermaid_agent(params)
    if response.img:
        mermaid.show_image(response.img)
    return response


@app.command()
def mer_iter(
    prompt: str = PROMPT_OPTION,
    output_file: str = OUTPUT_FILE_OPTION,
    input_file: str = INPUT_FILE_OPTION,
):
    params = OneShotMermaidParams(
        prompt=prompt, output_file=output_file, input_file=input_file
    )

    if not params.prompt.strip():
        raise Exception("Prompt is required")

    print(f"Prompt: {params.prompt}")
    print(f"Output file: {params.output_file}")
    print(f"Input file: {params.input_file}")

    response: MermaidAgentResponse = mermaid_agent.one_shot_mermaid_agent(params)
    if response.img:
        mermaid.show_image(response.img)
    else:
        raise Exception("Failed to generate Mermaid chart")

    print(f"BUILT one shot mermaid chart: {response}")

    iterate_params = IterateMermaidParams(
        change_prompt="",
        base_prompt=prompt,
        current_mermaid_chart=response.mermaid,
        current_mermaid_img=response.img,
        output_file=output_file,
        input_file=input_file,
    )

    while True:
        user_input = input(
            "Would you like to make any changes? (Enter change request or 'n'/'no'/'e' to exit): "
        )
        if user_input.lower() in ["n", "no", "e"]:
            break

        iterate_params.change_prompt = user_input

        response = mermaid_agent.iterate_mermaid_agent(iterate_params)
        iterate_params.current_mermaid_chart = response.mermaid
        if response.img:
            iterate_params.current_mermaid_img = response.img
            mermaid.show_image(iterate_params.current_mermaid_img)

    return response


def main():
    app()
