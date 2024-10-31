# paper_fetcher/arxiv_fetcher.py
import logging
from xml.etree import ElementTree as ET

import requests

from .abstract_fetcher import AbstractPaperFetcher


class ArXivFetcher(AbstractPaperFetcher):
    """
    Fetcher for ArXiv academic papers.
    """

    def __init__(self, json_file_path='arxiv_res.json'):
        super().__init__(json_file_path)

    def fetch_papers(self, search_params=None, max_results=10):
        """Fetch papers from ArXiv based on search parameters."""
        query = self._build_query(search_params)
        response = requests.get('http://export.arxiv.org/api/query', params={
                                'search_query': f'all:{query}', 'start': 0, 'max_results': max_results})

        if response.status_code == 200:
            return self._parse_paper_info(response.content)
        else:
            logging.error(
                f"Error fetching papers from ArXiv: {response.status_code}")
            return []

    def _build_query(self, search_params):
        """Helper to construct the search query string."""
        if search_params is None:
            return ''
        keyword = search_params.get('keyword', '').strip()
        author = search_params.get('author', '').strip()
        year = search_params.get('year', '').strip()
        return f"{keyword} {author} {year}".strip()

    def _parse_paper_info(self, xml_content):
        """Parse XML content from ArXiv and extract paper information."""
        root = ET.fromstring(xml_content)
        papers = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            paper = {
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                "author": ', '.join(author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")),
                "abstract": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
                "year": entry.find("{http://www.w3.org/2005/Atom}published").text.split('-')[0],
                "url": entry.find("{http://www.w3.org/2005/Atom}id").text,
            }
            papers.append(paper)
        return papers
