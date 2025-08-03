import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse

def main():
    # set up argument like python3 scriptname.py 2005-port1433-1434/file2.csv
    parser = argparse.ArgumentParser(
        description='Plot time series data from a CSV file to make barchart')
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
    
    # Plotting the data as a bar chart
    plt.figure(figsize=(12, 6))
    
    
    plt.bar(df['Date'], df['packet_count'], color='red', width=18)
    plt.title('Packets 376 bytes, port 1433 and 1434 2005-2024')
    plt.xlabel('Date')
    plt.ylabel('Packet Count')
    plt.grid(True, axis='y')
    
    # seting the x-axis to show dates every 3 months in a readable format
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    
    # change font size
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    
    # seting x-axis limits slightly before min date for clear visibility
    plt.xlim(df['Date'].min() - pd.DateOffset(months=1), df['Date'].max())

    


    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
