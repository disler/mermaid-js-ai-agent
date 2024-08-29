import pytest
from mermaid_agent.modules.llm_module import (
    build_gemini_duo,
    build_models,
    build_big_3_models,
)


def test_sonnet_3_5_model():
    # Build the models
    sonnet_3_5_model = build_models()

    # Define a simple prompt
    test_prompt = "What is the capital of France?"

    # Test sonnet_3_5_model
    sonnet_result = sonnet_3_5_model.prompt(test_prompt, temperature=0.5).text()
    assert (
        "Paris" in sonnet_result
    ), f"Unexpected response from sonnet_3_5_model: {sonnet_result}"
    print("Sonnet 3.5 response:", sonnet_result)


def test_build_big3_models():
    # Build the big 3 models
    sonnet_3_5_model, gpt4_o_model, gemini_1_5_pro_model = build_big_3_models()

    # Define a simple prompt
    test_prompt = "What is the capital of France?"

    # Test sonnet_3_5_model
    sonnet_result = sonnet_3_5_model.prompt(test_prompt, temperature=0.5).text()
    assert (
        "Paris" in sonnet_result
    ), f"Unexpected response from sonnet_3_5_model: {sonnet_result}"
    print("Sonnet 3.5 response:", sonnet_result)

    # Test gpt4_o_model
    gpt4_result = gpt4_o_model.prompt(test_prompt, temperature=0.5).text()
    assert (
        "Paris" in gpt4_result
    ), f"Unexpected response from gpt4_o_model: {gpt4_result}"
    print("GPT-4 response:", gpt4_result)

    # Test gemini_1_5_pro_model
    gemini_result = gemini_1_5_pro_model.prompt(test_prompt).text()
    assert (
        "Paris" in gemini_result
    ), f"Unexpected response from gemini_1_5_pro_model: {gemini_result}"
    print("Gemini 1.5 Pro response:", gemini_result)


def test_build_gemini_duo():
    # Build the Gemini duo models
    gemini_1_5_pro, gemini_1_5_flash = build_gemini_duo()

    # Define a simple prompt
    test_prompt = "What is the capital of France?"

    # Test gemini_1_5_pro
    pro_result = gemini_1_5_pro.prompt(test_prompt).text()
    assert (
        "Paris" in pro_result
    ), f"Unexpected response from gemini_1_5_pro: {pro_result}"
    print("Gemini 1.5 Pro response:", pro_result)

    # Test gemini_1_5_flash
    flash_result = gemini_1_5_flash.prompt(test_prompt).text()
    assert (
        "Paris" in flash_result
    ), f"Unexpected response from gemini_1_5_flash: {flash_result}"
    print("Gemini 1.5 Flash response:", flash_result)
