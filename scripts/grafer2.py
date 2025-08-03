import pandas as pd
import matplotlib.pyplot as plt
import argparse

def main():
    # reminder
    # set up argument like: python3 scriptname.py 2005-port1433-1434/file2.csv
    parser = argparse.ArgumentParser(description='Plot time series data from a CSV file to make linechart')
    parser.add_argument('csvfile', type=str,
                        help='Path to the CSV file containing data with header: year,month,packet_count')
    args = parser.parse_args()

    # reading the CSV file (the header row is read automatically)
    df = pd.read_csv(args.csvfile)
    
    # column names to lower case and strip extra spaces
    df.columns = [col.strip().lower() for col in df.columns]
    
     # removing any rows where 'year' if not numeric 
    df = df[pd.to_numeric(df['year'], errors='coerce').notnull()]
    
    # creating a new 'Date' column by combining year and month and parse it into datetime.
    df['Date'] = pd.to_datetime(df['year'].astype(str) + ' ' + df['month'], format='%Y %B')
    
    # sort the DataFrame by the Date column
    df.sort_values('Date', inplace=True)
    
    # Plotting the data
    plt.figure(figsize=(12, 6))
    
    plt.plot(df['Date'], df['packet_count'], linestyle='-', color='blue')
    plt.title('Packets 376 bytes, port 1433 and 1434 2005-2024')
    plt.xlabel('Date')
    plt.ylabel('Packet Count')
    plt.grid(True)
    
    # seting the x-axis limits to match the data range
    plt.xlim(df['Date'].min(), df['Date'].max())
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
