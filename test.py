#curl 'https://support.binance.com/hc/sitemap.xml' -H 'Pragma: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: no-cache' --compressed
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import time
from twilio.rest import Client
import json

account = "AC17d4025699b733bf6a9921747a36241c"
token = "f1d9c1c08db17aee7430dfa4145ba4e4"
client = Client(account, token)

def get_sitemap(url):
    headers = {
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
    }

    get_url = requests.get(url, headers=headers)

    if get_url.status_code == 200:
        return get_url.text
    else:
        print('Unable to fetch sitemap: %s.' % url)

def get_new_coin(results, previous_results):
    for new_coin, old_coin in zip(sorted(results), sorted(previous_results)):
        if new_coin != old_coin:
            return new_coin

def get_fee_structure():
    headers = {
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
    }
    url = 'https://www.binance.com/assetWithdraw/getAllAsset.html'
    get_url = requests.get(url, headers=headers)
    json_data = json.loads(get_url.text)
    results = []
    for data in json_data:
        results.append(data["assetCode"])
    return results

def main():
    previous_count = 0
    previous_results = ["a","b"]
    while(1):
        results = get_fee_structure()
        if len(results) != previous_count:
            new_coin = get_new_coin(results, previous_results)
            print(new_coin)
            #print(new_coin)
            #message = client.messages.create(to="+6586150790", from_="+19092662529",
            #                                 body="New Coin Launching: " + new_coin)
            #time.sleep(30)
            #message = client.messages.create(to="+6586150790", from_="+19092662529",
            #                                 body="New Coin Launching: " + new_coin)

        else:
            print("Same")
            time.sleep(5)
            continue
        previous_count = len(results)
        previous_result = results


if __name__ == '__main__':
    main()
