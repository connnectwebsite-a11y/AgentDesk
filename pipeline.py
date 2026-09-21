
from agents import (
    triage_agent,
    diagnostic_agent,
    device_router_agent,
    source_relevance_agent,
    knowledge_agent,
    quality_control_loop
)

from knowledge import (
    search_knowledge,
    verify_official_sources,
    format_search_results
)


def select_relevant_sources(results, selection):

    if not selection or selection.strip().upper() == "NONE":
        return []

    numbers = []

    for item in selection.split(","):
        try:
            numbers.append(int(item.strip()))
        except ValueError:
            continue

    selected = []

    for number in numbers:
        index = number - 1

        if 0 <= index < len(results):
            selected.append(results[index])

    return selected


def run_agentdesk(client, tavily_client, ticket):

    print("🚀 AgentDesk started...")

    # 1. Triage
    print("1/8 Triage...")
    triage = triage_agent(
        client,
        ticket
    )

    # 2. Diagnosis
    print("2/8 Diagnostic...")
    diagnosis = diagnostic_agent(
        client,
        ticket,
        triage
    )

    # 3. Device routing
    print("3/8 Routing...")
    router = device_router_agent(
        client,
        ticket,
        diagnosis
    )

    # 4. Search documentation
    print("4/8 Searching documentation...")
    search_results = search_knowledge(
        tavily_client,
        ticket,
        router
    )

    # 5. Keep official sources
    print("5/8 Verifying official sources...")
    official_results = verify_official_sources(
        search_results
    )

    if not official_results:
        return "No suitable official documentation was found."

    # 6. Determine relevant sources
    print("6/8 Checking relevance...")

    official_text = format_search_results(
        official_results
    )

    selection = source_relevance_agent(
        client,
        ticket,
        router,
        official_text
    )

    selected_sources = select_relevant_sources(
        official_results,
        selection
    )

    if not selected_sources:
        return "No sufficiently relevant official documentation was found."

    evidence_context = format_search_results(
        selected_sources
    )

    # 7. Build troubleshooting plan
    print("7/8 Building troubleshooting plan...")

    troubleshooting_plan = knowledge_agent(
        client,
        ticket,
        diagnosis,
        router,
        evidence_context
    )

    # 8. QA + automatic revision
    print("8/8 Quality assurance...")

    quality = quality_control_loop(
        client,
        ticket,
        troubleshooting_plan,
        evidence_context
    )

    print("✅ AgentDesk completed")

    return {
        "ticket": ticket,
        "triage": triage,
        "diagnosis": diagnosis,
        "router": router,
        "sources": selected_sources,
        "evidence": evidence_context,
        "first_qa": quality["first_qa"],
        "revision_used": quality["revision_used"],
        "final_qa": quality["final_qa"],
        "final_response": quality["final_plan"]
    }
