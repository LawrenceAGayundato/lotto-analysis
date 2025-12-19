"""Quick fetch script for testing"""
from fetch_pcso_data import PCSODataFetcher

fetcher = PCSODataFetcher()
print("Fetching last 7 days of PCSO data...")
results = fetcher.fetch_all_games(days_back=7)
fetcher.save_to_json(results)
print(f"\nFetched {len(results)} results")
