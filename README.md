# Mermaid Diagram AI Agent
> Communicate your work with diagrams in seconds with GenAI + Mermaid

![Command Diagram](./imgs/mermaid_ai_agent.png)

## Setup
> Image generated WITH this tool!
![Setup](./imgs/setup.png)

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Install dependencies `uv sync`
- Set your OpenAI API key as an environment variable `export OPENAI_API_KEY=<your_api_key>`
- Optionally setup 
  - Optionally set ANTHROPIC_API_KEY, VERTEX_API_KEY, GROQ_API_KEY as environment variables. See `.env.sample` for details.
    - Update your LLM in the `src/mermaid_agent/modules/llm_module.py: build_model()` function.
- ✅ To run a single generation: 
  - `uv run main mer -p "Flowchart of ##setup instructions" -o "setup_diagram.png" -i "./README.md"`
  - `uv run main mer -p "state diagram of process: build prompt, generate HQ examples, iterate, build dataset, fine-tune, test, iterate, prompt " -o "fine_tune_process.png"`
  - `uv run main mer -p "pie chart title: 'Time Spent on Project Tasks', 'Coding': 40, 'Testing': 20, 'Documentation': 20, 'Meetings': 15, 'Learn AI Coding w/IndyDevDan': 5" -o "project_time_allocation.png"`
- ✅ To run an interactive generation:
  - `uv run main mer-iter -p "Flowchart of ##setup instructions" -o "setup_diagram.png" -i "./README.md"` 
- ✅ To run a bulk-version based iteration
  - `uv run main mer-bulk -p "Flowchart of ##setup instructions" -o "setup_diagram.png" -i "./README.md" -c 5` 
  - `uv run main mer-bulk -p "pie chart title: 'Time Spent on Project Tasks', 'Coding', 'Testing', 'Documentation', 'Meetings', 'Learn AI Coding w/IndyDevDan'" -o "project_time_allocation.png" -c 5`

## Learn AI Coding
- Watch us code the [mer-bulk command with AIDER](https://youtu.be/ag-KxYS8Vuw)

## Next
- [] every output/ session id directory for image 
- [] log the mermaid chart text to a /output file
- [] multiple input files for improved context
- [] params for size and theme?
- [] integration into idt?


## Resources
- https://gist.github.com/disler/d51d7e37c3e5f8d277d8e0a71f4a1d2e
- https://mermaid.ink/
- https://www.makotemplates.org/
- https://github.com/simonw/llm
- https://pypi.org/project/Mako/
- https://docs.astral.sh/uv/getting-started/features/#python-versions
- https://mermaid.js.org
- https://mermaid.js.org/syntax/examples.html
- https://ai.google.dev/api/models#models_list-shell