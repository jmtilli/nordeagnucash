#!/usr/bin/perl -w

package Finance::Quote::NordeaGnuCash;

require 5.005;

use strict;

our $VERSION = '0.01'; # VERSION

sub methods {
	return ( nordeagnucash => \&ngcget );
}

sub labels {
    my @labels =
        qw/currency last date symbol/;
    return ( ngcget => \@labels );
}


sub ngcget {
	my $quoter = shift;
	my @stocks = @_;
	my %info;

	my $home = $ENV{'HOME'};
	my $dirname = "$home/nordeagnucash/prices";
	my @files = glob "$dirname/*.txt";
	my @sorted = sort @files;
	my $last = $sorted[-1];
	$last =~ /.*\/([0-9]{4})([0-9]{2})([0-9]{2})\.txt/;
	my $yyyy = $1;
	my $mm = $2;
	my $dd = $3;
	my %pricedb;
	my %currencydb;
	open my $fh, '<', $last or die "Can't open $!";
	while(my $line = <$fh>)
	{
		chomp $line;
		my @linear = split / /, $line;
		$pricedb{$linear[1]} = $linear[2];
		$currencydb{$linear[1]} = $linear[3];
	}
	close $fh;

	foreach my $stock (@stocks) {
		if (defined $pricedb{$stock})
		{
			$quoter->store_date( \%info, $stock, { isodate => "$yyyy-$mm-$dd" } );
			$info{$stock,"symbol"} = $stock;
			$info{$stock,"success"} = 1;
			$info{$stock,"currency"} = $currencydb{$stock};
			$info{$stock,"last"} = $pricedb{$stock};
		}
		else
		{
			$info{$stock,"success"} = 0;
		}
	}

	return wantarray() ? %info : \%info;
};
