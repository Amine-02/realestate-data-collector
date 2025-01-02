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
    print("::debug::Making request with payload: " + str(payload))  # Shows as debug in GH Actions
    time.sleep(2)
    response = requests.post(REALTOR_API_URL, data=payload, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("::error::Request failed with status: " + str(response.status_code))  # Shows as error in GH Actions
        print("::error::Response content: " + response.text)
        return None

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