#!/usr/bin/python3

import urllib.request

AUCTION_FILENAME = 'auction.json'
AUCTION_SERV_URL = "http://localhost:8800"
# AUCTION_SERV_URL = "http://lig-serv-tdcge.imag.fr/auction"


with open(AUCTION_FILENAME, 'r') as auction_file:
    auction_desc = auction_file.read()

    req = urllib.request.Request(f'{AUCTION_SERV_URL}/competitions',
                                 headers={'Content-type': 'application/json'},
                                 data=auction_desc.encode('utf-8'))
    res = urllib.request.urlopen(req)
    htmldoc = res.read().decode('utf-8')
    print(htmldoc)

