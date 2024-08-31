from mermaid_agent import mermaid_agent
from mermaid_agent.modules import llm_module
from mermaid_agent.modules import mermaid
from mermaid_agent.modules import chain
from mermaid_agent.modules.typings import (
    OneShotMermaidParams,
    IterateMermaidParams,
    MermaidAgentResponse,
    BulkMermaidParams,
    BulkMermaidAgentResponse,
)

import os
import typer
from jinja2 import Template
from PIL import Image
from mermaid_agent.modules.utils import build_file_path, current_date_time_str

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
) -> MermaidAgentResponse:
    """Generates a Mermaid chart in one shot."""
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
) -> MermaidAgentResponse:
    """Generates a Mermaid chart iteratively, allowing for user refinement."""
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

    # Create a directory for this iteration session
    session_dir = build_file_path(f"iter_session_{current_date_time_str()}")
    os.makedirs(session_dir, exist_ok=True)

    # Save the initial chart
    iteration_count = 0
    initial_output_file = os.path.join(
        session_dir, f"iteration_{iteration_count}_{output_file}"
    )
    response.img.save(initial_output_file)

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

            iteration_count += 1
            iteration_output_file = os.path.join(
                session_dir, f"iteration_{iteration_count}_{output_file}"
            )
            response.img.save(iteration_output_file)

    return response


@app.command()
def mer_bulk(
    prompt: str = PROMPT_OPTION,
    output_file: str = OUTPUT_FILE_OPTION,
    input_file: str = INPUT_FILE_OPTION,
    count: int = typer.Option(5, "--count", "-c", help="Number of diagrams to generate"),
) -> BulkMermaidAgentResponse:
    """Generates multiple Mermaid charts in one shot."""
    params = BulkMermaidParams(
        prompt=prompt, output_file=output_file, input_file=input_file, count=count
    )
    response: BulkMermaidAgentResponse = mermaid_agent.bulk_mermaid_agent(params)
    for i, res in enumerate(response.responses):
        if res.img:
            mermaid.show_image(res.img)
            print(f"Generated diagram {i+1}/{count}")
    return response


def main():
    """Entry point for the Mermaid agent CLI."""
    app()
