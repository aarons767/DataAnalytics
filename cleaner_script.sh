#!/bin/bash


og_file="US-Gun-Violence.csv"
cleaned_file="cleaned_file.csv"


#removing duplicate rows
echo "Removing duplicate rows"
sort -u $file > nodupes.csv

#removing rows with missing column data
awk -F, '{
    if ($1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "" || $6 == "" || $7 == ""  ) 
        print $0 has missing value!";
	}' ./nodupes.csv







