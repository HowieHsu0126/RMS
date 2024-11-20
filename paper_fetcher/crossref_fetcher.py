import requests
import logging
from .abstract_fetcher import AbstractPaperFetcher


class CrossRefFetcher(AbstractPaperFetcher):
    """
    Fetcher for academic papers using the CrossRef API.
    """

    def __init__(self, json_file_name, cache_enabled=True):
        super().__init__(json_file_name, cache_enabled)
        self.base_url = "https://api.crossref.org/works"

    def fetch_papers(self, search_params=None, max_results=10):
        """Fetch papers from CrossRef based on search parameters."""
        query = self._build_query(search_params)
        params = {
            "query": query,
            "rows": max_results
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json().get("message", {}).get("items", [])
            papers = self._parse_papers(data)
            return papers
        except Exception as e:
            logging.error(f"Error fetching papers from CrossRef: {e}")
            return []

    def _build_query(self, search_params):
        """Construct the query string for CrossRef."""
        if not search_params:
            return ""
        keyword = search_params.get('keyword', '').strip()
        author = search_params.get('author', '').strip()
        return f"{keyword} {author}".strip()

    def _parse_papers(self, data):
        """Parse CrossRef response data into a list of paper dictionaries."""
        papers = []
        for item in data:
            paper = {
                "title": item.get("title", ["N/A"])[0],
                "author": ', '.join(
                    author.get("given", "N/A") + " " + author.get("family", "N/A")
                    for author in item.get("author", [])
                ) if "author" in item else "N/A",
                "year": item.get("created", {}).get("date-parts", [[0]])[0][0],
                "doi": item.get("DOI", "N/A"),
                "journal": item.get("container-title", ["N/A"])[0],
                "issn": ', '.join(item.get("ISSN", [])),
                "url": item.get("URL", "N/A"),
            }
            papers.append(paper)
        return papers
