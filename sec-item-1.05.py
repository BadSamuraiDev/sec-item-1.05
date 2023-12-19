import sys
import os
import getpass
import requests
import yaml
import argparse
import json


def main():
    args = parse_arguments()

    if args.readme:
      with open('README.md', 'r') as readme_file:
          print(readme_file.read())
      sys.exit(0)

    api_token = args.token or getpass.getpass("SEC API token: ")

    if args.debug:
        print("Debug mode is enabled")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.watchlist is not None:
      try :
        watchlist_file_path = os.path.join(script_dir, args.watchlist)
      except Exception as e:
        print(f"Error parsing watchlist path: {e}")
        sys.exit(1)
    else:
      watchlist_file_path = os.path.join(script_dir, 'watchlist.yaml')

    wl = load_watchlist(watchlist_file_path)

    if args.debug:
        for company in wl['company']:
            print(f"{company['name']} ({company['ticker']})")

    watchlist_tickers = {company['ticker'] for company in wl['company']}
    response_data = get_api_response(api_token, args.debug)

    match_results = find_ticker_matches(response_data, watchlist_tickers)

    if args.debug:
        print(json.dumps(match_results, indent=2))

    if args.output:
      try:
          output_path = os.path.join(script_dir, args.output)
      except Exception as e:
          print(f"Error parsing output path: {e}")
          sys.exit(1)
      
      write_output(output_path, match_results)

def parse_arguments():
    parser = argparse.ArgumentParser(description='''
      SEC API Query Tool: This script interacts with the SEC API to fetch 8-K 
      filings related to Item 1.05 and Cybersecurity Incident disclosures.
      Users can query and match results against a watchlist of company tikers.
      For more detailed documentation, please run with --readme.
      ''')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--token', nargs='?', help='SEC API token')
    parser.add_argument('--watchlist', nargs='?', help='Watchlist path')
    parser.add_argument('--output', nargs='?', help='Output JSON path')
    parser.add_argument('--readme', action='store_true', help='Display README.me contents')
    return parser.parse_args()

def load_watchlist(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("The file watchlist.yaml was not found.")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}")
        sys.exit(1)

def get_api_response(api_token, debug):
  url = 'https://api.sec-api.io/full-text-search?'
  headers = {'Content-Type': 'application/json', 'Authorization': api_token}
  # "Item 1.05" requires special handling due to the non-breaking space character
  body = {
    "query": "\"item\u00a01\u002e05\" OR \"item&#160;1.05\" OR \"item&nbsp;1.05\"",
    "formTypes": ["8-K"]
  }

  if api_token:
    response = requests.post(url, headers=headers, json=body)
    return response.json() if debug else response.json()
  else:
    print("No API token provided. Using sample response.")
    with open('sample.json', 'r') as file:
      return json.loads(file.read())

def find_ticker_matches(response_data, watchlist_tickers):
  matches = []
  for filing in response_data['filings']:
    if filing['ticker'] in watchlist_tickers:
      print(f"Match found: {filing['companyNameLong']} - {filing['filedAt']} - {filing['filingUrl']}")
      matches.append({
        'ticker': filing['ticker'],
        'companyNameLong': filing['companyNameLong'],
        'filedAt': filing['filedAt'],
        'filingUrl': filing['filingUrl']
      })
  return matches

def write_output(output_path, match_results):
  try:
    with open(output_path, 'w') as file:
      json.dump(match_results, file, indent=2)
      print(f"Output written to {output_path}")
  except Exception as e:
    print(f"Error writing output: {e}")
    sys.exit(1)

if __name__ == '__main__':
  main()
