#!/bin/bash


#og_file="US-Gun-Violence.csv"
#cleaned_file="cleaned_file.csv"
#no_missing="no_missing.csv"
#normalized_file="normalized.csv"



# Validate arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_file> <cleaned_file> <no_missing_file>"
    exit 1
fi

og_file=$1
cleaned_file=$2
no_missing=$3

# Check if input file exists
if [ ! -f "$og_file" ]; then
    echo "Error: Input file '$og_file' not found!"
    exit 1
fi


#removing duplicate rows
echo "Removing duplicate rows"
awk -F, 'NR == 1 { print; next } !seen[$0]++' $og_file > $cleaned_file



echo "Removing rows with missing column data"
awk -F ',' '{
    #Normalized invalid fields to N/A
    if ($5 ~ /^[0-9]+$/) {
	    $5 = "N/A"
    }
    if ($6 == "" || $7 == "") {
	next;
    }

    print $0;  # Print the line to the output file if no fields are missing
}' $cleaned_file > $no_missing

#Script to get rid of outliers 
#awk -F"," 'NR==1 || ($6 <= 50 && $7 <= 50)' "$no_missing" > normalized_nooutlier_clean.csv

