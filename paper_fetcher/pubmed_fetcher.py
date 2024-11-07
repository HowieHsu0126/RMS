# paper_fetcher/pubmed_fetcher.py
import logging
from xml.etree import ElementTree as ET

import requests

from .abstract_fetcher import AbstractPaperFetcher


class PubMedFetcher(AbstractPaperFetcher):
    """
    Fetcher for PubMed academic papers.
    """

    def __init__(self, json_file_name):
        super().__init__(json_file_name)

    def fetch_papers(self, search_params=None, max_results=10):
        """Fetch papers from PubMed based on search parameters."""
        query = self._build_query(search_params)
        response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
                                params={'db': 'pubmed', 'term': query, 'retmax': max_results, 'retmode': 'json'})
        if response.status_code == 200:
            ids = response.json().get("esearchresult", {}).get("idlist", [])
            return [self._fetch_article_details(article_id) for article_id in ids]
        else:
            logging.error(f"Error fetching from PubMed: {response.status_code}")
            return []

    def _build_query(self, search_params):
        """Helper to construct the PubMed search query string."""
        keyword = search_params.get('keyword', '')
        author = search_params.get('author', '')
        journal = search_params.get('journal', '')
        year = search_params.get('year', '')
        return f"{keyword}[Title/Abstract] {author}[Author] {journal}[Journal] {year}[Publication Date]".strip()

    def _fetch_article_details(self, article_id):
        """Fetch detailed information for a specific article from PubMed."""
        details_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={article_id}&retmode=xml"
        response = requests.get(details_url)
        if response.status_code == 200:
            return self._parse_article_details(response.content)
        else:
            logging.error(f"Error fetching article details for ID {article_id}: {response.status_code}")
            return {}

    def _parse_article_details(self, xml_content):
        """Parse XML content from PubMed and extract article information."""
        root = ET.fromstring(xml_content)
        return {
            "title": root.findtext(".//ArticleTitle", "N/A"),
            "authors": ', '.join(f"{author.findtext('ForeName', 'N/A')} {author.findtext('LastName', 'N/A')}" for author in root.findall(".//Author")),
            "abstract": root.findtext(".//Abstract/AbstractText", "N/A"),
            "year": root.findtext(".//PubDate/Year", "N/A"),
            "journal": root.findtext(".//Journal/Title", "N/A"),
            "volume": root.findtext(".//Journal/Volume", "N/A"),
            "pages": root.findtext(".//Pagination/MedlinePgn", "N/A"),
            "number": root.findtext(".//Journal/Issue", "N/A"),
            "publisher": root.findtext(".//PublisherName", "N/A"),
            "doi": root.findtext(".//ELocationID[@EIdType='doi']", "N/A"),
            "url": root.findtext(".//ArticleId[@IdType='pubmed']", "N/A")
        }
