import requests
from datetime import date
import statistics
from interface.stats import Stats
from script.constants import REALTOR_API_URL, HEADERS, BASE_SEARCH_PAYLOAD, ZONES

def fetch_realtor_page(zone, current_page):
    payload = BASE_SEARCH_PAYLOAD.copy()
    payload.update(ZONES[zone])
    payload["CurrentPage"] = current_page
    response = requests.post(REALTOR_API_URL, data=payload, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status {response.status_code}")
        return None

def compute_stats(zone):
    prices = []
    current_page = 1
    while True:
        data = fetch_realtor_page(zone, current_page)
        if data["Paging"]["CurrentPage"] > data["Paging"]["TotalPages"]:
            break
        if data["ErrorCode"]["Id"] != 200:
            break
        for result in data["Results"]:
            price = int(result["Property"]["Price"].split("$")[0].strip().replace("\xa0", ""))
            prices.append(price)
        current_page += 1

    date_str = date.today().isoformat()
    avg_price = round(statistics.mean(prices),2)
    median_price = statistics.median(prices)
    min_price = min(prices)
    max_price = max(prices)
    std_dev_price = round(statistics.stdev(prices),2) if len(prices) > 1 else 0
    return Stats(
        date=date_str,
        count=len(prices),
        average_price=avg_price,
        median_price=median_price,
        min_price=min_price,
        max_price=max_price,
        std_dev_price=std_dev_price
    )