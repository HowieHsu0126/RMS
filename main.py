import argparse
import json
import time

from paper_fetcher.arxiv_fetcher import ArXivFetcher
from paper_fetcher.google_scholar_fetcher import GoogleScholarFetcher
from paper_fetcher.pubmed_fetcher import PubMedFetcher
from paper_fetcher.utils import setup_logging


def main():
    setup_logging()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Fetch academic papers and optionally save or display results in JSON format."
    )
    parser.add_argument(
        "--platform",
        type=str,
        default="pubmed",
        choices=["pubmed"],
        help="The platform to fetch papers from. Options: 'pubmed', 'arxiv', 'google_scholar'. Default is 'pubmed'.",
    )
    parser.add_argument(
        "--json_file_name",
        type=str,
        default=f"papers_{int(time.time())}.json",
        help="The name of the JSON file to save the fetched papers.",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default="machine learning",
        help="Keyword to search for papers.",
    )
    parser.add_argument(
        "--author",
        type=str,
        default="",
        help="Author name to search for papers.",
    )
    parser.add_argument(
        "--journal",
        type=str,
        default="",
        help="Journal name to search for papers.",
    )
    parser.add_argument(
        "--year",
        type=str,
        default="",
        help="Year of publication to search for papers.",
    )
    parser.add_argument(
        "--max_results",
        type=int,
        default=10,
        help="Maximum number of papers to fetch.",
    )
    parser.add_argument(
        "--output_json",
        action="store_true",
        help="If set, outputs the fetched papers as JSON to the console instead of saving to a file.",
    )

    args = parser.parse_args()

    # Select fetcher based on platform
    if args.platform == "pubmed":
        fetcher = PubMedFetcher(json_file_name=args.json_file_name)
    elif args.platform == "arxiv":
        fetcher = ArXivFetcher(json_file_name=args.json_file_name)
    elif args.platform == "google_scholar":
        fetcher = GoogleScholarFetcher(json_file_name=args.json_file_name)
    else:
        raise ValueError(f"Unsupported platform: {args.platform}")

    # Set search parameters from command line arguments
    search_params = {
        "keyword": args.keyword,
        "author": args.author,
        "journal": args.journal,
        "year": args.year,
    }

    if args.output_json:
        # Fetch papers and print JSON to console
        result_json = fetcher.fetch_by_keywords_and_return_json(
            search_params=search_params, max_results=args.max_results
        )
        print(result_json)
    else:
        # Fetch papers and save to file
        fetcher.run(
            search_params=search_params,
            max_results=args.max_results,
        )


if __name__ == "__main__":
    main()
