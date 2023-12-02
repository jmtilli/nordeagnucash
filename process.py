#!/usr/bin/env python3
from __future__ import print_function
from __future__ import division
import os
import sys
import re
import csv
from decimal import Decimal
if len(sys.argv) != 2:
    assert False
yyyymmdd_pat = re.compile("^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$")
yyyymmdd=sys.argv[1]
if not re.match(yyyymmdd_pat, yyyymmdd):
    assert False
fnsrc=os.environ["HOME"]+"/nordeagnucash/nordeaexport/" + yyyymmdd + ".csv"
fndb=os.environ["HOME"]+"/nordeagnucash/database.txt"
fntgt=os.environ["HOME"]+"/nordeagnucash/prices/" + yyyymmdd + ".txt"
fnprt=os.environ["HOME"]+"/nordeagnucash/portfolios/" + yyyymmdd + ".txt"
fncur=os.environ["HOME"]+"/nordeagnucash/currencies/" + yyyymmdd + ".txt"
nda2gnu = {}
with open(fndb, "r") as f:
    for row in f.readlines():
        code,mktcode,curcode,gnuex,gnuticker,name=row.split(" ", 5)
        assert (code,mktcode,curcode) not in nda2gnu
        nda2gnu[(code,mktcode,curcode)] = (gnuex,gnuticker)
prices = {}
holdings = {}
currencyrates = {}
with open(fnsrc, "r") as f:
    csv_reader = csv.reader(f, delimiter=';')
    rows = []
    for row in csv_reader:
        rows.append(row)
    mapping={}
    for idx in range(len(rows[1])):
        mapping[rows[1][idx]] = idx
    version = 1
    for required in ['Type','ISIN','MIC','CURRENCY','NAME','AMOUNT','PRICE','FX']:
        if required not in mapping:
            print("Field %s not found" % (required,))
            assert False
    #if rows[1][:18] == ['Type', 'AccountKey', 'Display Name', 'POA', 'FREE/PENSION', 'MARKETVALUE', 'UNREALIZEDPROFITLOSS', 'ISIN', 'MIC', 'CURRENCY', 'NAME', 'AMOUNT', 'PRICE', 'PRICETIME', 'CHANGE', 'CHANGEPCT', 'PRICEFACTOR', 'FX']:
    #    version = 1
    #else:
    #    print("---")
    #    for col in ['Type', 'AccountKey', 'Display Name', 'POA', 'FREE/PENSION', 'MARKETVALUE', 'UNREALIZEDPROFITLOSS', 'ISIN', 'MIC', 'CURRENCY', 'NAME', 'AMOUNT', 'PRICE', 'PRICETIME', 'CHANGE', 'CHANGEPCT', 'PRICEFACTOR', 'FX', '...']:
    #        print(col)
    #    print("---")
    #    for col in rows[1]:
    #        print(col)
    #    print("---")
    #    print("Unsupported version")
    #    assert False
    if version == 1:
        reached_end = False
        for row in rows[2:]:
            if row[0] == '' and row[1] == '' and row[2] == '' and row[3] == '' and row[4] == '':
                reached_end = True
                continue
            if reached_end:
                print("Invalid CSV")
                assert False
            if row[mapping['Type']] == "CashAccount":
                continue
            elif row[mapping['Type']] != "Custody":
                assert False
            security=row[mapping['ISIN']]
            market=row[mapping['MIC']]
            currency=row[mapping['CURRENCY']]
            name=row[mapping['NAME']]
            cnt=int(row[mapping['AMOUNT']])
            price=Decimal(row[mapping['PRICE']].replace(',', '.'))
            currencyrate=Decimal(row[mapping['FX']].replace(',', '.'))
            if market == 'XHEL':
                assert currency == 'EUR'
            elif market == 'XNYS':
                assert currency == 'USD'
            elif market == 'XSTO':
                assert currency == 'SEK'
            elif market == 'XNGS':
                assert currency == 'USD'
            elif market == 'XETR':
                assert currency == 'EUR'
            elif market == 'XPAR':
                assert currency == 'EUR'
            elif market == 'XOSL':
                assert currency == 'NOK'
            elif market == 'XAMS':
                assert currency == 'EUR'
            elif market == 'MTAA':
                assert currency == 'EUR'
            elif market == 'XSWX':
                assert currency == 'CHF'
            elif market == 'XLON':
                assert currency == 'GBX'
            elif market == 'XCSE':
                assert currency == 'DKK'
            elif market == 'SSME':
                assert currency == 'SEK'
            elif market == 'FSME':
                assert currency == 'EUR'
            elif market == 'XXXX':
                print("Warning, unsupported XXXX market")
                continue
            else:
                print("Unsupported market: " + market)
                assert False
            if currency == 'GBX':
                currency = 'GBP'
                price = price / 100
                currencyrate = currencyrate * 100
            assert currency in ["CAD", "CHF", "DKK", "EUR", "GBP", "NOK", "SEK", "USD"]
            if currency != "EUR":
                if currency not in currencyrates:
                    currencyrates[currency] = currencyrate
                assert currencyrates[currency] == currencyrate
            gnuex,gnuticker = nda2gnu[(security,market,currency)]
            prices[(gnuex,gnuticker)] = (str(price),currency)
            holdings[(gnuex,gnuticker)] = cnt
with open(fntgt, "w") as f:
    for key in sorted(prices.keys()):
        gnuex, gnuticker = key
        price, currency = prices[key]
        f.write("%s %s %s %s\n" % (gnuex, gnuticker, price, currency))
with open(fnprt, "w") as f:
    for key in sorted(holdings.keys()):
        gnuex, gnuticker = key
        cnt = holdings[key]
        f.write("%s %s %d\n" % (gnuex, gnuticker, cnt))
with open(fncur, "w") as f:
    for currency in sorted(currencyrates.keys()):
        rate = currencyrates[currency]
        f.write("%s %s\n" % (currency, rate))
