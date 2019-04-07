import os
import pandas as pd
 
def getTickers():
	os.system("curl --ftp-ssl anonymous:jupi@jupi.com "
	          "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt "
	          "> nasdaq.lst")

	os.system("awk ' NR > 32 {print $1}'  nasdaq.lst2 > nasdaq.csv")
	os.system("echo; head nasdaq.csv; echo '...'; tail nasdaq.csv")