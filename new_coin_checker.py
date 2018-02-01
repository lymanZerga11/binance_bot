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
    result = ""
    try:
        get_url = requests.get(url, headers=headers, timeout=10)
        if get_url.status_code == 200:
            result = get_url.text
        else:
            print('Unable to fetch sitemap: %s.' % url)
    except:
        s = "Sitemap Request Failed.."
    return result

def process_sitemap(s):
    soup = BeautifulSoup(s, "html5lib")
    result = []

    for loc in soup.findAll('loc'):
        match = re.search('^https://support.binance.com/hc/en-us/articles/\d+-[A-Za-z0-9]+-([A-Z0-9]+)-$', loc.text)
        if match:
            result.append(match.group(1))
    return result


def is_sub_sitemap(s):
    if s.endswith('.xml') and 'sitemap' in s:
        return True
    else:
        return False


def parse_sitemap(s):
    sitemap = process_sitemap(s)
    result = []

    while sitemap:
        candidate = sitemap.pop()

        if is_sub_sitemap(candidate):
            sub_sitemap = get_sitemap(candidate)
            for i in process_sitemap(sub_sitemap):
                sitemap.append(i)
        else:
            result.append(candidate)

    return result

def get_fee_structure():
    headers = {
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
    }
    url = 'https://www.binance.com/assetWithdraw/getAllAsset.html'
    results = []
    try:
        get_url = requests.get(url, headers=headers, timeout=10)
        json_data = json.loads(get_url.text)
        for data in json_data:
            results.append(data["assetCode"])
    except:
        s = "Fee Request Failed.."
    return results

def get_new_coin(results, previous_results):
    for new_coin, old_coin in zip(sorted(results), sorted(previous_results)):
        if new_coin != old_coin:
            return new_coin

def main():
    previous_sitemap_results = ["a","b"]
    previous_fee_results = ["a","b"]
    count = 0
    while(1):
        sitemap = get_sitemap('https://support.binance.com/hc/sitemap.xml')
        sitemap_results = parse_sitemap(sitemap)
        fee_results = get_fee_structure()

        # print(sitemap_results)
        # print(fee_results)
        if len(sitemap_results) != len(previous_sitemap_results):
            if len(sitemap_results) and len(previous_sitemap_results):
                new_coin = get_new_coin(sitemap_results, previous_sitemap_results)
                # print(new_coin)
                message = client.messages.create(to="+6586150790", from_="+19092662529",
                                                 body="New Coin Launching: " + new_coin)
                time.sleep(20)
                message = client.messages.create(to="+6586150790", from_="+19092662529",
                                                 body="New Coin Launching: " + new_coin)

        if  len(fee_results) != len(previous_fee_results):
            if  len(fee_results) and len(previous_fee_results):
                new_coin = get_new_coin(fee_results, previous_fee_results)
                # print(new_coin)
                message = client.messages.create(to="+6586150790", from_="+19092662529",
                                                 body="New Coin Launching: " + new_coin)
                time.sleep(20)
                message = client.messages.create(to="+6586150790", from_="+19092662529",
                                                 body="New Coin Launching: " + new_coin)
        else:
            # print("Same")
            time.sleep(5)
        previous_fee_results = fee_results
        previous_sitemap_results = sitemap_results
        count = count + 1


if __name__ == '__main__':
    main()
