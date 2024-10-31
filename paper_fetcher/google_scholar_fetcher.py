# paper_fetcher/google_scholar_fetcher.py
import logging

from scholarly import scholarly

from .abstract_fetcher import AbstractPaperFetcher


class GoogleScholarFetcher(AbstractPaperFetcher):
    """
    Fetcher for Google Scholar academic papers.
    """

    def __init__(self, json_file_path='gs_res.json'):
        super().__init__(json_file_path)

    def fetch_papers(self, search_params=None, max_results=10):
        """Fetch papers from Google Scholar based on search parameters."""
        query = self._build_query(search_params)
        if not query:
            logging.warning("Invalid query, returning empty result.")
            return []

        try:
            search_query = scholarly.search_pubs(query)
            papers = [self._parse_paper_info(paper) for paper in search_query][:max_results]
            return papers
        except Exception as e:
            logging.error(f"Error fetching from Google Scholar: {str(e)}")
            return []

    def _build_query(self, search_params):
        """Helper to construct the search query string."""
        keyword = search_params.get('keyword', '').strip()
        author = f'author:{search_params.get("author", "").strip()}' if search_params.get('author', '') else ''
        year = f'year:{search_params.get("year", "").strip()}' if search_params.get('year', '') else ''
        return f'{keyword} {author} {year}'.strip()

    def _parse_paper_info(self, paper):
        """Parse paper information from Google Scholar result."""
        scholarly.fill(paper)
        bib = paper.get('bib', {})
        return {
            "title": bib.get('title', 'N/A'),
            "author": ', '.join(bib.get('author', [])),
            "abstract": bib.get('abstract', 'N/A'),
            "year": bib.get('pub_year', 'N/A'),
            "journal": bib.get('venue', 'N/A'),
            "citation_count": paper.get('num_citations', 'N/A'),
            "doi": paper.get('doi', 'N/A'),
            "url": paper.get('eprint_url', 'N/A')
        }
