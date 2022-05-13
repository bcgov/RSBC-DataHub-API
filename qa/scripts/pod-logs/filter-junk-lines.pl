#!/usr/bin/env perl

my $inside_exception=0;
my $line_number=0;

while (<>)
{
	$line++;
	
	# If this is a junk log line, do not print the warning or the stack trace
	if (/WARN  o.s.c.k.leader/ || /WARN  i.f.k.c.d.i.WatchConnectionManager/)
	{
		$inside_exception=1;  # Flag set when searching for exception end
		$subline=1;  # Counts number of lines in the current exception
		#print "\nException found on line $line: $_";
		while($inside_exception)
		{
		  	$_ = <>;
		  	#print(" " . $subline . ": " . $_);
		  	if (/Thread.java:748/)
		  	{
				$inside_exception=0;
		  	}
		  	$subline+=1;
		  	$line++;
		}
	}
	else
	{
		print $_;
	}
  
}
