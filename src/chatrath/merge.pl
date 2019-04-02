#!/usr/bin/perl -lw

use strict;

my @values = ();

open(LS,"ls *\.test\.json |");
while(<LS>){
    chomp;
    my $fileName = $_;
    my $content = "";
    open(IN,$fileName);
    while(<IN>){
        $content .= $_;
    }
    close(IN);
    $content =~ s/^\[//;
    $content =~ s/\]$//;
    push @values, $content;
}
close(LS);

my $all = join(",",@values);
$all =~ s/^,//;
$all =~ s/,$//;
$all = "[" . $all . "]";
print $all;
