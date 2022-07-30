#!/usr/bin/env python2
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
fntgt=os.environ["HOME"]+"/nordeagnucash/processed/" + yyyymmdd + ".txt"
nda2gnu = {}
with open(fndb, "r") as f:
    for row in f.readlines():
        code,mktcode,curcode,gnuex,gnuticker,name=row.split(" ", 5)
        assert (code,mktcode,curcode) not in nda2gnu
        nda2gnu[(code,mktcode,curcode)] = (gnuex,gnuticker)
prices = {}
with open(fnsrc, "r") as f:
    csv_reader = csv.reader(f, delimiter=';')
    rows = []
    for row in csv_reader:
        rows.append(row)
    if rows[1] == ['Type', 'AccountKey', 'Display Name', 'POA', 'FREE/PENSION', 'MARKETVALUE', 'UNREALIZEDPROFITLOSS', 'ISIN', 'MIC', 'CURRENCY', 'NAME', 'AMOUNT', 'PRICE', 'PRICETIME', 'CHANGE', 'CHANGEPCT', 'PRICEFACTOR', 'FX', 'A.PRICE', 'VALUE', 'VALUE_BASE', 'BASECURRENCY', 'MARKETVALUE_DEVELOPMENT', 'MARKETVALUE_DEVELOPMENT_TODAY', 'INCOMPLETE_DATA', 'INCOMPLETE_DATA_MARKETVALUE', 'INCOMPLETE_DATA_PROFITLOSS']:
        version = 1
    else:
        print "Unsupported version"
        assert False
    if version == 1:
        reached_end = False
        for row in rows[2:]:
            if row[0] == '' and row[1] == '' and row[2] == '' and row[3] == '' and row[4] == '':
                reached_end = True
                continue
            if reached_end:
                print "Invalid CSV"
                assert False
            if row[0] == "CashAccount":
                continue
            elif row[0] != "Custody":
                assert False
            security=row[7]
            market=row[8]
            currency=row[9]
            name=row[10]
            price=Decimal(row[12].replace(',', '.'))
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
            else:
                print "Unsupported market: " + market
                assert False
            if currency == 'GBX':
                currency = 'GBP'
                price = price / 100
            assert currency in ["CAD", "CHF", "DKK", "EUR", "GBP", "NOK", "SEK", "USD"]
            gnuex,gnuticker = nda2gnu[(security,market,currency)]
            prices[(gnuex,gnuticker)] = (str(price),currency)
with open(fntgt, "w") as f:
    for key in prices:
        gnuex, gnuticker = key
        price, currency = prices[key]
        f.write("%s %s %s %s\n" % (gnuex, gnuticker, price, currency))
