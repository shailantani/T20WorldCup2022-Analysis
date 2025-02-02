import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# URL of the page to scrape
url = "https://www.espncricinfo.com/records/tournament/batting-most-runs-career/indian-premier-league-2023-15129"

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
        
        # Extract text from each cell and append to data list
        row_data = [cell.get_text(strip=True) for cell in cells]
        data.append(row_data)
    
    # Define the file names for CSV and XLSX
    csv_file = 'batsmen_record.csv'
    xlsx_file = 'batsmen_record.xlsx'
    
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
