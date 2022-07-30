# Nordea-GnuCash

Nordea-GnuCash is a set of scripts to process portfolio exports obtained from
Nordea Investor. You can export a portfolio from Nordea Investor by going to
`My Portfolio` in the upper menu and then down below in the opened page
clicking `Export To Excel`.

You need to use Excel to convert that file to CSV. If you store it to
`~/vboxshared/nordeaexport.csv`, and have this repository cloned to
`~/nordeagnucash` and have made directories `~/nordeagnucash/nordeaexport`,
`~/nordeagnucash/portfolios`, `~/nordeagnucash/prices`,
`~/nordeagnucash/currencies` then all you need to do is to run:
```
~/nordeagnucash/get.sh
```

It will populate the price and portfolio dumps.

Eventually, the intention is to create scripts to import these price dumps to
GnuCash, and create scripts to compare historial GnuCash portfolio states to
these Nordea portfolio dumps to ensure that GnuCash stock ownership history is
correct.

## How to start GnuCash in a manner that automatically uses the database

Create a file `~/.local/bin/gnucash` with contents:
```
#!/bin/sh
export FQ_LOAD_QUOTELET=NordeaGnuCash
export PERL5LIB=$HOME/nordeagnucash
echo "Set custom Finance::Quote module list"
/usr/bin/gnucash
```

Then add execution permissions to that file.

Now you should be able to automatically get quotes into GnuCash.
