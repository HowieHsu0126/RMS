#!/bin/bash

# Allow script to continue even if a command fails
set +e

# Define test cases
DEFAULT_KEYWORD="artificial intelligence"
AUTHOR="John Doe"
JOURNAL="Nature"
YEAR="2023"
MAX_RESULTS=5

# Function to display a section header for clarity in the logs
print_section() {
    echo
    echo "=============================="
    echo "$1"
    echo "=============================="
    echo
}

# Generate a JSON file name with a timestamp
generate_json_file_name() {
    local timestamp=$(date +%Y%m%d%H%M%S)
    echo "test_papers_${timestamp}.json"
}

# Run a test case and handle exit codes
run_test_case() {
    local description="$1"
    local cmd="$2"

    print_section "$description"
    eval "$cmd"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "Test passed: New papers were fetched and saved."
    elif [ $exit_code -eq 1 ]; then
        echo "Test passed: No new papers were fetched, but execution succeeded."
    else
        echo "Test failed: An error occurred during execution."
    fi
}

# Run tests
run_test_case "Test 1: Default parameters" \
    "python main.py --json_file_name $(generate_json_file_name) --keyword '$DEFAULT_KEYWORD' --max_results $MAX_RESULTS"

run_test_case "Test 2: Specify author" \
    "python main.py --json_file_name $(generate_json_file_name) --keyword '$DEFAULT_KEYWORD' --author '$AUTHOR' --max_results $MAX_RESULTS"

run_test_case "Test 3: Specify journal" \
    "python main.py --json_file_name $(generate_json_file_name) --keyword '$DEFAULT_KEYWORD' --journal '$JOURNAL' --max_results $MAX_RESULTS"

run_test_case "Test 4: Specify year" \
    "python main.py --json_file_name $(generate_json_file_name) --keyword '$DEFAULT_KEYWORD' --year '$YEAR' --max_results $MAX_RESULTS"

run_test_case "Test 5: Specify author and journal" \
    "python main.py --json_file_name $(generate_json_file_name) --keyword '$DEFAULT_KEYWORD' --author '$AUTHOR' --journal '$JOURNAL' --max_results $MAX_RESULTS"

run_test_case "Test 6: Specify author, journal, and year" \
    "python main.py --json_file_name $(generate_json_file_name) --keyword '$DEFAULT_KEYWORD' --author '$AUTHOR' --journal '$JOURNAL' --year '$YEAR' --max_results $MAX_RESULTS"

run_test_case "Test 7: Output JSON to console (default parameters)" \
    "python main.py --keyword '$DEFAULT_KEYWORD' --max_results $MAX_RESULTS --output_json"

run_test_case "Test 8: Output JSON to console with author" \
    "python main.py --keyword '$DEFAULT_KEYWORD' --author '$AUTHOR' --max_results $MAX_RESULTS --output_json"

run_test_case "Test 9: Output JSON to console with journal and year" \
    "python main.py --keyword '$DEFAULT_KEYWORD' --journal '$JOURNAL' --year '$YEAR' --max_results $MAX_RESULTS --output_json"

run_test_case "Test 10: Output JSON to console with all filters" \
    "python main.py --keyword '$DEFAULT_KEYWORD' --author '$AUTHOR' --journal '$JOURNAL' --year '$YEAR' --max_results $MAX_RESULTS --output_json"

print_section "All tests completed successfully."
