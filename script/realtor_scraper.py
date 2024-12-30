import requests
from constants import REALTOR_API_URL, HEADERS, BASE_SEARCH_PAYLOAD, ZONES


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

def fetch_realtor_data(zone):
    current_page = 1
    while True:
        data = fetch_realtor_page(zone, current_page)
        if data["Paging"]["CurrentPage"] > data["Paging"]["TotalPages"]:
            break
        if data["ErrorCode"]["Id"] != 200:
            break
        for result in data["Results"]:
            print(result["Id"], result["Property"]["Price"].split("$")[0].strip())
        current_page += 1


if __name__ == "__main__":
    fetch_realtor_data("saint-hubert")
