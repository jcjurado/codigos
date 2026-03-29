from langchain_community.tools.tavily_search import TavilySearchResults
from config import TAVILY_API_KEY, TAVILY_MAX_RESULTS


def get_search_tool() -> TavilySearchResults:
    return TavilySearchResults(
        max_results=TAVILY_MAX_RESULTS,
        api_key=TAVILY_API_KEY,
    )