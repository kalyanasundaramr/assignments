
from ddgs import DDGS


def search_web(query: str) -> str:
    """
    Search the web for current information, SEO trends,
    relevant keywords, and content research.

    Args:
        query: Search query related to the SEO content topic.

    Returns:
        Search results containing titles, URLs, and summaries.
    """
    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )

        if not results:
            return "No search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            url = result.get("href", "")
            description = result.get("body", "")

            formatted_results.append(
                f"Result {index}\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Description: {description}"
            )

        return "\n\n".join(formatted_results)

    except Exception as error:
        return f"Web search failed: {error}"
