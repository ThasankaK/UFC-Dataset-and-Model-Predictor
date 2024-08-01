import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_more_info(fighter_info_url, soup):
    formatted_date = None
    stats={
        'SLpM:':None,
        'Str. Acc.:':None,
        'SApM:':None,
        'Str. Def:': None,
        'TD Avg.:': None,
        'TD Acc.:': None,
        'TD Def.:': None,
        'Sub. Avg.:': None
    }

    response = requests.get(fighter_info_url)


    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'html.parser')
        

        dob_element = soup.find('div', string='Date of Birth')
        if not dob_element:
        
            dob_element = soup.find('div', class_='b-list__info-box')
        
        if dob_element:
            
            dob_text = dob_element.get_text(strip=True)
            dob_text = dob_text.split("DOB:")[-1]
            if dob_text and dob_text != "--":

            
                date_obj = datetime.strptime(dob_text, '%b %d, %Y')

                formatted_date = date_obj.strftime('%Y-%m-%d')
                    
              
            else:
                formatted_date = None
            
        else:
            return None
        
        # Find the container with the career statistics
        stats_container = soup.find('div', class_='b-list__info-box b-list__info-box_style_middle-width js-guide clearfix')
        
        # Check if the container was found
        if stats_container:
            # Dictionary to hold the stats
            stats = {}
            
            # Extract stats from the left column
            left_stats = stats_container.find('div', class_='b-list__info-box-left clearfix').find_all('li', class_='b-list__box-list-item b-list__box-list-item_type_block')
            for stat in left_stats:
                label = stat.find('i', class_='b-list__box-item-title').get_text(strip=True)
                value = stat.get_text(strip=True).replace(label, '').strip()
                if value:
                    if '%' in value:
                        value = value.replace('%', '')
                        value = float(value)
                        value = value/100
                    else:
                        value = float(value)

                stats[label] = value
        
            right_stats = stats_container.find('div', class_='b-list__info-box-right b-list__info-box_style-margin-right').find_all('li', class_='b-list__box-list-item b-list__box-list-item_type_block')
            for stat in right_stats:
                label = stat.find('i', class_='b-list__box-item-title').get_text(strip=True)
                value = stat.get_text(strip=True).replace(label, '').strip()
                if value:
                    if '%' in value:
                        value = value.replace('%', '')
                        value = float(value)
                        value = value/100
                    else:
                        value = float(value)

                    stats[label] = value
            
            
        else:
            print("Career statistics container not found.")

        return formatted_date, stats['SLpM:'], stats['Str. Acc.:'], stats['SApM:'], stats['Str. Def:'], stats['TD Avg.:'], stats['TD Acc.:'], stats['TD Def.:'], stats['Sub. Avg.:']
    else:
        print("Failed to retrieve the webpage.")



fighters = []
alphabet = 'abcdefghijklmnopqrstuvwxyz'
fighter_id_counter = 1
for letter in alphabet:
    # url of the UFC fighters' statistics page
    url = f'http://www.ufcstats.com/statistics/fighters?char={letter}&page=all'


    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        exit()

    
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all fighter blocks on the page
    fighter_blocks = soup.find_all('tr', class_='b-statistics__table-row')

    # Initialize fighter ID counter
    
    for fighter in fighter_blocks:
        name = ""
        td_tag_count = 1
        a_tag_limit = 0 

        fighter_data = {}
        fighter_data['fighter_id'] = fighter_id_counter
        columns = fighter.find_all('td')
        if columns and not all(col['class'] == ['b-statistics__table-col_type_clear'] for col in columns): 
     
            for i, column in enumerate(columns):
              
                a_tag = column.find('a')
            
                if a_tag and a_tag_limit < 2:
                    
                    name += a_tag.text.strip() + " "
                    
            
                    url = a_tag['href'].strip()
                    fighter_data['fighter_name'] = name.strip()
                    fighter_data['fighter_url'] = url

                    fighter_data['fighter_dob'], \
                    fighter_data['fighter_slpm'], \
                    fighter_data['fighter_str_acc_%'], \
                    fighter_data['fighter_sapm'], \
                    fighter_data['fighter_str_def_%'], \
                    fighter_data['fighter_td_avg'], \
                    fighter_data['fighter_td_acc_%'], \
                    fighter_data['fighter_td_def_%'], \
                    fighter_data['fighter_sub_avg'] = get_more_info(url, soup)
                    
                    a_tag_limit += 1
                
                else:

                    if not a_tag:
                    
                        if td_tag_count == 1:
                            if column.text.strip() != "--" and column.text.strip() != "":
                                text = column.text.strip().replace('"',' ')
                                text = text.replace("'",'')
                                feet = int(text.split()[0])*12*2.54
                                inches = int(text.split()[1])*2.54
                                fighter_data['fighter_height_cm'] = round((feet + inches), 2)
                            else:
                                fighter_data['fighter_height_cm'] = None
                        elif td_tag_count == 2:
                            if column.text.strip() != "--":

                                fighter_data['fighter_weight_lbs'] = column.text.strip()[0:3]
                            else:
                                fighter_data['fighter_weight_lbs'] = None
                        elif td_tag_count == 3:
                            
                            if column.text.strip() != "--":
                                fighter_data['fighter_reach_cm'] = float(column.text.strip()[0:len(column.text.strip())-1]) * 2.54
                            else:
                                fighter_data['fighter_reach_cm'] = None
                        elif td_tag_count == 4:
                            fighter_data['fighter_stance'] = column.text.strip()
                        elif td_tag_count == 5:
                            fighter_data['fighter_wins'] = column.text.strip()
                        elif td_tag_count == 6:
                            fighter_data['fighter_losses'] = column.text.strip()
                        elif td_tag_count == 7:
                            fighter_data['fighter_draws'] = column.text.strip()

                        td_tag_count += 1
            #fighter_data['fighter_name'] = fighter_data['fighter_name'].strip()
            fighters.append(fighter_data)
            fighter_id_counter += 1


df_fighters = pd.DataFrame(fighters)

# reorder
df_fighters = df_fighters[['fighter_id', 'fighter_name', 'fighter_dob', 'fighter_height_cm', 'fighter_weight_lbs', 'fighter_reach_cm', 'fighter_stance',
                           'fighter_wins', 'fighter_losses', 'fighter_draws', 'fighter_slpm', 'fighter_str_acc_%', 'fighter_sapm',  'fighter_str_def_%', 
                           'fighter_td_avg', 'fighter_td_acc_%', 'fighter_td_def_%', 'fighter_sub_avg', 'fighter_url']]

df_fighters.to_csv('ufc_fighters.csv', index=False)

print("Fighter data has been scraped and saved to 'ufc_fighters.csv'.")
