from typing import Any, List, Tuple

from pydantic import BaseModel
from mermaid_agent.modules.chain import MinimalChainable, FusionChain
from mermaid_agent.modules.llm_module import (
    build_big_3_models,
    prompt as llm_prompt,
    get_model_name,
)
from mermaid_agent.modules.typings import FusionChainResult


def test_chainable_solo():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return f"Solo response: {prompt}"

    # Test context and single chain
    context = {"variable": "Test"}
    chains = ["Single prompt: {{variable}}"]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Assert the results
    assert len(result) == 1
    assert result[0] == "Solo response: Single prompt: Test"


def test_chainable_run():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return f"Response to: {prompt}"

    # Test context and chains
    context = {"var1": "Hello", "var2": "World"}
    chains = ["First prompt: {{var1}}", "Second prompt: {{var2}} and {{var1}}"]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Assert the results
    assert len(result) == 2
    assert result[0] == "Response to: First prompt: Hello"
    assert result[1] == "Response to: Second prompt: World and Hello"


def test_chainable_with_output():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return f"Response to: {prompt}"

    # Test context and chains
    context = {"var1": "Hello", "var2": "World"}
    chains = ["First prompt: {{var1}}", "Second prompt: {{var2}} and {{output[-1]}}"]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Assert the results
    assert len(result) == 2
    assert result[0] == "Response to: First prompt: Hello"
    assert (
        result[1]
        == "Response to: Second prompt: World and Response to: First prompt: Hello"
    )


def test_chainable_json_output():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        if "Output JSON" in prompt:
            return '{"key": "value"}'
        return prompt

    # Test context and chains
    context = {"test": "JSON"}
    chains = ["Output JSON: {{test}}", "Reference JSON: {{output[-1].key}}"]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Assert the results
    assert len(result) == 2
    assert isinstance(result[0], dict)
    print("result", result)
    assert result[0] == {"key": "value"}
    assert result[1] == "Reference JSON: value"  # Remove quotes around "value"


def test_chainable_reference_entire_json_output():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        if "Output JSON" in prompt:
            return '{"key": "value"}'
        return prompt

    context = {"test": "JSON"}
    chains = ["Output JSON: {{test}}", "Reference JSON: {{output[-1]}}"]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    assert len(result) == 2
    assert isinstance(result[0], dict)
    assert result[0] == {"key": "value"}
    assert result[1] == 'Reference JSON: {"key": "value"}'


def test_chainable_reference_long_output_value():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return prompt

    context = {"test": "JSON"}
    chains = [
        "Output JSON: {{test}}",
        "1 Reference JSON: {{output[-1]}}",
        "2 Reference JSON: {{output[-2]}}",
        "3 Reference JSON: {{output[-1]}}",
    ]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    assert len(result) == 4
    assert result[0] == "Output JSON: JSON"
    assert result[1] == "1 Reference JSON: Output JSON: JSON"
    assert result[2] == "2 Reference JSON: Output JSON: JSON"
    assert result[3] == "3 Reference JSON: 2 Reference JSON: Output JSON: JSON"


def test_chainable_empty_context():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return prompt

    # Test with empty context
    context = {}
    chains = ["Simple prompt"]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Assert the results
    assert len(result) == 1
    assert result[0] == "Simple prompt"


def test_chainable_json_output_with_markdown():
    # Mock model and callable function
    class MockModel:
        pass

    def mock_callable_prompt(model, prompt):
        return """
        Here's a JSON response wrapped in markdown:
        ```json
        {
            "key": "value",
            "number": 42,
            "nested": {
                "inner": "content"
            }
        }
        ```
        """

    context = {}
    chains = ["Test JSON parsing"]

    # Run the Chainable
    result, _ = MinimalChainable.run(context, MockModel(), mock_callable_prompt, chains)

    # Assert the results
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert result[0] == {"key": "value", "number": 42, "nested": {"inner": "content"}}


# ------------ CompetitionChainable.run

import random


def test_fusion_chain_run():
    # Mock models
    class MockModel:
        def __init__(self, name):
            self.name = name

    # Mock callable function
    def mock_callable_prompt(model, prompt):
        return f"{model.name} response: {prompt}"

    # Mock evaluator function (random scores between 0 and 1)
    def mock_evaluator(outputs):
        top_response = random.choice(outputs)
        scores = [random.random() for _ in outputs]
        return top_response, scores

    # Test context and chains
    context = {"var1": "Hello", "var2": "World"}
    chains = ["First prompt: {{var1}}", "Second prompt: {{var2}} and {{output[-1]}}"]

    # Create mock models
    models = [MockModel(f"Model{i}") for i in range(3)]

    # Mock get_model_name function
    def mock_get_model_name(model):
        return model.name

    # Run the FusionChain
    result = FusionChain.run(
        context=context,
        models=models,
        callable=mock_callable_prompt,
        prompts=chains,
        evaluator=mock_evaluator,
        get_model_name=mock_get_model_name,
    )

    # Assert the results
    assert isinstance(result, FusionChainResult)
    assert len(result.all_prompt_responses) == 3
    assert len(result.all_context_filled_prompts) == 3
    assert len(result.performance_scores) == 3
    assert len(result.model_names) == 3

    for i, (outputs, context_filled_prompts) in enumerate(
        zip(result.all_prompt_responses, result.all_context_filled_prompts)
    ):
        assert len(outputs) == 2
        assert len(context_filled_prompts) == 2

        assert outputs[0] == f"Model{i} response: First prompt: Hello"
        assert (
            outputs[1]
            == f"Model{i} response: Second prompt: World and Model{i} response: First prompt: Hello"
        )

        assert context_filled_prompts[0] == "First prompt: Hello"
        assert (
            context_filled_prompts[1]
            == f"Second prompt: World and Model{i} response: First prompt: Hello"
        )

    # Check that performance scores are between 0 and 1
    assert all(0 <= score <= 1 for score in result.performance_scores)

    # Check that the number of unique scores is likely more than 1 (random function)
    assert (
        len(set(result.performance_scores)) > 1
    ), "All performance scores are the same, which is unlikely with a random evaluator"

    # Check that top_response is present and is either a string or a dict
    assert isinstance(result.top_response, (str, dict))

    # Print the output of FusionChain.run
    print("All outputs:")
    for i, outputs in enumerate(result.all_prompt_responses):
        print(f"Model {i}:")
        for j, output in enumerate(outputs):
            print(f"  Chain {j}: {output}")

    print("\nAll context filled prompts:")
    for i, prompts in enumerate(result.all_context_filled_prompts):
        print(f"Model {i}:")
        for j, prompt in enumerate(prompts):
            print(f"  Chain {j}: {prompt}")

    print("\nPerformance scores:")
    for i, score in enumerate(result.performance_scores):
        print(f"Model {i}: {score}")

    print("\nTop response:")
    print(result.top_response)

    print("result.model_dump: ", result.model_dump())
    print("result.model_dump_json: ", result.model_dump_json())


def test_real_fusion_chain_run():

    sonnet_3_5_model, gpt4_o_model, gemini_1_5_pro_model = build_big_3_models()

    code_request = (
        "Python code to Scrape the URL and return the content within the <body> tag"
    )

    context = {
        "code_request": code_request,
    }

    prompts = [
        # Prompt 1
        """
        Draft a high-level plan for code that will fulfill the CODE_REQUEST. Include the main steps and any libraries that might be useful. Be concise and short.

        ## CODE_REQUEST
        {{code_request}}

        ## Code Draft Plan""",
        # Prompt 2
        """
        Write code to fulfill the CODE_REQUEST. Use appropriate libraries and error handling.

        ## CODE_REQUEST
        {{code_request}}

        ## Code Draft
        {{output[-1]}}

        ## Code""",
        # Prompt 3
        """
        Review the code draft and code for fulfilling the CODE_REQUEST. Make improvements and produce concise, final, readable, and runnable production level code.

        ## CODE_REQUEST
        {{code_request}}

        ## Code Draft
        {{output[-2]}}

        ## Code
        ```
        {{output[-1]}}
        ```

        ## Production Code""",
    ]

    def evaluator(outputs: List[str]) -> Tuple[Any, List[float]]:

        outputs_as_str_md = "\n".join(
            [f"### Output {n+1}\n```{content}```" for n, content in enumerate(outputs)]
        )

        eval_prompt = """# Given these outputs, evaluate them on a scale of 0.0 - 1.0, where the maximum rating is given to the most relevant and accurate output given the PROMPT_REQUEST.

Respond in this JSON format {"ratings": [float, float, float, ...]} where each float is the rating for the corresponding output.
Respond strictly in JSON format, do not include any other text in your response.

## PROMPT_REQUEST
{{prompt_request}}

## Outputs
{{outputs_as_str_md}}

## Your Rating In JSON:"""

        eval_prompt_responses, context_filled_prompts = MinimalChainable.run(
            context={
                "prompt_request": code_request,
                "outputs_as_str_md": outputs_as_str_md,
            },
            model=sonnet_3_5_model,
            callable=llm_prompt,
            prompts=[eval_prompt],
        )

        class Parse(BaseModel):
            ratings: List[float]

        print("eval_prompt_responses", eval_prompt_responses)
        print("context_filled_prompts", context_filled_prompts)

        ratings = Parse.model_validate(eval_prompt_responses[-1]).ratings

        top_response = outputs[ratings.index(max(ratings))]

        return top_response, ratings

    models = [sonnet_3_5_model, gpt4_o_model, gemini_1_5_pro_model]
    # models = [sonnet_3_5_model, gpt4_o_model]

    result = FusionChain.run_parallel(
        context=context,
        models=models,
        callable=llm_prompt,
        prompts=prompts,
        evaluator=evaluator,
        get_model_name=get_model_name,
    )

    # Assertions
    assert isinstance(result, FusionChainResult)
    assert len(result.all_prompt_responses) == 3, "Should have outputs for all 3 models"
    assert (
        len(result.all_context_filled_prompts) == 3
    ), "Should have context-filled prompts for all 3 models"
    assert (
        len(result.performance_scores) == 3
    ), "Should have performance scores for all 3 models"
    assert len(result.model_names) == 3, "Should have names for all 3 models"

    for model_outputs, model_prompts in zip(
        result.all_prompt_responses, result.all_context_filled_prompts
    ):
        assert (
            len(model_outputs) == 3
        ), "Each model should have 3 outputs (one for each prompt)"
        assert (
            len(model_prompts) == 3
        ), "Each model should have 3 context-filled prompts"

        # Check if the outputs contain Python code
        assert any(
            "def" in output or "import" in output for output in model_outputs
        ), "At least one output should contain Python code"

        # Check if the context is properly filled in the prompts
        assert all(
            "{{code_request}}" not in prompt for prompt in model_prompts
        ), "All placeholders should be replaced in the prompts"

    # Check if the performance scores are reasonable
    assert all(
        0 <= score <= 1 for score in result.performance_scores
    ), "All performance scores should be between 0 and 1"

    # Check that top_response is present and is either a string or a dict
    assert isinstance(
        result.top_response, (str, dict)
    ), "Top response should be either a string or a dict"

    # Build up a string with results for manual inspection
    result_string = ""
    for i, (model_outputs, model_prompts, score) in enumerate(
        zip(
            result.all_prompt_responses,
            result.all_context_filled_prompts,
            result.performance_scores,
        )
    ):
        result_string += f"\nModel {i + 1}:\n"
        result_string += f"Performance score: {score}\n"
        for j, (output, prompt) in enumerate(zip(model_outputs, model_prompts)):
            result_string += f"\nPrompt {j + 1}:\n"
            result_string += prompt
            result_string += "\n\nOutput:\n"
            result_string += output
            result_string += "\n"
        result_string += "\n" + "=" * 50 + "\n"

    # add eval summary
    eval_summary = "\n\nEvaluation Scores:\n" + "\n".join(
        [
            f"Model {i+1} ({model.model_id}): {score:.2f}"
            for i, (model, score) in enumerate(zip(models, result.performance_scores))
        ]
    )

    result_string += "\nTest completed successfully!\n"

    # Write the result string to a file
    with open("./test_output.txt", "w") as f:
        f.write(result_string)

    print("Results have been written to test_output.txt")
