
from tavily import TavilyClient


def search_knowledge(tavily_client, ticket, router_result):

    query = f"""
    Find official technical support documentation for:

    User problem:
    {ticket}

    Device information:
    {router_result}
    """

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return response.get("results", [])


def format_search_results(results):

    if not results:
        return "No documentation found."

    output = ""

    for number, result in enumerate(results, start=1):

        title = result.get("title", "Unknown title")
        url = result.get("url", "")
        content = result.get("content", "")

        output += f"""
SOURCE {number}

Title: {title}
URL: {url}

Content:
{content}

---
"""

    return output


OFFICIAL_DOMAINS = {
    "Microsoft": [
        "support.microsoft.com"
    ],
    "Apple": [
        "support.apple.com"
    ],
    "Samsung": [
        "samsung.com"
    ],
    "Google": [
        "support.google.com"
    ],
    "Dell": [
        "dell.com"
    ],
    "HP": [
        "support.hp.com"
    ],
    "Lenovo": [
        "support.lenovo.com"
    ]
}


def verify_official_sources(results):

    verified = []

    for result in results:

        url = result.get("url", "").lower()

        for company, domains in OFFICIAL_DOMAINS.items():

            if any(domain in url for domain in domains):

                verified_result = result.copy()
                verified_result["official_vendor"] = company

                verified.append(verified_result)
                break

    return verified
