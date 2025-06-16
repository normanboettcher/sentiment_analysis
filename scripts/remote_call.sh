#!/bin/bash

set -euo pipefail

SCRIPT_PATH="/home/norman/Projekte/MachineLearning/sentiment_analysis/performance/src/remote_call_review.py"


function print_help() {
    cat << EOF
Usage: $(basename "$0")

Description:
    This script provides basic operations to perform your git add, commit and push activities.
    Additional steps such as mvn pmd checks are also available.
    You can customize the script with whatever you would like to add.

Options:
    -h, --help              Prints help for usage of parameters and script
    -n, --number            The number of reviews you want to send to the REST-API.
    -s, --sep               The separator or delimiter of the csv file,
    -f, --file              The actual csv-file which should be loaded

Examples:
    $(basename "$0") --number 5 --file ~/myproject/data.csv --sep ,
    $(basename "$0") --n 10 -f ~/myproject/data.csv -s ,

EOF
}

OPTS=$(getopt -o "n:f:s:h" -l "number:, file:, sep:, help" -- "$@")

if [[ $? -ne 0 ]]; then
  echo "Failed to parse options"
  exit 1
fi

eval set -- "$OPTS"

NUMBER=0
FILE=""
SEP=""
while true; do
  case "$1" in
  -n | --number)
    NUMBER="$2"
    shift 2
    ;;
  -f | --file)
    FILE="$2"
    shift 2
    ;;
  -s | --sep)
    SEP="$2"
    shift 2
    ;;
  -h | --help)
    print_help
    exit 0
    ;;
  --)
    shift
    break
    ;;
  *)
    echo "Unknown option: $1"
    exit 1
    ;;
  esac
done

echo "Starting script at $SCRIPT_PATH"
python "$SCRIPT_PATH" "$NUMBER" "$SEP" "$FILE"
exit 0