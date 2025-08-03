#!/bin/bash

#the files need to be seorted with a specific name for the script to work, or adjust the script
#used like this to get comandline output: './count_376_packets.sh *.cap' or like this to take full directory './count_376_packets.sh ./' 
# or './count_376_packets.sh ./directory_with_pcaps > file1.csv'


if ! command -v tshark &> /dev/null; then
    echo "Error: tshark is not installed." >&2
    exit 1
fi

for pcap in 20**-*-port1433-1434.cap; do

    [ -e "$pcap" ] || continue
    year=$(echo "$pcap" | cut -d'-' -f1)
    month_num=$(echo "$pcap" | cut -d'-' -f2)
    month_name=$(date -d "2000-$month_num-01" +%B)
    packet_count=$(tshark -r "$pcap" -Y "frame.len == 418" 2>/dev/null | wc -l)
    echo "$month_name, $packet_count"
done
