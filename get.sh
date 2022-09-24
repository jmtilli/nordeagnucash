#!/bin/sh
set -e -u
SRC="$HOME/vboxshared/nordeaexport.csv"
SHASRC="`cat "$SRC"|sed '1s/^\xEF\xBB\xBF//'|sha1sum|cut -d' ' -f1`"
# Begins with 0xef 0xbb 0xbf
DATE="`cat "$SRC"|sed '1s/^\xEF\xBB\xBF//'|head -1|cut -d';' -f1|cut -d' ' -f1`"
DD="`echo "$DATE"|cut -d'.' -f1`"
MM="`echo "$DATE"|cut -d'.' -f2`"
YYYY="`echo "$DATE"|cut -d'.' -f3`"
echo "Date: $DATE"
case "$YYYY" in
	[0-9][0-9][0-9][0-9])
		;;
	*)
		echo "Invalid year in date"
		exit 1
		;;
esac
case "$MM" in
	[0-9][0-9])
		;;
	*)
		echo "Invalid month in date"
		exit 1
		;;
esac
case "$DD" in
	[0-9][0-9])
		;;
	[0-9])
		DD="0$DD"
		;;
	a)
		echo "Invalid month day in date: $DD"
		exit 1
		;;
esac
TGT="$HOME/nordeagnucash/nordeaexport/${YYYY}${MM}${DD}.csv"
if [ -e "$TGT" ]; then
	SHATGT="`sha1sum "$TGT"|cut -d' ' -f1`"
	if [ "$SHASRC" != "$SHATGT" ]; then
		echo "Copying, different"
		cat "$SRC"|sed '1s/^\xEF\xBB\xBF//' > "$TGT"
		python2 "$HOME/nordeagnucash/process.py" "${YYYY}${MM}${DD}" || (unlink "$TGT"; exit 1)
		echo "Enter these into GnuCash manually:"
		cat "$HOME/nordeagnucash/currencies/${YYYY}${MM}${DD}.txt"
	fi
else
	echo "Copying, nonexistent"
	cat "$SRC"|sed '1s/^\xEF\xBB\xBF//' > "$TGT"
	python2 "$HOME/nordeagnucash/process.py" "${YYYY}${MM}${DD}" || (unlink "$TGT"; exit 1)
	echo "Enter these into GnuCash manually:"
	cat "$HOME/nordeagnucash/currencies/${YYYY}${MM}${DD}.txt"
fi
echo OK
exit 0
