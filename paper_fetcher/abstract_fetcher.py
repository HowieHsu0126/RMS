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
    - Saving and loading data to and from a JSON file

    Attributes:
        results_dir (str): Directory where results are stored.
        json_file_path (str): Path to the JSON file storing paper data.
        cache_enabled (bool): Whether to cache fetched data in memory.
        cache (list): Cache for storing paper data if caching is enabled.
    """

    def __init__(self, json_file_name, cache_enabled=True):
        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)
        self.json_file_path = os.path.join(self.results_dir, json_file_name)
        self.cache_enabled = cache_enabled
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

    def _save_to_json(self, data):
        """
        Saves provided data to a JSON file, ensuring file locking.

        Args:
            data (list): List of papers to be saved.
        """
        if self.cache_enabled:
            self.cache.extend(data)
            data_to_write = self.cache
        else:
            existing_data = self._load_existing_data()
            existing_data.extend(data)
            data_to_write = existing_data

        with FileLock(f"{self.json_file_path}.lock"):
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_write, f, ensure_ascii=False, indent=4)

        logging.info(f"Saved {len(data)} papers to {self.json_file_path}")

    def fetch_by_keywords(self, search_params=None, max_results=10):
        """
        Fetches papers based on search parameters and saves them to a file.

        Args:
            search_params (dict, optional): Search conditions for fetching papers. Defaults to None.
            max_results (int, optional): Maximum number of papers to fetch. Defaults to 10.

        Returns:
            int: Number of papers fetched and saved.
        """
        logging.info(
            "Fetching papers with parameters..." if search_params else "Fetching latest papers..."
        )

        papers = self.fetch_papers(search_params, max_results)

        # Save all fetched papers
        self._save_to_json(papers)
        return len(papers)

    def fetch_by_keywords_and_return_json(self, search_params=None, max_results=10):
        """
        Fetches papers based on search parameters and returns them in JSON format.

        Args:
            search_params (dict, optional): Search conditions for fetching papers. Defaults to None.
            max_results (int, optional): Maximum number of papers to fetch. Defaults to 10.

        Returns:
            str: JSON-formatted string containing the fetched papers.
        """
        logging.info(
            "Fetching papers with parameters for JSON output..." if search_params else "Fetching latest papers for JSON output..."
        )

        papers = self.fetch_papers(search_params, max_results)

        # Save all fetched papers to JSON file
        self._save_to_json(papers)

        # Return the papers in JSON format
        return json.dumps(papers, ensure_ascii=False, indent=4)
    
    def run(self, search_params=None, max_results=10, output_json=False):
        """
        Main entry point for running the paper fetch operation. 
        Provides success or failure status codes for external monitoring.
        Optionally returns the fetched papers in JSON format.

        Args:
            search_params (dict, optional): Search conditions for fetching papers. Defaults to None.
            max_results (int, optional): Maximum number of papers to fetch. Defaults to 10.
            output_json (bool, optional): If True, returns fetched papers as JSON instead of saving to file.

        Returns:
            str (optional): JSON-formatted string containing fetched papers (if output_json is True).
        """
        try:
            if output_json:
                result_json = self.fetch_and_return_json(search_params, max_results)
                fetched_count = len(json.loads(result_json))
                if fetched_count > 0:
                    logging.info(f"Fetched and returned {fetched_count} papers in JSON format.")
                    sys.exit(0)  # Success, JSON returned
                else:
                    logging.info("Fetch completed successfully but no papers found.")
                    sys.exit(1)  # No new papers found
            else:
                saved_count = self.fetch_by_keywords(search_params, max_results)
                if saved_count > 0:
                    logging.info("Fetch completed successfully with new papers.")
                    sys.exit(0)  # Success, new papers saved
                else:
                    logging.info("Fetch completed successfully but no new papers found.")
                    sys.exit(1)  # No new papers found
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            sys.exit(2)  # Error occurred


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
