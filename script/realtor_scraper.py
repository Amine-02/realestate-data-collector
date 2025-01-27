import random
import requests
import statistics
from database.firebase_database import read_from_database, remove_from_database
from datetime import date
from interface.stats import Stats
from script.constants import (
    REALTOR_API_URL,
    HEADERS,
    BASE_SEARCH_PAYLOAD,
    PROXIES_SERVER_LIST,
    ALL_ZONES,
)
from playwright.sync_api import sync_playwright


def update_cookies():
    # Retrieve updated cookies using Playwright and update the HEADERS constant
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.realtor.ca")

        # Wait for the cookies to be set by the website
        page.wait_for_timeout(1000)

        # Collect cookies
        cookies = page.context.cookies()
        browser.close()

        # Convert cookies into a string for the Cookie header
        cookies_str = "; ".join(
            [f"{cookie['name']}={cookie['value']}" for cookie in cookies]
        )

        # Update the global HEADERS constant with the new Cookie value
        HEADERS["Cookie"] = cookies_str


def make_api_request(payload):
    # Make an API request using updated HEADERS
    response = requests.post(
        REALTOR_API_URL,
        headers=HEADERS,
        proxies=random.choice(PROXIES_SERVER_LIST),
        data=payload,
    )
    return response


def fetch_realtor_page(zone, current_page):

    # Step 1: Get the zone configuration
    zone_config = ALL_ZONES.get(zone)

    # Step 2: Prepare the payload
    payload = BASE_SEARCH_PAYLOAD.copy()
    payload.update(zone_config)
    payload["CurrentPage"] = current_page

    # Step 3: Make the API request
    response = make_api_request(payload)

    # Step 4: Process response if successful
    if response.status_code == 200:
        return response.json()
    else:
        return None


def compute_stats(zone):
    prices = []
    current_page = 1
    update_cookies()
    while True:
        data = fetch_realtor_page(zone, current_page)
        if data is None or not data["Results"]:
            break
        if data["Paging"]["CurrentPage"] > data["Paging"]["TotalPages"]:
            break
        if data["ErrorCode"]["Id"] != 200:
            break
        for result in data["Results"]:
            price = int(
                result["Property"]["Price"].split("$")[0].strip().replace("\xa0", "")
            )
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
            std_dev_price=0,
        )

    return Stats(
        date=date.today().isoformat(),
        count=len(prices),
        average_price=round(statistics.mean(prices), 2),
        median_price=statistics.median(prices),
        min_price=min(prices),
        max_price=max(prices),
        std_dev_price=round(statistics.stdev(prices), 2) if len(prices) > 1 else 0,
    )


def clean_up_data(zone):
    all_data = read_from_database(zone)
    if not all_data:
        print(f"No data found under '{zone}'.")
        return

    for child_key, child_value in all_data.items():
        if isinstance(child_value, dict):
            if child_value.get("count") == 0:
                delete_path = f"{zone}/{child_key}"
                remove_from_database(delete_path)
                print(f"Deleted '{delete_path}' because count=0.")
