from typing import Optional
from mermaid_agent.modules import llm_module
from mermaid_agent.modules import mermaid
from mermaid_agent.modules import chain
from mermaid_agent.modules.typings import (
    OneShotMermaidParams,
    ResolutionMermaidParams,
    IterateMermaidParams,
    MermaidAgentResponse,
)
from PIL import Image


def build_model():
    # return llm_module.build_sonnet_3_5()
    return llm_module.build_latest_openai()
    # return llm_module.build_mini_model()


def one_shot_mermaid_agent(params: OneShotMermaidParams) -> MermaidAgentResponse:

    model = build_model()

    base_prompt = params.prompt
    output_file = params.output_file
    input_file = params.input_file

    file_content = ""
    if input_file:
        with open(input_file, "r") as file:
            file_content = file.read()

    mermaid_prompt_1 = """You are a world-class expert at creating mermaid charts.

You follow the instructions perfectly to generate mermaid charts.

<instructions>
    <instruction>Based on the user-prompt, create the corresponding mermaid chart.</instruction>
    <instruction>Be very precise with the chart, every node and edge must be included.</instruction>
    <instruction>Use double quotes for text in the chart</instruction>
    <instruction>Respond with the mermaid chart only.</instruction>
    <instruction>Do not wrap the mermaid chart in markdown code blocks. Respond with the mermaid chart only.</instruction>
    <instruction>If you see a file-content section, use the content to help create the chart.</instruction>
    <instruction>Keep node labels short and concise.</instruction>
    <instruction>Avoid embedding links in the chart.</instruction>
</instructions>

% if file_content:
<file-content>
    ${file_content}
</file-content>
% endif

<examples>
    <example>
        <user-chart-request>
            Create a flowchart that shows A flowing to E. At C, branch out to H and I.
        </user-chart-request>
        <chart-response>
            graph LR;
                A
                B
                C
                D
                E
                H
                I

                A --> B
                A --> C
                A --> D
                C --> H
                C --> I
                D --> E
        </chart-response>
    </example>
    <example>
        <user-chart-request>
            Build a pie chart that shows the distribution of Apples: 40, Bananas: 35, Oranges: 25.
        </user-chart-request>
        <chart-response>
            pie title Distribution of Fruits
                "Apples" : 40
                "Bananas" : 35
                "Oranges" : 25
        </chart-response>
    </example>
    <example>
        <user-chart-request>
            State diagram for a traffic light. Still, Moving, Crash.
        </user-chart-request>
        <chart-response>
            stateDiagram-v2
                [*] --> Still
                Still --> [*]

                Still --> Moving
                Moving --> Still
                Moving --> Crash
                Crash --> [*]
        </chart-response>
    </example>
    <example>
        <user-chart-request>
            Create a timeline of major social media platforms from 2002 to 2006.
        </user-chart-request>
        <chart-response>
            timeline
                title History of Social Media Platforms
                2002 : LinkedIn
                2004 : Facebook
                     : Google
                2005 : Youtube
                2006 : Twitter
        </chart-response>
    </example>
</examples>

<user-prompt>
    {{user_prompt}}
</user-prompt>

Your mermaid chart:"""

    mermaid_prompt_2 = """You are a world-class expert at creating mermaid charts.

Your co-worker has just generated a mermaid chart.

It's your job to review the chart to ensure it's correct.

If you see any mistakes, be very precise in what the mistakes are.

<instructions>
    <instruction>Review the chart to ensure it's correct.</instruction>
    <instruction>Be very precise in your correction.</instruction>
    <instruction>If you see any mistakes, correct them.</instruction>
    <instruction>Respond with the corrected mermaid chart.</instruction>
    <instruction>Do not wrap the mermaid chart in markdown code blocks. Respond with the mermaid chart only.</instruction>
    <instruction>If the chart is already correct, respond with the chart only.</instruction>
</instructions>

<mermaid-chart>
    {{output[-1]}}
</mermaid-chart>

Your correction of the mermaid chart if needed:"""

    context = {"user_prompt": base_prompt, "file_content": file_content}

    # Render the template with the context
    rendered_mermaid_prompt_1 = llm_module.conditional_render(
        mermaid_prompt_1, {"file_content": file_content}
    )

    chain.MinimalChainable.to_delim_text_file(
        "rendered_mermaid_prompt_1", [rendered_mermaid_prompt_1]
    )

    print("context", context.get("user_prompt"))

    prompt_response, ctx_filled_prompts = chain.MinimalChainable.run(
        context,
        model,
        llm_module.prompt,
        prompts=[rendered_mermaid_prompt_1, mermaid_prompt_2],
    )

    chain.MinimalChainable.to_delim_text_file(
        "mermaid_prompt_1_results", prompt_response
    )

    chain.MinimalChainable.to_delim_text_file(
        "mermaid_prompt_1_ctx_filled_prompts", ctx_filled_prompts
    )

    res = llm_module.parse_markdown_backticks(prompt_response[-1])

    img = mermaid.mm(res, output_file)

    for _ in range(2):
        if img is None:
            print("Failed to generate image - running resolution agent")

            resolution_params = ResolutionMermaidParams(
                error="Error: Failed to generate Mermaid diagram",
                damaged_mermaid_chart=res,
                base_prompt=base_prompt,
                output_file=output_file,
                input_file=input_file,
            )

            resolution_response = resolution_mermaid_agent(resolution_params)
            img = resolution_response.img
        else:
            break

    return MermaidAgentResponse(img=img, mermaid=res)


def resolution_mermaid_agent(params: ResolutionMermaidParams) -> MermaidAgentResponse:
    model = build_model()

    error = params.error
    damaged_mermaid_chart = params.damaged_mermaid_chart
    prompt = params.base_prompt
    output_file = params.output_file
    input_file = params.input_file

    file_content = ""
    if input_file:
        with open(input_file, "r") as file:
            file_content = file.read()

    correction_prompt = """You are a world-class expert at creating and fixing mermaid charts.

You have been given a damaged mermaid chart and an error message. Your task is to fix the chart.

<instructions>
    <instruction>Analyze the error message and the damaged mermaid chart.</instruction>
    <instruction>Identify the issue causing the error.</instruction>
    <instruction>Fix the mermaid chart to resolve the error.</instruction>
    <instruction>Ensure the fixed chart still fulfills the original prompt.</instruction>
    <instruction>Respond with the corrected mermaid chart only.</instruction>
    <instruction>Do not wrap the mermaid chart in markdown code blocks.</instruction>
</instructions>

<error-message>
{{error}}
</error-message>

<damaged-mermaid-chart>
{{damaged_mermaid_chart}}
</damaged-mermaid-chart>

<original-prompt>
{{prompt}}
</original-prompt>

% if file_content:
<file-content>
${file_content}
</file-content>
% endif

Your corrected mermaid chart:"""

    context = {
        "error": error,
        "damaged_mermaid_chart": damaged_mermaid_chart,
        "prompt": prompt,
        "file_content": file_content,
    }

    # Render the template with the context
    rendered_correction_prompt = llm_module.conditional_render(
        correction_prompt, {"file_content": file_content}
    )

    prompt_response, ctx_filled_prompts = chain.MinimalChainable.run(
        context, model, llm_module.prompt, prompts=[rendered_correction_prompt]
    )

    chain.MinimalChainable.to_delim_text_file(
        "resolution_mermaid_results", prompt_response
    )

    chain.MinimalChainable.to_delim_text_file(
        "resolution_mermaid_ctx_filled_prompts", ctx_filled_prompts
    )

    res = llm_module.parse_markdown_backticks(prompt_response[-1])

    img = mermaid.mm(res, output_file)

    return MermaidAgentResponse(img=img, mermaid=res)


def iterate_mermaid_agent(params: IterateMermaidParams) -> MermaidAgentResponse:
    model = build_model()

    change_prompt = params.change_prompt
    base_prompt = params.base_prompt
    current_mermaid_chart = params.current_mermaid_chart
    current_mermaid_img = params.current_mermaid_img
    output_file = params.output_file
    input_file = params.input_file

    file_content = ""
    if input_file:
        with open(input_file, "r") as file:
            file_content = file.read()

    iteration_prompt_1 = """You are a world-class expert at creating and modifying mermaid charts.

You have been given a current mermaid chart and a request for changes. Your task is to update the chart according to the requested changes.

<instructions>
    <instruction>Analyze the current mermaid chart and the requested changes.</instruction>
    <instruction>Update the mermaid chart to incorporate the requested changes.</instruction>
    <instruction>Ensure the updated chart still fulfills the original base prompt.</instruction>
    <instruction>Respond with the updated mermaid chart only.</instruction>
    <instruction>Do not wrap the mermaid chart in markdown code blocks.</instruction>
</instructions>

<current-mermaid-chart>
{{current_mermaid_chart}}
</current-mermaid-chart>

<base-prompt>
{{base_prompt}}
</base-prompt>

<change-request>
{{change_prompt}}
</change-request>

% if file_content:
<file-content>
${file_content}
</file-content>
% endif

Your updated mermaid chart:"""

    iteration_prompt_2 = """You are a world-class expert at creating and reviewing mermaid charts.

Your co-worker has just updated a mermaid chart based on requested changes. Your task is to review the updated chart to ensure it's correct and incorporates the requested changes.

<instructions>
    <instruction>Review the updated chart to ensure it's correct and incorporates the requested changes.</instruction>
    <instruction>Be very precise in your critique.</instruction>
    <instruction>If you see any mistakes or missing changes, correct them.</instruction>
    <instruction>Ensure the updated chart still fulfills the original base prompt.</instruction>
    <instruction>Respond with the final mermaid chart only.</instruction>
    <instruction>Do not wrap the mermaid chart in markdown code blocks.</instruction>
</instructions>

<updated-mermaid-chart>
{{output[-1]}}
</updated-mermaid-chart>

<base-prompt>
{{base_prompt}}
</base-prompt>

<change-request>
{{change_prompt}}
</change-request>

Your final mermaid chart:"""

    context = {
        "current_mermaid_chart": current_mermaid_chart,
        "base_prompt": base_prompt,
        "change_prompt": change_prompt,
        "file_content": file_content,
    }

    # Render the templates with the context
    rendered_iteration_prompt_1 = llm_module.conditional_render(
        iteration_prompt_1, {"file_content": file_content}
    )
    rendered_iteration_prompt_2 = iteration_prompt_2

    prompt_response, ctx_filled_prompts = chain.MinimalChainable.run(
        context,
        model,
        llm_module.prompt,
        prompts=[rendered_iteration_prompt_1, rendered_iteration_prompt_2],
    )

    chain.MinimalChainable.to_delim_text_file(
        "iteration_mermaid_results", prompt_response
    )

    chain.MinimalChainable.to_delim_text_file(
        "iteration_mermaid_ctx_filled_prompts", ctx_filled_prompts
    )

    res = llm_module.parse_markdown_backticks(prompt_response[-1])

    img = mermaid.mm(res, output_file)

    return MermaidAgentResponse(img=img, mermaid=res)
