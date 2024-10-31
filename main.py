# main.py
from paper_fetcher.pubmed_fetcher import PubMedFetcher
from paper_fetcher.utils import setup_logging

if __name__ == "__main__":
    setup_logging()

    pm_fetcher = PubMedFetcher()
    search_params_pm = {
        "keyword": "cancer",
        "author": "",
        "journal": "Nature",
        "year": "2020"
    }
    pm_fetcher.fetch_by_keywords(search_params_pm, max_results=15)
