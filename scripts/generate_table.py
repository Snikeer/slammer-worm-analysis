import os
import sys
import subprocess
from prettytable import PrettyTable

# Usage:
#	./SCRIPT DIRECTORY_PATH
# Eample:
#	python3 generate_table.py  2005-port1433-1434/


# redoing months to convert month-number to month-name
def month_to_name(month_num):
    months = {
        "01": "January", "02": "February", "03": "March", "04": "April", "05": "May",
        "06": "June", "07": "July", "08": "August", "09": "September", "10": "October",
        "11": "November", "12": "December"
    }
    return months.get(month_num, "Total")

# Checking if directory is passed as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python3 generate_table.py <directory_path>")
    sys.exit(1)

# Geting the directory path from argument
directory = sys.argv[1]

if not os.path.isdir(directory):
    print(f"Error: The path '{directory}' is not a valid directory.")
    sys.exit(1)

# making PrettyTable just for fast visual validation of the splitting
table = PrettyTable()
table.field_names = ["Month", "Start Time", "End Time", "# Packets", "File Size"]

# converting result to LaTeX table if needed (was not so useful in the end )
latex_table = []
latex_table.append("\\begin{table}[H]")
latex_table.append("\\centering")
latex_table.append("\\begin{tabular}{|l|l|l|r|r|}")
latex_table.append("\\hline")
latex_table.append("Month & Start Time & End Time & \\# Packets & File Size \\\\ \\hline")

# year 
year = None

# Processing each .cap file in the given directory
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".cap"):
        filepath = os.path.join(directory, filename)

        # Extracting year from filename
        if year is None:
            year = filename.split("-")[0]

        # Capinfos gathering Start/End Time and File Size
        result = subprocess.run(["capinfos", filepath], capture_output=True, text=True)
        info = result.stdout.splitlines()

        # Extracting required fields
        start_time = next((line.split(": ", 1)[1].split(".")[0] for line in info if "First packet time" in line), "N/A")
        end_time = next((line.split(": ", 1)[1].split(".")[0] for line in info if "Last packet time" in line), "N/A")
        file_size = next((line.split(": ", 1)[1] for line in info if "File size" in line), "N/A")

        # tshark to count number of packets
        packet_count_result = subprocess.run(["tshark", "-r", filepath], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        packet_count = len(packet_count_result.stdout.splitlines())
	

	# extract month

        month_num = filename.split("-")[1]
        month_name = month_to_name(month_num)



        # row to the PrettyTable
        table.add_row([month_name, start_time, end_time, f"{packet_count:,}", file_size])

        # row to the LaTeX table
        latex_table.append(f"{month_name} & {start_time} & {end_time} & {packet_count:,} & {file_size} \\\\ \\hline")

# elements of the LaTeX table
latex_table.append("\\end{tabular}")
latex_table.append(f"\\caption{{PCAP Summary for Year {year}}}")
latex_table.append("\\label{{tab:pcap_summary}}")
latex_table.append("\\end{table}")

# write both tables to the same text file
output_file = os.path.join(directory, "pcap_summary.txt")
with open(output_file, "w") as f:
    # write the PrettyTable 
    f.write(f"Year: {year}\n\n")
    f.write(table.get_string())
    f.write("\n\n")
    f.write("Below is the LaTeX table for use in Overleaf:\n\n")
    # write the LaTeX table 
    f.write("\n".join(latex_table))

print(f"Table written to {output_file}")
