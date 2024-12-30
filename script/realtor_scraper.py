import requests

def get_realtor_page(current_page=1):
    url = "https://api2.realtor.ca/Listing.svc/PropertySearch_Post"

    #
    payload = {
        "ZoomLevel": "12",
        "LatitudeMax": "45.56454",
        "LongitudeMax": "-73.22756",
        "LatitudeMin": "45.42110",
        "LongitudeMin": "-73.60143",
        "CurrentPage": str(current_page),
        "Sort": "6-D",
        "GeoIds": "g20_f25fc9mj",
        "PropertyTypeGroupID": "1",
        "TransactionTypeId": "2",
        "PropertySearchTypeId": "0",
        "BuildingTypeId": "17",
        "Currency": "CAD",
        "IncludeHiddenListings": "false",
        "RecordsPerPage": "12",
        "ApplicationId": "1",
        "CultureId": "2",
        "Version": "7.0"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://www.realtor.ca/",
        "Origin": "https://www.realtor.ca",
        "Cookie": "visid_incap_2269415=iasRiu/PSECJvTHSO5phVsKY82UAAAAAQUIPAAAAAACL4Lf7uWrWNehiRPfakqwo; visid_incap_3157676=JHqFUrIHQuCfkJ18c60FvQk7cGcAAAAAQUIPAAAAAADVRhtFWiyeR/G/zQ84pnhU; reese84=3:lfYY8lcu1K3xviFMPuKMQg==:I2Xhn/qmZLoMEj5/EkWCFG4cFGwQsujWN5aeVDCjBShAtf3XD7dOkR2IJoIXSQBtEb1HCTPho2m0XVPB3AbwuYLG7YlJtqw1vkf+GrIh2ncBukICWxDgWXT1A8iEuLAs4uzQOJJI4ocwELEWAuQ1S37sFmj0oaUteayl/BPXdmcCigT6HD4RF3L2phYzV8bGlch3Tm519BRf/UWJTbbneKb0MztECaz7fy7AQJ8O4pL08V5RmfrRABBnLnq1pMVEed0Eyg8B6LZlRNgAHah4jG+CtjXefZl84hXzc3yeJlo+cOT4LRoRYVmu70hslIn5auNHRTDFpw+wNVFRXOSE7uVQZA6rFSNRQlBQDxG2AGWab0crxOzY0HS010jZajsczJc895+5kO3sLuIGNr2tUmbpfbvS/Y+VW/u1+HeVsWGDhbjUKBPpXLJ4MlN+kWfK97RDBlgMUYwEnnBfDkeFPw==:BJOybTV5dct6hwMH6sv8iD0Rn742GpAFRT2Be2MCepQ=; visid_incap_3057435=/EuahJPqTn6pDVXpuWUiEQs7cGcAAAAAQUIPAAAAAAAFBbgoQvdrM4gYjkyTqlOQ; gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko=gigya-pr_ver4; visid_incap_2271082=byPWFLYGSV6aCktpYrBEIhI7cGcAAAAAQUIPAAAAAADfXSeMVjvzQvAaMiETXMu/; incap_ses_191_2269415=ps6YLYexxkZK0N04sJGmAgU7cGcAAAAAiZzyZITwUKwcWYoBUVNkdQ==; nlbi_2269415=VTcgOAXY+2XC+pZiCcuCgwAAAAB9wdiqi/y1P6Pu9osidWHU; incap_ses_1848_2269415=3KBOMem/nCYq5Ou0UWqlGTe1cGcAAAAA2Ks0ia21FAlydNYwcrkjIQ==; incap_ses_1848_3157676=gtlGfoII/1A4vq6zUWqlGU1YcGcAAAAA3spEjmVN9xAFqGXdO/mi6w==; nlbi_2269415_2147483392=SJL5SSabYQRXpwi1CcuCgwAAAABkXMXf29ekbHABs0i0UjGO; nlbi_3057435=hlkdMUpfLz+gBQpCoWGLxgAAAACaZwTtBp5YJOQ2iIeQq9Gk; incap_ses_1848_3057435=5xxuEN/FpSg4TECzUWqlGQs7cGcAAAAAXHYltBQpLAhAhcxWtfiXCQ==; nlbi_2271082=+PgcIN2jWEG+jyIdVPrQ3QAAAAABOEkbshcP8kBvRbHRIGrq; incap_ses_1848_2271082=R/z2AQ3bMw7BZoyzUWqlGRJPcGcAAAAAlSneydx2vM5j6OyobzsvUg==; incap_ses_1228_2269415=WRmXHCzDvhH4Xttlr7sKEY4gcmcAAAAAKdDNWo3LOnPffU2e+JPGuQ==; incap_ses_1228_3157676=2CcpJfoeWl9EYNtlr7sKEZAgcmcAAAAAn95GvDpBtSnSXZDsh/n2tQ==; incap_ses_1228_2271082=40nLRmG44BzRZNtlr7sKEZUgcmcAAAAAIBjhFY7jaUpy+IcSGLPLOw=="
    }

    response = requests.post(url, data=payload, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status {response.status_code}")
        return None

# Example usage:
if __name__ == "__main__":
    # Get page 1
    data_page_1 = get_realtor_page(current_page=1)
    if data_page_1:
        print("Page 1 data:", data_page_1)