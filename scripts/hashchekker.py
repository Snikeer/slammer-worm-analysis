import sys
import os
import hashlib
from scapy.all import rdpcap, UDP

# Slammer MD5 to compare (optional)
KNOWN_SLAMMER_MD5 = "a0aa4a74b70cbca5a03960df1a3dc878"

def main():
    """
    Usage:
        python3 script.py 2005-08-port1433-1434.cap
        python3 script.py 2005-*
        python3 script.py file1.cap file2.cap file3.cap
    """
    #reminfer
    if len(sys.argv) < 2:
        print("Usage: python script.py <pcap_or_cap_file1> [<pcap_or_cap_file2> ...]")
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

        # output CSV name (ex: "2005-08-port1433-1434-hash.csv")
        out_file = f"{base_name}-hash.csv"

        print(f"[+] Processing {pcap_file} -> {out_file}")

        # read the packets from the PCAPfile
        packets = rdpcap(pcap_file)

        # open output file in write mode
        with open(out_file, "w") as f:
            # write a header row (CSV )
            f.write("packet_index,md5_hash,slammer_match\n")

            # going through all packets
            for i, pkt in enumerate(packets):
                if pkt.haslayer(UDP):
                
                    # ekstracting the raw UDP payload
                    pay = bytes(pkt[UDP].payload)
                    # compute MD5 hash
                    md5val = hashlib.md5(pay).hexdigest()

                    # comparing to Slammer MD5 (if set)
                    if KNOWN_SLAMMER_MD5:
                        match_flag = "YES" if md5val == KNOWN_SLAMMER_MD5 else "NO"
                    else:
                        match_flag = "N/A"

                    # write the CSV line: packet_index, MD5 hash, match_flag
                    f.write(f"{i},{md5val},{match_flag}\n")

        print(f"[+] Results saved to file:  {out_file}")

if __name__ == "__main__":
    main()
