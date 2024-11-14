import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os


def get_event_id():
    id = 1
    if os.path.exists("ufc_events.csv"):
        event_data = pd.read_csv("ufc_events.csv")
        event_ids = event_data['event_id'].tolist()
        while id in event_ids:
            id += 1
    
    return id

url = 'http://www.ufcstats.com/statistics/events/completed?page=all'


response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()


soup = BeautifulSoup(response.text, 'html.parser')


event_blocks = soup.find_all('tr', class_='b-statistics__table-row')


for event in event_blocks:

    if os.path.exists("ufc_events.csv"):
        csv_ufc_event_data = pd.read_csv("ufc_events.csv")
        written_urls = csv_ufc_event_data["url_link"].tolist()
    else:
        csv_ufc_event_data = pd.DataFrame()
        written_urls = []



    event_data = {}
    
    columns = event.find_all('td')
    
    for values in columns:
        link_tag = values.find('a')
        date_tag = values.find('span')
        
        if link_tag:
            event_data['event_name'] = link_tag.text.strip()
            if link_tag['href'].strip() in written_urls:
                break
            event_data['url_link'] = link_tag['href'].strip()
        
        if date_tag:
           
            raw_date = date_tag.text.strip()


            try:
          
                date_obj = datetime.strptime(raw_date, '%B %d, %Y')
              
                formatted_date = date_obj.strftime('%Y-%m-%d')
                event_data['event_date'] = formatted_date
            except ValueError as e:
                print(f"Date parsing error: {e}")
                event_data['event_date'] = raw_date  
    
    
    if 'event_name' in event_data and 'url_link' in event_data:
        event_data['event_id'] = get_event_id()


        event_data_df = pd.DataFrame([event_data])
        updated_event_df  = pd.concat([csv_ufc_event_data, event_data_df], ignore_index=True)

        df = updated_event_df[['event_id', 'event_name', 'event_date', 'url_link']]

        df.to_csv('ufc_events.csv', index=False)

