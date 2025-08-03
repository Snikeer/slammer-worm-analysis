import sys
import subprocess

if len(sys.argv) != 2:
    print("Usage: python3 script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# calculating total unique IP count
total_ips_cmd = f"tail -n +2 {filename} | wc -l"
total_ips = int(subprocess.check_output(total_ips_cmd, shell=True).strip())

# command for country analysis
country_cmd = (
    f"awk -F '|' '{{print $4}}' {filename} | sort | uniq -c | sort -rn | "
    f"awk '{{print $2,\"&\",$1,\"&\", sprintf(\"%.2f\\\\% \\\\\\\\ \\\\hline\", ($1/{total_ips})*100)}}' | head"
)
country_result = subprocess.check_output(country_cmd, shell=True).decode()

# command for 16 netblock analysis
netblock_cmd = (
    f"awk -F '|' '{{print $2, $4}}' {filename} | grep -E '[0-9]+'| awk '{{split($1, x, \".\"); print x[1]\".\"x[2]\".0.0/16\", $2}}'| sort | uniq -c | sort -rn | "
    f"awk '{{print $3,\"&\",$2,\"&\",$1,\"&\", sprintf(\"%.2f\\\\% \\\\\\\\ \\\\hline\", ($1/{total_ips})*100)}}' | head"
)
netblock_result = subprocess.check_output(netblock_cmd, shell=True).decode()

# print result, easy peasy
print(f"\nTotal unique IP addresses: {total_ips}\n")

print('\\begin{table}[H]\n\\centering\n\\begin{subtable}[t]{0.48\\textwidth}\n\\centering\n\\begin{tabular}{|l|r|r|}\n\\hline\nCountry & Count & Percentage \\\\ \\hline')
print(country_result)
print('\\end{tabular}\n\\caption{Top 10 Countries by Unique IP Addresses}\n\\end{subtable}\n\\hfill\n\\begin{subtable}[t]{0.48\\textwidth}\n\\centering\n\\begin{tabular}{|l|r|r|r|}\n\\hline\nCountry & /16 Netblock & Count & Percentage \\\\ \\hline')
print(netblock_result)
print('\\end{tabular}\n\\caption{Top /16 Netblocks by Slammer Hits}\n\\end{subtable}\n\\caption{Slammer Activity}\n\\label{tab:combined_tables}\n\\end{table}')
