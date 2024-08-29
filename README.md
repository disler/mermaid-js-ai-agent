# Mermaid Agent

## Next
- session ids + output dir
- add a resolution agent in `iterate_mermaid_agent`
- params for size and theme?
- testing
- cool use cases
- integration into IDT?

## Setup
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Install dependencies `uv sync`
- Set your OpenAI API key as an environment variable `export OPENAI_API_KEY=<your_api_key>`
- Optionally setup 
  - Optionally set ANTHROPIC_API_KEY, VERTEX_API_KEY, GROQ_API_KEY as environment variables. See `.env.sample` for details.

## Docs on gemini models
- https://ai.google.dev/api/models#models_list-SHELL
- Run this to get the latest models:
  - `export GOOGLE_API_KEY=<FILL IN HERE>`
  - `curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY"`  


## Resources
- https://mermaid.ink/
- https://www.makotemplates.org/
- https://pypi.org/project/Mako/
- https://docs.astral.sh/uv/getting-started/features/#python-versions
- https://mermaid.js.org/syntax/examples.html