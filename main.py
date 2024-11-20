# main.py
from paper_fetcher.pubmed_fetcher import PubMedFetcher
from paper_fetcher.utils import setup_logging
import time
import argparse
import json


def main():
    setup_logging()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Fetch academic papers and optionally save or display results in JSON format."
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
        default="cancer",
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

    # Create PubMedFetcher instance with provided JSON file name
    pm_fetcher = PubMedFetcher(json_file_name=args.json_file_name)

    # Set search parameters from command line arguments
    search_params_pm = {
        "keyword": args.keyword,
        "author": args.author,
        "journal": args.journal,
        "year": args.year,
    }

    if args.output_json:
        # Fetch papers and print JSON to console
        result_json = pm_fetcher.fetch_by_keywords_and_return_json(
            search_params=search_params_pm, max_results=args.max_results
        )
        print(result_json)
    else:
        # Fetch papers and save to file
        pm_fetcher.run(
            search_params_pm,
            max_results=args.max_results,
        )


if __name__ == "__main__":
    main()
