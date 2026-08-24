# TrendPulse — Task 1: Data Collection

Fetches the top 500 trending stories from the HackerNews API, categorizes them into
technology, worldnews, sports, science, or entertainment based on keyword matching
in the title, and saves the results as a JSON file.

## How it works
1. Fetch top story IDs from `https://hacker-news.firebaseio.com/v0/topstories.json`
2. For each category, scan the IDs, fetch each story's details, and keep matching
   ones (up to 25 per category)
3. Save the combined results to `data/trends_YYYYMMDD.json`
