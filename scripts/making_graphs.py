import pandas as pd
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from matplotlib.dates import DateFormatter

def main():
    parser = argparse.ArgumentParser(description='Generate daily and monthly UDP packet counts from CSV files.')
    parser.add_argument('csv_files', type=str, nargs='+', help='One or more CSV files to analyze')
    args = parser.parse_args()

    # processing each file
    for csv_file in args.csv_files:
        print(f"Processing {csv_file}...")
        df = pd.read_csv(csv_file)

        # converting the 'frame.time' column to datetime
        if 'frame.time' in df.columns:
            df['time'] = pd.to_datetime(df['frame.time'])
        else:
            df['time'] = pd.to_datetime(df['time'])

        # setting time as index
        df.set_index('time', inplace=True)

        # DAILY LINE CHART
        daily_counts = df.resample('D').size()

        plt.figure(figsize=(10, 6))
        ax1 = plt.gca()
        daily_counts.plot(kind='line', color='purple', markersize=4, ax=ax1)
       
        # title/labels 
        year_str = df.index[0].year
        plt.title(f"Daily UDP Packet Counts (Slammer Traffic) - {year_str}")
        plt.xlabel(f"{year_str} by Day")
        plt.ylabel("Packet Count")

        # x-axis to show short month names + day
        date_format = DateFormatter('%b')
        ax1.xaxis.set_major_formatter(date_format)
        plt.xticks(rotation=45)
        plt.tight_layout()
        daily_output = f"{Path(csv_file).stem}_daily_linechart.png"
        plt.savefig(daily_output)
        plt.show()

        # MONTHLY BAR CHART
        monthly_counts = df.resample('M').size()
        plt.figure(figsize=(10, 6))
        ax2 = plt.gca()
        monthly_counts.plot(kind='bar', color='orange', ax=ax2)
        plt.title(f"Monthly UDP Packet Counts (Slammer Traffic) - {year_str}")
        plt.xlabel(f"{year_str} by Month")
        plt.ylabel("Packet Count")
      
        # x-axis tick labels to month short names
        monthly_labels = monthly_counts.index.strftime('%b')
        ax2.set_xticklabels(monthly_labels, rotation=45)
        plt.tight_layout()
        monthly_output = f"{Path(csv_file).stem}_monthly_barchart.png"
        plt.savefig(monthly_output)
        plt.show()

if __name__ == "__main__":
    main()
