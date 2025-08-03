
# Slammer Worm: From Outbreak to Stagnation?

**Bachelor Thesis in Cybersecurity – 2025**  
*Alexander Danielsen, Noroff University College*

This repository contains all scripts and visualizations developed for my Bachelor project analyzing long-term activity of the SQL Slammer worm using Internet Background Radiation (IBR) data from 2005 to 2024.

📄 **Full report**: [`Slammer_2025_Report.pdf`](./report/Slammer_2025_Report.pdf)

> ⚠️ The raw PCAP dataset is excluded due to ethical, legal, and size limitations. Only scripts, output files, and images are included.

---

## 🧪 Project Overview

The goal of this project was to determine if the Slammer worm, despite being released in 2003, still generates detectable traffic nearly two decades later. This was achieved by:

- Filtering UDP traffic targeting ports 1433 and 1434.
- Detecting Slammer activity by size, checksum, and MD5 hash of payloads.
- Visualizing temporal and geographical distribution of hits.
- Verifying payloads against VirusTotal API.
- Documenting trends, anomalies, and long-term persistence.

---

## 📂 Repository Structure

```
Slammer-Worm-Analysis/
├── scripts/               # Core analysis scripts (filtering, splitting, counting)
├── 1_timestamps/          # Timestamp conversion and traffic graphs
├── 2_geolocation/         # IP enrichment and country/netblock stats
├── 3_hashes/              # Payload hashing and VirusTotal lookups
├── report/                # Full PDF thesis report
└── README.md              # This file
```

---

## 🛠️ Tools & Technologies

- **Languages:** Python, Bash
- **Libraries:** `pandas`, `matplotlib`, `hashlib`, `prettytable`
- **Network tools:** `tcpdump`, `tshark`, `capinfos`, `editcap`, `netcat`
- **External APIs:** VirusTotal, Team Cymru WHOIS

---

## 🧾 Scripts Overview

### 🔹 1. `monthly_spliter.sh`
Splits a large yearly `.cap` file into monthly segments. Uses timestamp filtering and removes empty months.

### 🔹 2. `generate_table.py`
Summarizes PCAP files with start/end time, packet count, and file size. Outputs PrettyTable and LaTeX tables.

### 🔹 3. `filter_split_review.py`
Filters yearly `.cap` file by ports 1433/1434 and then splits it into months. Includes table generation.

### 🔹 4. `hashcheker.py` / `cheksum_finder.py`
Identifies Slammer-like payloads:
- `hashcheker.py`: MD5 hash detection
- `cheksum_finder.py`: 16-bit checksum detection

### 🔹 5. `count_376_packets.sh` / `count_376_packets2.sh`
Counts packets of length 418 bytes (Slammer size). Second version supports multiple directories and outputs CSV.

### 🔹 6. `grafer2.py` / `grafer3.py`
Reads CSV files and generates:
- Line charts (grafer2)
- Bar charts (grafer3)
Used to visualize Slammer activity over time.

### 🔹 7. `1_timestamps/converter_of_time.py`
Converts Unix timestamps to human-readable format via pipe from `tshark` output.

### 🔹 8. `1_timestamps/making_graphs.py`
Generates daily and monthly Slammer activity charts from CSV timestamp logs.

### 🔹 9. `2_geolocation/geolocator.sh`
Extracts IPs from timestamped CSVs and queries Cymru WHOIS for ASN and country info.

### 🔹 10. `2_geolocation/time_saver.py`
Parses WHOIS enrichment output and prints LaTeX tables for:
- Top countries
- Top /16 netblocks

### 🔹 11. `3_hashes/hash_and_sizhe_chelcker.py`
Hashes all UDP payloads in PCAP files and records their size in a CSV.

### 🔹 12. `3_hashes/virustotal_hashchecker.py`
Queries VirusTotal API for metadata and detection stats on suspicious hashes.

---

## 🚀 Example Usage

```bash
# Split a full-year PCAP into monthly segments
bash scripts/monthly_spliter.sh 2005-total.cap 2005

# Generate traffic summary table
python3 scripts/generate_table.py ./2005-port1433-1434/

# Filter + split + generate stats
python3 scripts/filter_split_review.py ./2005-port1433-1434/

# Detect Slammer via hash
python3 scripts/hashcheker.py 2005-08-port1433-1434.cap

# Count 418-byte packets across multiple directories
bash scripts/count_376_packets2.sh ./year_dirs > slammer_count.csv

# Plot graphs
python3 scripts/grafer3.py slammer_count.csv

# Convert timestamps
tshark ... | python3 1_timestamps/converter_of_time.py 2005

# Geolocation
bash 2_geolocation/geolocator.sh ../1_timestamps/timestamp_slammer_2020_data.csv

# VirusTotal lookup
python3 3_hashes/virustotal_hashchecker.py
```

---

## 📈 Results Preview

You can view example charts, CSVs, and summaries inside:

- `1_timestamps/` → time-based traffic graphs
- `2_geolocation/` → enriched IP stats
- `3_hashes/` → hash metadata and VirusTotal lookups

---

## 📌 Notes

- Scripts assume a specific filename and folder pattern like:  
  `2005-port1433-1434/2005-08-port1433-1434.cap`  
  Adjust paths as needed.
- Most tools expect Bash, Python 3.8+, and Wireshark CLI tools (`tshark`, `capinfos`, etc.) installed.
- For VirusTotal API, you'll need to generate a free key and insert it in `virustotal_hashchecker.py`.

---

## 📫 Contact

Feel free to connect or message me on [LinkedIn](https://www.linkedin.com/in/alexander-danielsen-b13479157)if you're interested in the project, have questions, or want to collaborate.

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code.



______________________________________________________________________













More detailed description of the scripts   (optional)

	
	
1. /script/monthly_spliter.sh

	This script splits a large PCAP (2005-total) file into monthly PCAP files based on the specified year. 
	It creates one file per month containing only the packets from that month.
	Each output file is automatically named using a hardcoded format:
	YEAR-MONTH-port1433-1434.cap (like: 2005-08-port1433-1434.cap).
	At the start, the script shows the timestamp of the first and last packet in the original file t
	o give a quick overview of the capture range.
	It then extracts packets for each month based on precise timestamps
	 (from the first day 00:00:00 to the last day 23:59:59).
	If a month has no packets, the empty file is deleted, and a warning is printed.

	Eample:
          ./monthly_spliter.sh ./2005-port1433-1444.cap 2005


2. /script/generate_table.py

	This script processes all .cap files in a given directory and creates a summary of their content. 
	For each .cap file, it extracts four pieces of information: 
	the first packet time, the last packet time, the number of packets, and the file size.
	To get this information, the script uses capinfos command to get info abou the packet  
	and tshark command to count the number of packets in each file.
	After collecting this information, the script formats it into two types of tables. 
	One is a readable text table using the PrettyTable library, which shows the results in columns with headers. 
	The other is a LaTeX table, which is useful if you want to include the results in a scientific or academic report. 
	The final output is saved in a file named pcap_summary.txt inside the same directory where the .cap files are located.
	It was assumed that this script would be more used when developed, 
	but in the end it was used only to validate results of the first monthly_spliter.sh described above. 	

	Eample:
          python3 generate_table.py  2005-port1433-1434/


3. /script/filter_split_review.py

	This script is essentially a combination of the monthly splitter and table generator scripts above, 
	or at least the functuanalyty of these two, with an additional step added at the beginning to filter t
	raffic by ports 1433 and 1434 using tcpdump.
	Script looking for pre-named files that included"-total" in the filename. 
	Total waa files with all the packets of the year, so if som of yaerly data was presplited when i got it, 
	it needed to be merged first.
	The script extracts the year from the filename (for example, from "2021-total" it gets 2021).
	Using the tcpdump command, it filters the total file to keep only network traffic that uses 
	destination port 1433 or 1434. This filtered traffic is saved to a new file total-filtered. 
	Before splitting, it deletes all existing .cap files in the directory to avoid mixing new and old files.
	It then splits the filtered file into 12 monthly PCAP files using the editcap tool. 
	Each output file contains only the packets from one calendar month based on timestamps 
	as mentioned in the first script.
	For each of these new .cap files, it uses the capinfos tool to extract the start time, end time, and file size, 
	and it uses the tshark tool to count the number of packets.The script creates a summary table using 
	PrettyTable and makes a LaTeX version of the table for report. 
	All results are saved in a file called pcap_summary.txt inside the same directory.

	Eample:
          python3 generate_table.py  2005-port1433-1434/


4.  two scripts /script/hashcheker.py and /script/cheksum_finder.py (very simular in the build minor, with a nibor difference)

	The scripts hashcheker.py and cheksum_finder.py analyze UDP packets in one or more PCAP files to detect 
	possible Slammer worm activity. 
	hashcheker.py for each UDP payload, it calculates the MD5 hash using Python library hashlib and compares it to  
	Slammer worm hash (a0aa4a74b70cbca5a03960df1a3dc878).
	While cheksum_finder.py calculates a simpler 16 bit checksum by summing the p
	ayload bytes (sum(payload) & 0xFFFF) and compares it to lammer checksum value. (0x7654)
	Both scripts output their results to separate CSV files, listing the packet index, computed value, 
	and whether it matches the expected Slammer signature.


	Example:
           python3 ./hashcheker.py 2005-port1433-1434/f2005-08-port1433-1434.cap
           python3 ./hashcheker.py 2005-port1433-1434/2005-*.cap
           python3 ./hashcheker.py file1.cap file2.pcap ...

	



5.  two scripts /script/count_376_packets.sh and /script/count_376_packets2.sh

	The script count_376_packets.sh scans .cap files named in the format YYYY-MM-port1433-1434.cap 
	within the current directory and counts how many packets have a frame length of 418 bytes. 
	It uses tshark to filter these packets and prints the result as a simple list of month, packet_count pairs.
	The second script, count_376_packets2.sh, is an extended and more flexible version of the first. 
	It allows users to specify one or more directories as input, processes all matching .cap 
	files in each directory, and prints a CSV-formatted output with columns year, month, packet_count. 
	It also includes basic input validation and directory navigation to support batch processing of multiple datasets.
	In short, count_376_packets2.sh builds on the functionality of count_376_packets.sh 
	by adding pasibility for multiple directory processing,  CSV format heading for the output, 
	and improved usability for larger scale analysis.
	
	Example:
	   ./count_376_packets.sh 2005-port1433-1434/directory_with_pcaps > file1.csv
	or
	   ./count_376_packets2.sh year_20**_directorys > file2.scv



6.  two scripts /script/grafer2.py and /script/grafer3.py
	
	The scripts grafer2.py and grafer3.py both reading a CSV file containing monthly packet counts and 
	visualize the data over time using Pythons pandas and matplotlib libraries. 
	For the scripts to work correctly, the CSV file must include a header row with the exact column names: 
	year, month, and packet_count. 
	grafer2.py generates a line chart to show traffic patterns, 
	while grafer3.py producing a bar chart with litle diferent date formatting and 
	and axis labels for easyer fit Both scripts have same structure for parsing and sorting the data.

	Example:
	    python3 ./grafer2.py 2005-port1433-1434/file2.csv
	or
	    python3 ./grafer3.py 2005-port1433-1434/file2.csv  






7. Script ./1_timestamps/converter_of_time.py              ( also found in /script/converter_of_time.py)

	This Python script was used to convert epoch timestamps (from frame.time_epoch) into human-readable 
	UTC date-time strings in CSV data extracted from PCAP files. It does not read the PCAP directly, 
	but instead processes the output of a tshark command piped through standard input. 
	The input was generated using filters like frame.len == 418 to isolate Slammer-related traffic and 
	fields such as ip.src and udp.dstport. This script was created to replace a slower manual 
	solution that used awk and the date command for timestamp conversion. 

	to replace slow manuall conversion (which to for ages to covert all years): 
	
	tshark -r ../2005-port1433-1434/2005-total_filtered_ports_1433-1434-Y 
	"frame.len == 418" -T fields -e frame.time_epoch -e ip.src -e udp.dstport -E header=y -E 
	separator=, -E quote=d 2>/dev/null | awk -F, 'NR==1 {print $0; next} 
	{cmd="date -d @"$1" +\"%Y-%m-%d %H:%M:%S\""; cmd | 
	getline timestamp; close(cmd); $1=timestamp; print $0}' OFS=, > timestamp_slammer_2005_data.csv


	with faster one (still tok a lot of time):
	
	Example:
	   tshark -r ../2005-port1433-1434/2005-total_filtered_ports_1433-1434 -Y "frame.len == 418" -T 
	   fields -e frame.time_epoch -e ip.src -e udp.dstport -E header=y -E separator=, -E quote=d 2>/dev/null | 
	   python3 converter_of_time.py 2005
 


8. Script ./1_timestamps/making_graphs.py             ( also found in /script/making_graphs.py )

	This script build on the CSV files produced for all years i the Script 7. It reads one or more 
	CSV files containing timestamped data and generates two charts types for each file/yesr: 
	A line chart based on daily acurancis and a bar chart based on monthly acuransis, 
	showing the number of records per day and per month. It uses the pandas library to parse the data and 
	resample it by time intervals, and matplotlib to create and save the plots. 
	The script looks for a column named frame.time or time, converts it to datetime, sets it as the index, 
	and then groups the data by day and by month. 
	Each chart is saved as a PNG image with filenames based on the original CSV filename. (the best script)

	(when inside directory ./1_timestamps/)
	Example:
	   python3 making_graphs.py timestamp_slammer_2005_data.csv    

7.-8. results of csv files and all chart is avaiable at ./1_timestamps/ directory





9. Script ./2_geolocation/geolocator.sh                 ( also found in /script/geolocator.sh )

	This Bash script, geolocator.sh , automates the process of extracting unique IP addresses from a CSV file 
	and then querying the file yar by year against the Cymru WHOIS service to retrieve enrichment data. 
	It takes a CSV file as input (with timestamped records), extracts the year from the filename, 
	and isolates all unique source IP addresses (from the second column, 
	skipping the header and removing quotation marks). 
	It then formats the IP list by adding the required begin, verbose, and end lines for a valid Cymru batch query. 	
	After a short pause, it sends the query using netcat (nc) to whois.cymru.com on port 43 and saves the response 
	to a files with name like enrich_<year>.cymru. This script was created to avoid running repetitive 
	commands manually and was used efficiently in a loop to process data of 19 yers
	
	(when inside ./2_geolocation/)
	Example:
	   for year in {2005..2024}; do ./geolocator.sh "../1_timestamps/timestamp_slammer_${year}_data.csv" & done
	
	
	
	
10.  Script ./2_geolocation/time_saver.py                           ( also found in /script/time_saver.py )
		
	This Python script analyzes a Cymru WHOIS-enriched file (formatted with pipe separetad | fields) and generates 
	LaTeX-formatted tables showing the top countries and top /16 IP netblocks by unique IP count. 
	It first calculates the total number of unique IP addresses by counting all lines in the file minus header. 
	Then, using shell commands run via subprocess, it extracts and counts occurrences of each country ($4 field),
	 calculating the percentage share of each. It also constructs /16 netblocks from the IP addresses ($2 field), 
	 pairs them with their country, and aggregates counts and percentages. 
	 The output comes only as print in command line, but can easyly be sendt to text file if needed
	 Eventualy this script automate these two commands to convert all dataset faster.
	
	Manual commands:
	   awk -F '|' '{print $4}' 1_merged.cymru | sort | uniq -c | sort -rn | awk '{total=160528; percent=($1/total)*100;
	    printf "%s %d %.2f%%\n", $2, $1, percent}' | awk '{print $1,"&",$2,"&",$3,"\\\\ \\hline"}'
	    
	    and
	    
	    awk -F '|' '{print $2, $4}' 1_merged.cymru| grep -E '[0-9]+'| awk '{split($1, x, "."); 
	    print x[1]"."x[2]".0.0/16", $2}'| sort | uniq -c | sort -rn | 
	    awk '{print $3,"&",$2,"&",$1,"&", sprintf("%.2f", ($1/163860)*100)"\\%\\\\ \\hline"}' | head
	

	(when inside ./2_geolocation/)
	
	Example:
	    python3 time_saver.py enrich_2012.cymru                 

	Output:

	Total unique IP addresses: 836

	\begin{table}[H]
	\centering
	\begin{subtable}[t]{0.48\textwidth}
	\centering
	\begin{tabular}{|l|r|r|}
	\hline
	Country & Count & Percentage \\ \hline
	RU & 263 & 31.46\% \\ \hline
	CN & 108 & 12.92\% \\ \hline
	US & 98 & 11.72\% \\ \hline
	TW & 79 & 9.45\% \\ \hline
	GB & 32 & 3.83\% \\ \hline
	JP & 31 & 3.71\% \\ \hline
	IN & 21 & 2.51\% \\ \hline
	AR & 19 & 2.27\% \\ \hline
	BR & 17 & 2.03\% \\ \hline
	MY & 12 & 1.44\% \\ \hline

	\end{tabular}
	\caption{Top 10 Countries by Unique IP Addresses}
	\end{subtable}
	\hfill
	\begin{subtable}[t]{0.48\textwidth}
	\centering
	\begin{tabular}{|l|r|r|r|}
	\hline
	Country & /16 Netblock & Count & Percentage \\ \hline
	RU & 94.242.0.0/16 & 114 & 13.64\% \\ \hline
	RU & 109.225.0.0/16 & 42 & 5.02\% \\ \hline
	RU & 212.106.0.0/16 & 29 & 3.47\% \\ \hline
	TW & 122.121.0.0/16 & 20 & 2.39\% \\ \hline
	TW & 111.253.0.0/16 & 11 & 1.32\% \\ \hline
	CN & 222.37.0.0/16 & 10 & 1.20\% \\ \hline
	GB & 172.129.0.0/16 & 10 & 1.20\% \\ \hline
	AR & 186.110.0.0/16 & 9 & 1.08\% \\ \hline
	GB & 172.162.0.0/16 & 9 & 1.08\% \\ \hline
	RU & 94.41.0.0/16 & 7 & 0.84\% \\ \hline

	\end{tabular}
	\caption{Top /16 Netblocks by Slammer Hits}
	\end{subtable}
	\caption{Slammer Activity}
	\label{tab:combined_tables}
	\end{table}
		       
	
	
	
	
	
11. Script ./3_hashes/hash_and_sizhe_chelcker.py                          ( also found in /script/hash_and_sizhe_chelcker.py )
	
	Slightly modified version of a previous md5 hash script, this version removes Slammer hash validation and 
	instead adds functionality to record the size of each UDP payload alongside its MD5 hash. 
	It processes one or more pcap files and outputs a CSV file per input, 
	containing the packet index, hash value, and payload size.
	
	(when inside ./3_hashes/
	
	Example:
           python3 hash_and_sizhe_chelcker.py 2005-port1433-1434/2005-08-port1433-1434.cap
           python3 hash_and_sizhe_chelcker.py  2005-port1433-1434/2005-*.cap
           python3 hash_and_sizhe_chelcker.py file1.cap file2.pcap ...
	
	
	
	
	
12. Script ./3_hashes/virustotal_hashchecker.py                                ( also found in /script/virustotal_hashchecker.py     )
	
	This Python script interacts with the VirusTotal API to query metadata and scan results 
	for a list of hardcoded MD5 hashes. It sets the required API key in the HTTP request headers and iterates through
	 each hash in the list. For each hash, it performs an HTTP GET request to the /api/v3/files/{hash} endpoint. 
	 If the response contains a valid data block, it extracts and prints attributes such as m
	 eaningful_name, size, reputation, and last_analysis_stats 
	 including counts for malicious, suspicious, undetected, and harmless. 
	 If the request fails or the hash is unknown to VirusTotal, it handles and displays the error code message. 
	 The hashes is from filtering results from the last script (11)

	
	(when inside ./3_hashes/
	Example:
	   python3 virustotal_hashchecker.py
	
	
	
	



