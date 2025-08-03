#!/usr/bin/env bash
#
# usage:
#   ./monthly_spliter.sh <PCAP_FILE> <YEAR>
# example:
#   ./monthly_spliter.sh ./2005-port1433-1444.cap 2005
#
# This script will attempt to create monthly PCAP files named e.g.:
#   2005-01-ports1433,1434.pcap
#   2005-02-ports1433,1434.pcap
#   ...
#   2005-12-ports1433,1434.pcap
#
# If a given month's file ends up with zero packets, it is removed,
# and a warning is printed at the end.
#

# reminder to use two arguments
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <PCAP_FILE> <YEAR>"
  echo "Example: $0 filiname/pahp yearnumber"
  exit 1
fi



PCAPFILE="$1"     # example  ./2005-port1433-1444.cap
YEAR="$2"         # example   2005

# extract base directory where the monthly files wil be saved
BASEDIR="$(dirname "$PCAPFILE")"

echo ""
echo "First packet in $PCAPFILE:"
tshark -nr "$PCAPFILE" -T fields -e frame.number -e frame.time 2>/dev/null | head -n 1

echo ""
echo "Last packet in $PCAPFILE:"
tshark -nr "$PCAPFILE" -T fields -e frame.number -e frame.time 2>/dev/null | tail -n 1



# leap years:
MONTH_DAYS=( "31" "28" "31" "30" "31" "30" "31" "31" "30" "31" "30" "31" )

# checking for leap year
if (( YEAR % 400 == 0 )) || { (( YEAR % 4 == 0 )) && (( YEAR % 100 != 0 )); }; then
  MONTH_DAYS[1]="29"  # February has 29 days in a leap year
fi

MONTH_NAMES=( "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" )

missing_months=()

# Loop over the 12 months
for i in "${!MONTH_NAMES[@]}"; do
  month="${MONTH_NAMES[$i]}"
  days="${MONTH_DAYS[$i]}"   # The number of days in this month
  
  # Constructing output file path inside the same directory as the original PCAP
  output_file="${BASEDIR}/${YEAR}-${month}-port1433-1434.cap"
  
  # eample: For January 2005  - > from "2005-01-01 00:00:00" to "2005-01-31 23:59:59"
  START="${YEAR}-${month}-01 00:00:00"
  END="${YEAR}-${month}-${days} 23:59:59"
  
  # editcap to filter
  editcap -A "$START" -B "$END" "$PCAPFILE" "$output_file"
  
  # cheking if the output file has packets
  packet_count=$(capinfos -c "$output_file" 2>/dev/null | awk '/Number of packets/{print $4}')
  
# making "exception" if no packets or no info, removing file and record missing month
  if [[ -z "$packet_count" || "$packet_count" == "0" ]]; then
    rm -f "$output_file"
    missing_months+=("$month")
  fi
done

# output warnings 
if [[ ${#missing_months[@]} -gt 0 ]]; then
  echo "WARNING: No packets found for these months in $PCAPFILE (file removed):"
  for mm in "${missing_months[@]}"; do
    echo "  - Month $mm of $YEAR"
  done
else
  echo "All 12 monthly PCAPs created successfully."
fi

exit 0
