
from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"


def ask_llm(client, system_prompt, user_prompt):

    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content


def triage_agent(client, ticket):

    system_prompt = """
You are the Triage Agent for AgentDesk, an IT support system.

Analyze the user's IT problem.

Return exactly:

Category: <category>
Priority: <Low, Medium, High>
Summary: <short summary>

Choose an appropriate category such as:
Network, Hardware, Software, Account, Security,
Audio, Camera, Mobile, or Other.

Do not troubleshoot the problem yet.
"""

    return ask_llm(
        client,
        system_prompt,
        ticket
    )


def diagnostic_agent(client, ticket, triage_result):

    system_prompt = """
You are the Diagnostic Agent for AgentDesk.

Analyze the IT support ticket and the Triage Agent result.

Identify:
- likely causes of the problem
- information relevant to troubleshooting

Do not invent facts about the user's device.
Do not give the final customer response yet.

Keep the diagnosis concise.
"""

    user_prompt = f"""
USER TICKET:
{ticket}

TRIAGE RESULT:
{triage_result}
"""

    return ask_llm(
        client,
        system_prompt,
        user_prompt
    )


def device_router_agent(client, ticket, diagnostic_result):

    system_prompt = """
You are the Device and Knowledge Router for AgentDesk.

Determine what type of device and documentation
should be used for this IT support problem.

Return exactly:

Device Type: <device type>
Operating System: <operating system or Unknown>
Brand: <brand or Unknown>
Issue Category: <category>
Knowledge Source Needed: <official documentation source>

Important:
Do not guess a brand or operating system.
If the ticket does not provide enough information,
use Unknown.
"""

    user_prompt = f"""
USER TICKET:
{ticket}

DIAGNOSTIC RESULT:
{diagnostic_result}
"""

    return ask_llm(
        client,
        system_prompt,
        user_prompt
    )


def source_relevance_agent(
    client,
    ticket,
    router_result,
    source_text
):

    system_prompt = """
You are the Source Relevance Agent for AgentDesk.

Your job is to select which official documentation
sources are directly useful for solving the user's
specific IT problem.

You will receive numbered sources.

Return ONLY the source numbers that are relevant.

Example:
1, 3

Rules:
- Prefer documentation directly addressing the problem.
- Reject unrelated documentation.
- Reject sources for the wrong device or operating system.
- Do not invent source numbers.
- If no source is relevant, return NONE.
"""

    user_prompt = f"""
USER TICKET:
{ticket}

DEVICE ROUTER:
{router_result}

OFFICIAL SOURCES:
{source_text}
"""

    return ask_llm(
        client,
        system_prompt,
        user_prompt
    )


def knowledge_agent(
    client,
    ticket,
    diagnostic_result,
    router_result,
    evidence_context
):

    system_prompt = """
You are the Knowledge Agent for AgentDesk.

Create a technical troubleshooting plan using ONLY
the supplied official documentation evidence.

Rules:

- Do not invent troubleshooting steps.
- Do not recommend commands or settings unless they
  are supported by the supplied evidence.
- Keep steps appropriate for the user's device and OS.
- Start with safer and simpler troubleshooting steps.
- Do not claim a step will definitely fix the problem.
- If the evidence is insufficient, clearly say so.
- Do not use knowledge outside the supplied evidence.

For each troubleshooting step, briefly explain what
the user should do.
"""

    user_prompt = f"""
USER TICKET:
{ticket}

DIAGNOSIS:
{diagnostic_result}

DEVICE INFORMATION:
{router_result}

OFFICIAL DOCUMENTATION EVIDENCE:
{evidence_context}

Create the troubleshooting plan.
"""

    return ask_llm(
        client,
        system_prompt,
        user_prompt
    )


def qa_agent(
    client,
    ticket,
    troubleshooting_plan,
    evidence_context
):

    system_prompt = """
You are the Quality Assurance Agent for AgentDesk.

Check whether the proposed troubleshooting plan is
supported by the supplied official documentation.

Check for:
- unsupported troubleshooting steps
- instructions for the wrong device or operating system
- invented commands or settings
- unsafe or unnecessary actions
- claims not supported by the evidence

Return exactly one of these formats:

APPROVED

or

NEEDS_REVISION
Reason: <brief explanation>

Be strict. If an important troubleshooting step is not
supported by the supplied evidence, request revision.
"""

    user_prompt = f"""
USER TICKET:
{ticket}

PROPOSED TROUBLESHOOTING PLAN:
{troubleshooting_plan}

OFFICIAL DOCUMENTATION EVIDENCE:
{evidence_context}
"""

    return ask_llm(
        client,
        system_prompt,
        user_prompt
    )


def revision_agent(
    client,
    ticket,
    troubleshooting_plan,
    qa_result,
    evidence_context
):

    system_prompt = """
You are the Revision Agent for AgentDesk.

The QA Agent has reviewed a troubleshooting plan.

Rewrite the plan so that it passes quality assurance.

Rules:
- Remove unsupported troubleshooting steps.
- Remove instructions for the wrong device or OS.
- Use ONLY the supplied official documentation evidence.
- Address the QA Agent's concerns.
- Do not invent commands, settings, or procedures.
- Keep the instructions clear for a normal user.
- Preserve useful steps that are supported by evidence.
"""

    user_prompt = f"""
USER TICKET:
{ticket}

ORIGINAL TROUBLESHOOTING PLAN:
{troubleshooting_plan}

QA REVIEW:
{qa_result}

OFFICIAL DOCUMENTATION EVIDENCE:
{evidence_context}

Produce the corrected troubleshooting plan.
"""

    return ask_llm(
        client,
        system_prompt,
        user_prompt
    )


def quality_control_loop(
    client,
    ticket,
    troubleshooting_plan,
    evidence_context
):

    # First QA check
    first_qa = qa_agent(
        client,
        ticket,
        troubleshooting_plan,
        evidence_context
    )

    # Already approved
    if first_qa.strip().upper().startswith("APPROVED"):

        return {
            "final_plan": troubleshooting_plan,
            "first_qa": first_qa,
            "revision_used": False,
            "final_qa": first_qa
        }

    # Revision required
    revised_plan = revision_agent(
        client,
        ticket,
        troubleshooting_plan,
        first_qa,
        evidence_context
    )

    # Check revised answer again
    final_qa = qa_agent(
        client,
        ticket,
        revised_plan,
        evidence_context
    )

    return {
        "final_plan": revised_plan,
        "first_qa": first_qa,
        "revision_used": True,
        "final_qa": final_qa
    }
