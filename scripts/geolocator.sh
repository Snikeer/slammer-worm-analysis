#!/bin/bash

# Example: ./cymru_query.sh timestamp_slammer_2005_data.csv

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <timestamp_csv_file>"
    exit 1
fi

infile="$1"

# extracting year from the input file name 4 figits
year=$(echo "$infile" | grep -oE '[0-9]{4}' | head -n1)
if [ -z "$year" ]; then
    echo "Error: No year found in the file name."
    exit 1
fi
echo "Extracted year: $year"

# extraxting  uniq source IPs, skipping the header, and removing quotes from preveous made csv file for timestamps
tail -n +2 "$infile" | cut -d',' -f2 | sed 's/"//g' | sort | uniq > "ips_${year}.query"
echo "Unique IPs saved to ips_${year}.query"

# at the start incert "begin" and "verbose" to the file,and at the end append "end"
# temporary file to hold changes
sed -i '1i begin' "ips_${year}.query"
sed -i '2i verbose' "ips_${year}.query"
echo "end" >> "ips_${year}.query"
echo "Modified ips_${year}.query with query header and footer."

# pause for 3 seconds to ensure file modifications are complete, to make sure all is done before sending it to whois.cymru.com
sleep 3


# query the Cymru WHOIS server and save the output
cat "ips_${year}.query" | nc whois.cymru.com 43 > "enrich_${year}.cymru"
echo "Enriched WHOIS data saved to enrich_${year}.cymru"
