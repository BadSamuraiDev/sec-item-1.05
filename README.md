# [![SEC Item 1.05 API Query](/sec-item-1.05.png)](https://github.com/BadSamuraiDev/sec-item-1.05)

This script queries the SEC API for filings with a "Item 1.05" in the full text search and matches tickers from a watchlist. Ideally this script would be run on an interval (mind the API limits!) against a list populated manually or by a 3rd party risk job.

By default the script will search between the current date and 30 days ago. This can be changed by modifying the `start_date` and `end_date` variables in the API body.

### Usage:
```
  python sec-item-1.05.py --token YOUR_API_TOKEN          # Run the script with an API token.
  python sec-item-1.05.py --debug --token YOUR_API_TOKEN  # Run the script in debug mode with an API token.
  python sec-item-1.05.py --debug                         # Run the script in debug mode, you'll be prompted for the API token.
  python sec-item-1.05.py --token YOUR_API_TOKEN --watchlist MY_WL.yaml --output MY_OUTPUT.json
```

### Options:
```
  --token     Provide the SEC API token. If omitted, the script will prompt for it.
  --debug     Enable debug mode for additional output useful for troubleshooting.
  --watchlist Provide a different watchlist file. If omitted, the script will use the default.
  --output    Provide a different output file. If omitted, the script will print to console.
  --help      Show this message and exit.
  --readme    Show the README and exit.
```

### Resources:
- [SEC API Documentation](https://sec-api.io/docs/full-text-search-api)
- [SEC Press Release](https://www.sec.gov/news/press-release/2023-139)
