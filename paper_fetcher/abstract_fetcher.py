import json
import logging
import os
import random
import time
from abc import ABC, abstractmethod
from filelock import FileLock
import sys  # For returning exit codes


class AbstractPaperFetcher(ABC):
    """
    Abstract base class for fetching academic papers. Provides common functionality such as:
    - Scheduling fetch operations
    - Deduplication of fetched data
    - Saving and loading data to and from a JSON file

    Attributes:
        results_dir (str): Directory where results are stored.
        json_file_path (str): Path to the JSON file storing paper data.
        cache_enabled (bool): Whether to cache fetched data in memory.
        paper_ids (set): Set of paper identifiers to ensure deduplication.
        cache (list): Cache for storing paper data if caching is enabled.
    """

    def __init__(self, json_file_name='papers.json', cache_enabled=True):
        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)
        self.json_file_path = os.path.join(self.results_dir, json_file_name)
        self.cache_enabled = cache_enabled
        self.paper_ids = self._load_existing_ids()
        self.cache = self._load_existing_data() if cache_enabled else []

    def _random_delay(self, min_delay=5, max_delay=10):
        """Pauses execution for a random interval within a specified range."""
        time.sleep(random.uniform(min_delay, max_delay))

    def _load_existing_data(self):
        """Loads existing data from the JSON file, if available, ensuring file locking."""
        if os.path.exists(self.json_file_path):
            with FileLock(f"{self.json_file_path}.lock"):
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return []

    def _load_existing_ids(self):
        """Extracts and returns a set of unique identifiers (DOI or URL) from existing data."""
        return {paper.get('doi') or paper.get('url') for paper in self._load_existing_data() if paper.get('doi') or paper.get('url')}

    def _save_to_json(self, data):
        """
        Saves provided data to a JSON file, ensuring file locking.

        Args:
            data (list): List of papers to be saved. Each paper should have unique identifiers for deduplication.
        """
        if self.cache_enabled:
            self.cache.extend(data)
            data_to_write = self.cache
        else:
            existing_data = self._load_existing_data()
            existing_data.extend(data)
            data_to_write = existing_data

        self.paper_ids.update(paper.get('doi') or paper.get('url')
                              for paper in data)

        with FileLock(f"{self.json_file_path}.lock"):
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_write, f, ensure_ascii=False, indent=4)

        logging.info(f"Saved {len(data)} papers to {self.json_file_path}")

    def fetch_by_keywords(self, search_params=None, max_results=10):
        """
        Fetches papers based on search parameters, filters out duplicates, and saves new papers.

        Args:
            search_params (dict, optional): Search conditions for fetching papers. Defaults to None.
            max_results (int, optional): Maximum number of papers to fetch. Defaults to 10.

        Returns:
            int: Number of newly saved papers.
        """
        logging.info(
            "Fetching papers with parameters..." if search_params else "Fetching latest papers...")

        papers = self.fetch_papers(search_params, max_results)
        new_papers = [paper for paper in papers if paper.get(
            'doi') not in self.paper_ids and paper.get('url') not in self.paper_ids]

        if new_papers:
            self._save_to_json(new_papers)
            return len(new_papers)
        else:
            logging.info("No new papers found.")
            return 0

    def run(self, search_params=None, max_results=10):
        """
        Main entry point for running the paper fetch operation. 
        Provides success or failure status codes for external monitoring.

        Args:
            search_params (dict, optional): Search conditions for fetching papers. Defaults to None.
            max_results (int, optional): Maximum number of papers to fetch. Defaults to 10.
        """
        try:
            saved_count = self.fetch_by_keywords(search_params, max_results)
            logging.info("Fetch completed successfully.")
            sys.exit(0 if saved_count > 0 else 1)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            sys.exit(1)

    @abstractmethod
    def fetch_papers(self, search_params=None, max_results=10):
        """
        Abstract method to fetch papers based on search parameters. 
        Must be implemented by subclasses.

        Args:
            search_params (dict, optional): Search conditions for fetching papers. Defaults to None.
            max_results (int, optional): Maximum number of papers to fetch. Defaults to 10.

        Returns:
            list: List of fetched papers.
        """
        pass
