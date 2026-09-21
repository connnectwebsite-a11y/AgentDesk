
import os
import gradio as gr

from groq import Groq
from tavily import TavilyClient

from pipeline import run_agentdesk


# API keys are read from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def create_clients():

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing.")

    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is missing.")

    groq_client = Groq(
        api_key=GROQ_API_KEY
    )

    tavily_client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    return groq_client, tavily_client


def support_ticket_ui(problem):

    if not problem or not problem.strip():
        return "Please describe your IT problem."

    try:
        groq_client, tavily_client = create_clients()

        result = run_agentdesk(
            groq_client,
            tavily_client,
            problem.strip()
        )

        if not isinstance(result, dict):
            return result

        response = result["final_response"]

        sources = result.get("sources", [])

        source_text = ""

        for source in sources:

            title = source.get(
                "title",
                "Official documentation"
            )

            url = source.get("url", "")

            source_text += f"- [{title}]({url})\n"

        return f"""
# 🤖 AgentDesk Response

{response}

## Official Sources

{source_text}
"""

    except Exception as error:
        return f"❌ AgentDesk error: {error}"


with gr.Blocks(title="AgentDesk") as app:

    gr.Markdown("""
# 🛠️ AgentDesk

### Multi-Agent IT Support

Describe your technical problem below.
AgentDesk will search official documentation,
generate troubleshooting steps and perform
quality assurance before responding.
""")

    problem_input = gr.Textbox(
        label="IT Problem",
        placeholder="Example: My Windows 11 laptop has no sound.",
        lines=5
    )

    submit_button = gr.Button(
        "Create Support Ticket",
        variant="primary"
    )

    response_output = gr.Markdown()

    submit_button.click(
        fn=support_ticket_ui,
        inputs=problem_input,
        outputs=response_output
    )


if __name__ == "__main__":
    app.launch(share=True)
