import os
import sys
import subprocess
from datetime import date
from prettytable import PrettyTable

def is_leap_year(year: int) -> bool:
    """Return True if 'year' is a leap year, False otherwise."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def days_in_month(year: int, month: int) -> int:
    """Return the number of days for the given 'month' in 'year'."""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    else:
        raise ValueError("Invalid month")

def month_to_name(month_num):
    """Convert a string month (01, 02, …) to its name."""
    months = {
        "01": "January", "02": "February", "03": "March", "04": "April", "05": "May",
        "06": "June", "07": "July", "08": "August", "09": "September", "10": "October",
        "11": "November", "12": "December"
    }
    return months.get(month_num, "Total")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a valid directory.")
        sys.exit(1)

    # 1. Find the *-total file. (e.g., 2021-total)
    total_file = None
    for f in os.listdir(directory):
        if f.endswith("-total"):
            total_file = f
            break

    if total_file is None:
        print("No *-total file found in the directory.")
        sys.exit(1)

    # Extract the year from the filename (e.g. "2021-total" -> "2021")
    year_str = total_file.split("-")[0]
    try:
        year_int = int(year_str)
    except ValueError:
        print(f"Could not extract a valid year from filename: {total_file}")
        sys.exit(1)

    total_path = os.path.join(directory, total_file)
    filtered_file = f"{year_str}-total_filtered_ports_1433-1434"  # no .cap extension
    filtered_path = os.path.join(directory, filtered_file)

    # 2. Run tcpdump to filter out only the ports 1433 or 1434 traffic
    print(f"Filtering {total_file} into {filtered_file} (ports 1433/1434 only)…")
    tcpdump_cmd = [
        "tcpdump", "-r", total_path,
        "(udp dst port 1433 or udp dst port 1434 or tcp dst port 1433 or tcp dst port 1434)",
        "-w", filtered_path
    ]
    subprocess.run(tcpdump_cmd, check=True)

    # 3. Remove all *.cap files in that directory
    print(f"Removing all *.cap files in '{directory}'…")
    for f in os.listdir(directory):
        if f.endswith(".cap"):
            os.remove(os.path.join(directory, f))

    # 4. Split the filtered file into monthly PCAP files
    # We’ll call the monthly files, e.g.: 2020-01-port1433-1434.cap
    for month in range(1, 13):
        start_day = 1
        end_day = days_in_month(year_int, month)

        month_str = f"{month:02d}"
        start_time = f"{year_str}-{month_str}-01 00:00:00"
        end_time   = f"{year_str}-{month_str}-{end_day} 23:59:59"

        out_file   = os.path.join(directory, f"{year_str}-{month_str}-port1433-1434.cap")

        print(f"Splitting out {out_file} from {filtered_file}…")
        editcap_cmd = [
            "editcap",
            "-A", start_time,
            "-B", end_time,
            filtered_path,
            out_file
        ]
        subprocess.run(editcap_cmd, check=True)

    # 5. Run the capinfos/tshark summary generation on the newly split files
    print("Generating pcap_summary.txt using capinfos/tshark…")

    table = PrettyTable()
    table.field_names = ["Month", "Start Time", "End Time", "# Packets", "File Size"]

    latex_table = [
        "\\begin{table}[H]",
        "\\centering",
        "\\begin{tabular}{|l|l|l|r|r|}",
        "\\hline",
        "Month & Start Time & End Time & \\# Packets & File Size \\\\ \\hline"
    ]

    # Process each .cap file in sorted order so the months come out in order
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".cap"):
            filepath = os.path.join(directory, filename)

            # Run capinfos
            result = subprocess.run(["capinfos", filepath],
                                    capture_output=True, text=True)
            info = result.stdout.splitlines()

            start_time = next((line.split(": ", 1)[1].split(".")[0]
                               for line in info if "First packet time" in line), "N/A")
            end_time = next((line.split(": ", 1)[1].split(".")[0]
                             for line in info if "Last packet time" in line), "N/A")
            file_size = next((line.split(": ", 1)[1]
                              for line in info if "File size" in line), "N/A")

            # Run tshark to get packet count
            packet_count_result = subprocess.run(["tshark", "-r", filepath],
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.DEVNULL)
            packet_count = len(packet_count_result.stdout.splitlines())

            # Extract month from filename (e.g. 2020-01-port1433-1434.cap -> "01")
            parts = filename.split("-")
            if len(parts) > 1 and parts[1].isdigit():
                month_num = parts[1]
            else:
                month_num = "00"

            month_name = month_to_name(month_num)

            table.add_row([month_name, start_time, end_time, f"{packet_count:,}", file_size])
            latex_table.append(
                f"{month_name} & {start_time} & {end_time} & {packet_count:,} & {file_size} \\\\ \\hline"
            )

    latex_table += [
        "\\end{tabular}",
        f"\\caption{{PCAP Summary for Year {year_str}}}",
        "\\label{tab:pcap_summary}",
        "\\end{table}"
    ]

    output_file = os.path.join(directory, "pcap_summary.txt")
    with open(output_file, "w") as f:
        f.write(f"Year: {year_str}\n\n")
        f.write(table.get_string())
        f.write("\n\nBelow is the LaTeX table for use in Overleaf:\n\n")
        f.write("\n".join(latex_table))

    print(f"Done. Summary written to: {output_file}")

if __name__ == "__main__":
    main()
