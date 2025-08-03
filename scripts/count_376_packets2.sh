#!/bin/bash

#the files need to be seorted with a specific name for the script to work, or adjust the script
#used like this to get comandline output and CSV file: specify directory with cap files: './count_376_packets.sh ./ > file2.scv'
#for multiple directorys in one go use this: './count_376_packets2.sh year_20**_directorys > file2.scv'



# reminder of the structure
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <directory1> [directory2] [directory3] ..." >&2
    exit 1
fi

# CSV header
echo "year,month,packet_count"

# Looping each provided directory
for TARGET_DIR in "$@"; do

    # need to be a directory
    if [ ! -d "$TARGET_DIR" ]; then
        echo "Warning: '$TARGET_DIR' is not a directory, skipping." >&2
        continue
    fi

    # change to the target directory
    pushd "$TARGET_DIR" > /dev/null

    # looping over all PCAP files matching the pattern "20**-*-port1433-1434.cap"
    for pcap in 20**-*-port1433-1434.cap; do
        [ -e "$pcap" ] || continue

        # finding the year and month number from the filename
        # pre-made filename format: YYYY-MM-...-port1433-1434.cap)
        year=$(echo "$pcap" | cut -d'-' -f1)
        month_num=$(echo "$pcap" | cut -d'-' -f2)

        # changing month number into month name (ex:"08" ->"August")
        month_name=$(date -d "$year-$month_num-01" +%B)

        # core command 
        #counting number of packets with frame length equal to 418 (376-byte Slammer UDP payload + headers)
        packet_count=$(tshark -r "$pcap" -Y "frame.len == 418" 2>/dev/null | wc -l)

        # printing the CSV header row: year, month name, packet count
        echo "$year,$month_name,$packet_count"
    done

    # return to the previous directory (if there many dir targets)
    popd > /dev/null
done
