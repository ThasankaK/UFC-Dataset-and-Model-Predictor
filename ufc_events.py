import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URL of the UFC events page
url = 'http://www.ufcstats.com/statistics/events/completed?page=all'

# Fetch the web page content
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract event data
events = []

# Find all event blocks on the page
event_blocks = soup.find_all('tr', class_='b-statistics__table-row')

# Initialize event ID counter
event_id_counter = 1

for event in event_blocks:
    event_data = {}
    
    columns = event.find_all('td')
    
    for values in columns:
        link_tag = values.find('a')
        date_tag = values.find('span')
        
        if link_tag:
            event_data['event_name'] = link_tag.text.strip()
            event_data['url_link'] = link_tag['href'].strip()
        
        if date_tag:
            # Extract and format date
            raw_date = date_tag.text.strip()
            try:
                # Parse the date
                date_obj = datetime.strptime(raw_date, '%B %d, %Y')
                # Format the date
                formatted_date = date_obj.strftime('%Y-%m-%d')
                event_data['event_date'] = formatted_date
            except ValueError as e:
                print(f"Date parsing error: {e}")
                event_data['event_date'] = raw_date  # Keep raw date in case of error
    
    # Append event data only if we have the name and URL
    if 'event_name' in event_data and 'url_link' in event_data:
        event_data['event_id'] = event_id_counter
        events.append(event_data)
        event_id_counter += 1

# Create a DataFrame from the extracted data
df = pd.DataFrame(events)

# Reorder columns
df = df[['event_id', 'event_name', 'event_date', 'url_link']]

# Save to CSV file
df.to_csv('ufc_events.csv', index=False)

print("Data has been scraped and saved to 'ufc_events.csv'.")
