import sys
from datetime import datetime

year = sys.argv[1]
output_file = f"timestamp_slammer_{year}_data.csv"

# output file for writing
with open(output_file, "w") as outfile:
    # header row
    outfile.write("frame.time,ip.src,udp.dstport\n")
    
    # each line from stdin
    for line in sys.stdin:
        # Skip the header row
        if line.startswith("frame.time_epoch"):
            continue
        
        # splitting the line into fields
        fields = line.strip().split(',')
        
        # converting the epoch time to a readable format
        try:
            epoch_time = float(fields[0].strip('"'))
            human_time = datetime.utcfromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            # skip lines with invalid epoch time
            continue
        
        # write the formatted line to the output file
        outfile.write(f'"{human_time}",{fields[1]},{fields[2]}\n')
