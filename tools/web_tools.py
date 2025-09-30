from crewai.tools import tool
from typing import List
import requests
from bs4 import BeautifulSoup
from config import DefaultCFG


@tool
def get_search_results_tool(keyword: str, num_results: int = 5) -> List[str]:
    """
    Perform a web search using the Serper API and return the top num_results result URLs."""
    # Your API key can be loaded from a config
    serper_api_key = DefaultCFG.serper_api_key
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    data = {"q": keyword}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    results = response.json()
    return [res["link"] for res in results.get("organic", [])[:num_results] if "link" in res]


@tool
def scrape_search_results_tool(urls: List[str]) -> List[str]:
    """Scrape the content of each URL and return a list of cleaned text content."""
    # Set a
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup(["script", "style", "footer", "header", "nav", "noscript"]):
                tag.decompose()
            text = soup.get_text(separator="\n")
            lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 50]
            content = "\n".join(lines[:15])
            results.append(content)
        except Exception as e:
            results.append(f"⚠️ Error scraping {url}: {e}")
    return results
