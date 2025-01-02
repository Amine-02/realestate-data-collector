import requests
import time
import statistics
from datetime import date
from interface.stats import Stats
from script.constants import REALTOR_API_URL, HEADERS, BASE_SEARCH_PAYLOAD, ALL_ZONES

def fetch_realtor_page(zone, current_page):
    zone_config = ALL_ZONES.get(zone)
    payload = BASE_SEARCH_PAYLOAD.copy()
    payload.update(zone_config)
    payload["CurrentPage"] = current_page
    
    # Add more browser-like headers
    browser_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.realtor.ca',
        'Referer': 'https://www.realtor.ca/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        **HEADERS  # Keep any existing important headers
    }
    
    time.sleep(2)
    
    response = requests.post(REALTOR_API_URL, json=payload, headers=browser_headers)  # Note: changed data to json
    print(f"Response status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Response content: {response.text}")
        return None
        
    return response.json()

def compute_stats(zone):
    prices = []
    current_page = 1
    while True:
        data = fetch_realtor_page(zone, current_page)
        if data is None:
            print(f"No data received for zone {zone} on page {current_page}")
            break
        if data["Paging"]["CurrentPage"] > data["Paging"]["TotalPages"]:
            break
        if data["ErrorCode"]["Id"] != 200:
            break
        for result in data["Results"]:
            price = int(result["Property"]["Price"].split("$")[0].strip().replace("\xa0", ""))
            prices.append(price)
        current_page += 1
    
    if not prices:
        return Stats(
            date=date.today().isoformat(),
            count=0,
            average_price=0,
            median_price=0,
            min_price=0,
            max_price=0,
            std_dev_price=0
        )

    return Stats(
        date=date.today().isoformat(),
        count=len(prices),
        average_price=round(statistics.mean(prices),2),
        median_price=statistics.median(prices),
        min_price=min(prices),
        max_price=max(prices),
        std_dev_price=round(statistics.stdev(prices),2) if len(prices) > 1 else 0
    )