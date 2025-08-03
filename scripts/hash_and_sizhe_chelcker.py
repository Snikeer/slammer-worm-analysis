import sys
import os
import hashlib
from scapy.all import rdpcap, UDP

def main():
    """
    this is how start used wit singel file or multiple files:
        python3 myscript.py 2005-08-port1433-1434.cap
        python3 myscript.py 2005-*
        python3 myscript.py file1.cap file2.pcap ...
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <pcap_or_cap_file1> [<pcap_or_cap_file2> ...]")
        sys.exit(1)

    # looping through every file specified on the command line
    for pcap_file in sys.argv[1:]:
        filename= os.path.basename(pcap_file)

        # removing known file extensions if present
        if filename.endswith(".pcap"):
            filename = filename[:-5]
        elif filename.endswith(".cap"):
            filename = filename[:-4]

        # output CSV filename ("oldfilename-size_and_hash.csv")
        out_file = f"{filename}-size_and_hash.csv"

        print(f"[+] Processing {pcap_file} -> {out_file}")

        # packets from the pcap file
        packets = rdpcap(pcap_file)

        # write mode new file
        with open(out_file, "w") as f:
            # make a litle header packet_index, md5_hash, payload_size
            f.write("packet_number,hash_value,size\n")

           
            for packet_count, pkt in enumerate(packets):
                if pkt.haslayer(UDP):
                    # extracting raw UDP payload
                    pay = bytes(pkt[UDP].payload)
                    # MD5 hash
                    md5val = hashlib.md5(pay).hexdigest()
                    # size
                    size = len(pay)

                    # writing packet_number, hash_value, size
                    f.write(f"{packet_count},{md5val},{size}\n")

        print(f"[+] Hurray!! saving result to {out_file}")

if __name__ == "__main__":
    main()
