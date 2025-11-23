import requests
import json
import csv
import time
from typing import List, Dict

def scrape_startupbase_api(
    base_url: str = "https://startupbase.uz/api/startups/",
    limit: int = 8,
    location: str = "all",
    delay: float = 0.5
) -> List[Dict]:
    """
    Scrape all startups from the StartupBase.uz API using pagination.

    Args:
        base_url: The API endpoint URL
        limit: Number of items per page
        location: Location filter
        delay: Delay between requests in seconds (to be respectful)

    Returns:
        List of all startup dictionaries
    """
    all_startups = []
    offset = 0
    total_count = None

    # Headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'Referer': 'https://startupbase.uz/en/startups',
    }

    print(f"Starting to scrape startups from {base_url}")

    while True:
        # Build request parameters
        params = {
            'limit': limit,
            'location': location,
            'offset': offset
        }

        try:
            # Make the request
            print(f"Fetching offset {offset}...", end=" ")
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()

            # Get total count on first request
            if total_count is None:
                total_count = data.get('count', 0)
                print(f"\nTotal startups to fetch: {total_count}")

            # Extract results
            results = data.get('results', [])
            if not results:
                print("No more results found.")
                break

            all_startups.extend(results)
            print(f"Got {len(results)} startups (Total collected: {len(all_startups)}/{total_count})")

            # Check if we've reached the end
            if data.get('next') is None or len(all_startups) >= total_count:
                print("Reached the end of pagination.")
                break

            # Move to next page
            offset += limit

            # Be respectful with delay between requests
            time.sleep(delay)

        except requests.exceptions.RequestException as e:
            print(f"\nError fetching data at offset {offset}: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"\nError parsing JSON at offset {offset}: {e}")
            break

    print(f"\nScraping complete! Total startups collected: {len(all_startups)}")
    return all_startups


def save_to_csv(data: List[Dict], filename: str = "startups_data.csv"):
    """Save the scraped data to a CSV file."""
    if not data:
        print("No data to save.")
        return

    # Flatten the nested data structure
    flattened_data = []
    for startup in data:
        row = {
            'id': startup.get('id'),
            'name': startup.get('name'),
            'logo': startup.get('logo'),
            'image': startup.get('image'),
            'short_description': startup.get('short_description'),
            'description': startup.get('description'),
            'industry_id': startup.get('industry', {}).get('id') if startup.get('industry') else None,
            'industry_name': startup.get('industry', {}).get('name') if startup.get('industry') else None,
            'stage': startup.get('stage'),
            'region_id': startup.get('region', {}).get('id') if startup.get('region') else None,
            'region_name': startup.get('region', {}).get('name') if startup.get('region') else None,
            'region_country': startup.get('region', {}).get('county') if startup.get('region') else None,
            'region_lat': startup.get('region', {}).get('lat') if startup.get('region') else None,
            'region_long': startup.get('region', {}).get('long') if startup.get('region') else None,
            'is_verified': startup.get('is_verified'),
            'digital_startup_awards_participant': startup.get('digital_startup_awards_participant'),
            'is_member': startup.get('is_member'),
            'tech_awards_winner': startup.get('tech_awards_winner')
        }
        flattened_data.append(row)

    # Write to CSV
    fieldnames = flattened_data[0].keys()
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)

    print(f"Data saved to {filename}")


def save_to_json(data: List[Dict], filename: str = "startups_data.json"):
    """Save the scraped data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'total_count': len(data),
            'startups': data
        }, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {filename}")


def main():
    """Main function to run the scraper."""
    print("=" * 60)
    print("StartupBase.uz API Scraper")
    print("=" * 60)

    # Scrape the data
    startups = scrape_startupbase_api()

    if startups:
        # Save to CSV and JSON files
        save_to_csv(startups)
        save_to_json(startups)

        # Print some statistics
        print("\n" + "=" * 60)
        print("Statistics:")
        print("=" * 60)
        print(f"Total startups: {len(startups)}")

        # Count by stage
        stages = {}
        for startup in startups:
            stage = startup.get('stage', 'Unknown')
            stages[stage] = stages.get(stage, 0) + 1

        print("\nStartups by stage:")
        for stage, count in sorted(stages.items(), key=lambda x: x[1], reverse=True):
            print(f"  {stage}: {count}")

        # Count by industry
        industries = {}
        for startup in startups:
            industry = startup.get('industry', {})
            if industry:
                industry_name = industry.get('name', 'Unknown')
                industries[industry_name] = industries.get(industry_name, 0) + 1

        print("\nTop 10 industries:")
        for industry, count in sorted(industries.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {industry}: {count}")
    else:
        print("No data was scraped.")


if __name__ == "__main__":
    main()
