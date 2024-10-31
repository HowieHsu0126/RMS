# paper_fetcher/abstract_fetcher.py
import json
import logging
import os
import random
import time
from abc import ABC, abstractmethod  # 导入 ABC 和 abstractmethod

import schedule


class AbstractPaperFetcher(ABC):
    """
    Abstract base class for fetching academic papers. Provides common
    functionality like scheduling, data deduplication, and saving/loading data.
    """

    def __init__(self, json_file_path='papers.json'):
        self.json_file_path = json_file_path
        # Load IDs for deduplication
        self.paper_ids = set(self._load_existing_ids())

    def _random_delay(self, min_delay=5, max_delay=10):
        """Introduces a random delay to avoid being flagged as a bot."""
        time.sleep(random.uniform(min_delay, max_delay))

    def _load_existing_data(self):
        """Load existing JSON data from file or return an empty list."""
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _load_existing_ids(self):
        """Load unique identifiers (DOI/URL) for deduplication from existing papers."""
        existing_data = self._load_existing_data()
        return {paper.get('doi') or paper.get('url') for paper in existing_data if paper.get('doi') or paper.get('url')}

    def _save_to_json(self, data):
        """Append new papers to JSON file and update the deduplication set."""
        existing_data = self._load_existing_data()
        existing_data.extend(data)

        self.paper_ids.update(paper.get('doi') or paper.get('url')
                              for paper in data)

        with open(self.json_file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        logging.info(f"Saved {len(data)} papers to {self.json_file_path}")

    def fetch_by_keywords(self, search_params=None, max_results=10):
        """
        Fetch papers based on specified search conditions and save to JSON file.

        Args:
            search_params (dict): Search conditions (keywords, authors, etc.)
            max_results (int): Maximum number of results to fetch
        """
        if search_params is None:
            logging.info("Fetching the latest uploaded papers...")
        else:
            logging.info(
                f"Fetching papers matching search conditions: {search_params}")

        papers = self.fetch_papers(search_params, max_results)

        # Deduplicate and save new papers
        new_papers = [paper for paper in papers if paper.get(
            'doi') not in self.paper_ids and paper.get('url') not in self.paper_ids]

        if new_papers:
            self._save_to_json(new_papers)
        else:
            logging.info("No new papers found.")

    def schedule_task(self, search_params, interval_minutes=10, max_results=10):
        """
        Schedule a task to fetch papers at regular intervals.

        Args:
            search_params (dict): Search conditions (keywords, authors, etc.)
            interval_minutes (int): Interval in minutes
            max_results (int): Maximum number of results to fetch per run
        """
        schedule.every(interval_minutes).minutes.do(
            self.fetch_by_keywords, search_params=search_params, max_results=max_results)
        logging.info(
            f"Scheduled paper fetching every {interval_minutes} minutes. Conditions: {search_params}")
        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_daily_latest_task(self, time_str="06:00", max_results=10):
        """
        Schedule a task to fetch the latest papers daily at a specific time.

        Args:
            time_str (str): Time in HH:MM format
            max_results (int): Maximum number of results to fetch
        """
        schedule.every().day.at(time_str).do(self.fetch_by_keywords,
                                             search_params=None, max_results=max_results)
        logging.info(f"Scheduled daily paper fetching at {time_str}")
        while True:
            schedule.run_pending()
            time.sleep(1)

    @abstractmethod
    def fetch_papers(self, search_params=None, max_results=10):
        """Abstract method: Fetch papers based on search parameters. Must be implemented by subclasses."""
        pass
