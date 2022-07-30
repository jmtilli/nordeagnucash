# Nordea-GnuCash

Nordea-GnuCash is a set of scripts to process portfolio exports obtained from
Nordea Investor. You can export a portfolio from Nordea Investor by going to
`My Portfolio` in the upper menu and then down below in the opened page
clicking `Export To Excel`.

You need to use Excel to convert that file to CSV. If you store it to
`~/vboxshared/nordeaexport.csv`, and have this repository cloned to
`~/nordeagnucash` and have made directories `~/nordeagnucash/nordeaexport`,
`~/nordeagnucash/portfolios`, `~/nordeagnucash/prices`, then all you need to do
is to run:
```
~/nordeagnucash/get.sh
```

It will populate the price and portfolio dumps.

Eventually, the intention is to create scripts to import these price dumps to
GnuCash, and create scripts to compare historial GnuCash portfolio states to
these Nordea portfolio dumps to ensure that GnuCash stock ownership history is
correct.
