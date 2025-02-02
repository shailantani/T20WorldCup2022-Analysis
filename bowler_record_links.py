import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from urllib.parse import urljoin

# URL of the page to scrape
url = "https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/indian-premier-league-2023-15129"

# Base URL for constructing complete links
base_url = "https://www.espncricinfo.com"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing the data
    table = soup.find('table', class_='ds-w-full ds-table ds-table-xs ds-table-auto ds-w-full ds-overflow-scroll ds-scrollbar-hide')
    
    # Check if the table is found
    if table is None:
        print("Table not found. Check if the class name is correct or if the webpage structure has changed.")
        exit()  # Exit the script
    
    # Initialize a list to store all the data
    data = []
    
    # Find all rows in the table body
    rows = table.find_all('tr')
    
    # Extract data from each row
    for row in rows:
        # Find all cells in the row
        cells = row.find_all(['td', 'th'])
        
        # Extract text from each cell
        row_data = [cell.get_text(strip=True) for cell in cells]
        
        # Extract link from the first cell (containing the bowler's name)
        link = cells[0].find('a')['href'] if cells[0].find('a') else ''
        
        # Construct complete URL
        full_link = urljoin(base_url, link)
        
        # Append complete link to row data
        row_data.append(full_link)
        
        # Append row data to the main data list
        data.append(row_data)
    
    # Define the file names for CSV and XLSX
    csv_file = 'bowling_records.csv'
    xlsx_file = 'bowling_records.xlsx'
    
    # Write data to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f"Data has been saved to {csv_file}")
    
    # Write data to XLSX file
    df = pd.DataFrame(data)
    df.to_excel(xlsx_file, index=False, header=False)
    print(f"Data has been saved to {xlsx_file}")
else:
    print("Failed to retrieve data from the URL")
