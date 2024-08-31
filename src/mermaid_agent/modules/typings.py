from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, Union, Any
from PIL import Image


class FusionChainResult(BaseModel):
    top_response: Union[str, Dict[str, Any]]
    all_prompt_responses: List[List[Any]]
    all_context_filled_prompts: List[List[str]]
    performance_scores: List[float]
    model_names: List[str]


class OneShotMermaidParams(BaseModel):
    prompt: str
    output_file: str
    input_file: Optional[str] = None


class ResolutionMermaidParams(BaseModel):
    error: str
    damaged_mermaid_chart: str
    base_prompt: str
    output_file: str
    input_file: Optional[str] = None


class IterateMermaidParams(BaseModel):
    change_prompt: str
    base_prompt: str
    current_mermaid_chart: str
    current_mermaid_img: Image.Image
    output_file: str
    input_file: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BulkMermaidParams(BaseModel):
    prompt: str
    output_file: str
    input_file: Optional[str] = None
    count: int

class MermaidAgentResponse(BaseModel):
    img: Optional[Image.Image]
    mermaid: Optional[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)

class BulkMermaidAgentResponse(BaseModel):
    responses: List[MermaidAgentResponse]
