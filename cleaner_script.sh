#!/bin/bash


og_file="US-Gun-Violence.csv"
cleaned_file="cleaned_file.csv"
no_missing="no_missing.csv"
normalized_file="normalized.csv"


#removing duplicate rows
echo "Removing duplicate rows"
awk -F, 'NR == 1 { print; next } !seen[$0]++' $og_file > $cleaned_file



echo "Removing rows with missing column data"
awk -F ',' '{
    # Check if any of the fields are empty
  #  error_txt="";

   # if ($1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "") {
    #    # Use system to print the entire line to stderr or stdout
   #     error_txt=error_txt "Empty data in line: ";
  #  }

    #Normalized invalid fields to N/A
    if ($5 ~ /^[0-9]+$/) {
	    $5 = "N/A"
    }

    if ($6 == "" || $7 == "") {
   #     error_txt = error_txt " Killing or injured field is empty: ";
	next;
    }

    print $0;  # Print the line to the output file if no fields are missing
}' $cleaned_file > $no_missing


awk -F, -v OFS=, 'BEGIN {
    # Create an array to map month names to numbers
    split("January Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec", monthNames, " ");
    for (i in monthNames) monthIndex[monthNames[i]] = i;
}
{
    if (NR == 1) {
        print $0;  # Print the header as is
    } else {
        # Split the date in the second column into components
        n = split($2, dateParts, " ");
        # Map the month name to a number
        month = sprintf("%02d", monthIndex[dateParts[1]]);
        # Remove possible comma from day part and ensure two digits
        day = sprintf("%02d", dateParts[2]+0);
        year = dateParts[3];  # Year is taken directly
        
        # Reformat the date into MM-DD-YYYY
        $2 = month "-" day "-" year;
        print $0;  # Print the modified line
    }
}' $no_missing  > $normalized_file
