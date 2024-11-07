# main.py
from paper_fetcher.pubmed_fetcher import PubMedFetcher
from paper_fetcher.utils import setup_logging
import time
import argparse

def main():
    setup_logging()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Fetch academic papers based on search parameters.")
    parser.add_argument("--json_file_name", type=str, default=f"papers_{int(time.time())}.json", help="The name of the JSON file to save the fetched papers.")
    parser.add_argument("--keyword", type=str, default="cancer", help="Keyword to search for papers.")
    parser.add_argument("--author", type=str, default="", help="Author name to search for papers.")
    parser.add_argument("--journal", type=str, default="", help="Journal name to search for papers.")
    parser.add_argument("--year", type=str, default="", help="Year of publication to search for papers.")
    parser.add_argument("--max_results", type=int, default=10, help="Maximum number of papers to fetch.")

    args = parser.parse_args()

    # Create PubMedFetcher instance with provided JSON file name
    pm_fetcher = PubMedFetcher(json_file_name=args.json_file_name)
    
    # Set search parameters from command line arguments
    search_params_pm = {
        "keyword": args.keyword,
        "author": args.author,
        "journal": args.journal,
        "year": args.year
    }
    
    # Run the fetcher with the provided parameters
    pm_fetcher.run(args.json_file_name, search_params_pm, max_results=args.max_results)

if __name__ == "__main__":
    main()
