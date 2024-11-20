from scholarly import scholarly, ProxyGenerator
import logging
import time
import requests
from .abstract_fetcher import AbstractPaperFetcher


class GoogleScholarFetcher(AbstractPaperFetcher):
    """
    Fetcher for Google Scholar academic papers.
    """

    def __init__(self, json_file_name):
        super().__init__(json_file_name)
        self.max_retries = 5
        self.base_timeout = 10

    def fetch_papers(self, search_params=None, max_results=10):
        """Fetch papers from Google Scholar based on search parameters."""
        query = self._build_query(search_params)
        if not query:
            logging.warning("Invalid query, returning empty result.")
            return []

        retry_count = 0
        timeout = self.base_timeout

        while retry_count < self.max_retries:
            try:
                search_query = scholarly.search_pubs(query)
                papers = [self._parse_paper_info(paper) for paper in search_query][:max_results]
                enriched_papers = [self._enrich_with_crossref(paper) for paper in papers]
                return enriched_papers
            except Exception as e:
                retry_count += 1
                logging.error(f"Attempt {retry_count} failed: {e}")
                if retry_count < self.max_retries:
                    logging.info(f"Retrying in {timeout} seconds...")
                    time.sleep(timeout)
                    timeout *= 2
                else:
                    logging.error(f"Giving up after {retry_count} attempts.")
                    break

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
            "url": paper.get('eprint_url', 'N/A'),
            "issn": "N/A"  # Placeholder for ISSN
        }

    def _enrich_with_crossref(self, paper):
        """Enrich paper information with CrossRef data to fetch ISSN."""
        if not paper.get("doi"):
            logging.info("No DOI available, skipping CrossRef enrichment.")
            return paper

        crossref_url = f"https://api.crossref.org/works/{paper['doi']}"
        try:
            response = requests.get(crossref_url, timeout=10)
            if response.status_code == 200:
                data = response.json().get("message", {})
                issn_list = data.get("ISSN", [])
                paper["issn"] = ', '.join(issn_list) if issn_list else "N/A"
            else:
                logging.warning(f"CrossRef query failed for DOI {paper['doi']} with status {response.status_code}.")
        except Exception as e:
            logging.error(f"Error querying CrossRef for DOI {paper['doi']}: {e}")

        return paper
