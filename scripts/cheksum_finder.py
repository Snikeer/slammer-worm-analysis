import sys
import os
from scapy.all import rdpcap, UDP


# Slammer checksum to compare (optional)
KNOWN_SLAMMER_CHECKSUM = 0x7654

def custom_sum(payload):
    """Compute a simple 16-bit sum of the given payload bytes."""
    return sum(payload) & 0xFFFF

def main():
    """
    Usage:
        python3 script.py 2005-08-port1433-1434.cap
        python3 script.py 2005-*
        python3 script.py file1.cap file2.cap file3.cap
    """
    #reminfer
    if len(sys.argv) < 2:
        print("Usage: python script.py <pcap_or_cap_file> [<pcap_or_cap_file2> ... ]")
        sys.exit(1)

    # looping through every file specified in argument
    for pcap_file in sys.argv[1:]:
    
       	# making an output file name based on the input name
        base_name = os.path.basename(pcap_file)

        # removing file extensions 
        if base_name.endswith(".pcap"):
            base_name = base_name[:-5]
        elif base_name.endswith(".cap"):
            base_name = base_name[:-4]

       # output CSV name (e.g., "2005-08-port1433-1434-checksum.csv")
        out_file = f"{base_name}-checksum.csv"

        print(f"[+] Processing {pcap_file} -> {out_file}")

       # read the packets from the PCAP file
        packets = rdpcap(pcap_file)

        # open output file in write mode
        with open(out_file, "w") as f:
            # Write a header row (CSV)
            f.write("packet_index,checksum_hex,match_flag\n")

            # going throug packets
            for i, pkt in enumerate(packets):
                if pkt.haslayer(UDP):
                # extracting the raw UDP payload
                    pay = bytes(pkt[UDP].payload)
                    cs_val = custom_sum(pay)

                    # compareing checksum (if set)
                    if KNOWN_SLAMMER_CHECKSUM is not None:
                        match_flag = "YES" if cs_val == KNOWN_SLAMMER_CHECKSUM else "NO"
                    else:
                        match_flag = "N/A"

                    # writing the result in CSV format
                    f.write(f"{i},0x{cs_val:04x},{match_flag}\n")

        print(f"[+] Checksums saved to file: {out_file}")

if __name__ == "__main__":
    main()
