
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os 
import csv


# Load the CSV file into a DataFrame
ufc_events = pd.read_csv('ufc_events.csv')

if os.path.exists('ufc_event_fight_stats.csv'):
    ufc_event_fights = pd.read_csv('ufc_event_fight_stats.csv')
    written_fight_event_urls = ufc_event_fights['event_url'].tolist()
else:
    ufc_event_fights = pd.DataFrame()
    written_fight_event_urls = []

ufc_event_urls = ufc_events['url_link'].tolist()
#print(written_fight_event_urls)
limit = 0
for url in ufc_event_urls:
    if limit == 200:
        break


    if url not in written_fight_event_urls:
        updated_ufc_event_fights = None
        limit += 1
        print(url)

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            exit()  
            
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        

        # Find all event blocks on the page
        event_blocks = soup.find_all('a', class_='b-flag')

        # Extract the href attribute from each link
        hrefs = [link['href'] for link in event_blocks]


        fighter_stats = pd.read_csv('ufc_fighters.csv')
        hrefs = set(hrefs)
        for href in hrefs:
            i = 0
            event_fight_data = {}   
    
           

            event_fight_data['fights_url'] = href
            event_fight_data['event_url'] = url


            response = requests.get(href)


            if response.status_code != 200:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
                exit()  
            result_box = None
            soup = BeautifulSoup(response.content, 'html.parser')
            fighter_names = soup.find_all('a', class_="b-link b-link_style_black")
            test = soup.find_all('section', class_='b-fight-details__section js-fight-section')
            if test[0].get_text(strip=True) == "Round-by-round stats not currently available.":
                break
        
        
            f1_name = fighter_names[0].get_text(strip=True)
            f2_name = fighter_names[1].get_text(strip=True)
        
            event_fight_data['f1_name'] = f1_name
            event_fight_data['f2_name'] = f2_name

            winner_box = soup.find_all('i', class_='b-fight-details__person-status b-fight-details__person-status_style_green')
            weight_class_tag = soup.find_all('i', class_='b-fight-details__fight-title')
            weight_class = weight_class_tag[0].get_text(strip=True)
        
            for word in weight_class.split():
        
                if "weight" in word:
                
                    weight_class = word
                    break
            
        

            event_fight_data['weight_class'] = weight_class


            if winner_box:


                for html in winner_box:
                    next_sibling = html.find_next_sibling('div')   
                    name_tag = next_sibling.find('h3', class_='b-fight-details__person-name')
                    winner_name = name_tag.get_text(strip=True)
                    break

                winner_fighter = fighter_stats[fighter_stats['fighter_name'] == winner_name]
                event_fight_data['result'] = winner_fighter['fighter_id'].tolist()[0]
            
            else:
                result_box = soup.find_all('i', class_='b-fight-details__person-status b-fight-details__person-status_style_gray')
        
                if result_box:
                    result = result_box[0].text.strip()
                    
                    if result == "D":
                        event_fight_data['result'] = "d"
                    elif result == "NC":
                        event_fight_data['result'] = "nc"
            

            f1 = fighter_stats[fighter_stats['fighter_name'] == f1_name]
            f2 = fighter_stats[fighter_stats['fighter_name'] == f2_name]
            


            event_fight_data['f1_id'] = f1['fighter_id'].tolist()[0]
            event_fight_data['f2_id'] = f2['fighter_id'].tolist()[0]

            
            totals_stats = soup.find_all('p', class_='b-fight-details__table-text')



            f1_knockdown = totals_stats[2].get_text(strip=True)
            f2_knockdown = totals_stats[3].get_text(strip=True)
            event_fight_data['f1_knockdowns'] = f1_knockdown
            event_fight_data['f2_knockdowns'] = f2_knockdown

    
            f2_sig_strikes = totals_stats[5].get_text(strip=True)
            f1_sig_strikes = totals_stats[4].get_text(strip=True)
            event_fight_data['f1_sig_strike_atts'] = int(f1_sig_strikes.split()[-1])
            event_fight_data['f1_sig_strikes'] = int(f1_sig_strikes.split()[0])
            event_fight_data['f2_sig_strike_atts'] = int(f2_sig_strikes.split()[-1])
            event_fight_data['f2_sig_strikes'] = int(f2_sig_strikes.split()[0])

            f1_total_strikes = totals_stats[8].get_text(strip=True)
            f2_total_strikes = totals_stats[9].get_text(strip=True)

            event_fight_data['f1_tot_strike_atts'] = int(f1_total_strikes.split()[-1])
            event_fight_data['f1_tot_strikes'] = int(f1_total_strikes.split()[0])
            event_fight_data['f2_tot_strike_atts'] = int(f2_total_strikes.split()[-1])
            event_fight_data['f2_tot_strikes'] = int(f2_total_strikes.split()[0])

            f1_takedowns = totals_stats[10].get_text(strip=True)
            f2_takedowns = totals_stats[11].get_text(strip=True)

            event_fight_data['f1_takedown_atts'] = int(f1_takedowns.split()[-1])
            event_fight_data['f1_takedowns'] = int(f1_takedowns.split()[0])
            event_fight_data['f2_takedown_atts'] = int(f2_takedowns.split()[-1])
            event_fight_data['f2_takedowns'] = int(f2_takedowns.split()[0])
        

            f1_submissions = totals_stats[14].get_text(strip=True)
            f2_submissions = totals_stats[15].get_text(strip=True)
            event_fight_data['f1_submissions'] = int(f1_submissions)
            event_fight_data['f2_submissions'] = int(f2_submissions)

            f1_reversals = totals_stats[16].get_text(strip=True)
            f2_reversals = totals_stats[17].get_text(strip=True)
            event_fight_data['f1_reversals'] = int(f1_reversals)
            event_fight_data['f2_reversals'] = int(f2_reversals)

            f1_control_time = totals_stats[18].get_text(strip=True)
            f2_control_time = totals_stats[19].get_text(strip=True)
            if f1_control_time == "--":
                event_fight_data['f1_ctrl_time'] = None 
            else:
                f1_minutes = int(f1_control_time.split(':')[0])
                f1_seconds = int(f1_control_time.split(':')[-1])
                event_fight_data['f1_ctrl_time'] = f1_minutes*60 + f1_seconds
            if f2_control_time == "--":
                event_fight_data['f2_ctrl_time'] = None
            else:

                f2_minutes = int(f2_control_time.split(':')[0])
                f2_seconds = int(f2_control_time.split(':')[-1])
                event_fight_data['f2_ctrl_time'] = f2_minutes*60 + f2_seconds

        
            sig_strike_section = soup.find_all('p')
            for html in sig_strike_section:
                if html.get_text(strip=True) == "Significant Strikes":
                    break
                i += 1
        
            
            f1_head_strikes = sig_strike_section[i+7].get_text(strip=True)
            f2_head_strikes = sig_strike_section[i+8].get_text(strip=True)

            event_fight_data['f1_head_strike_atts'] = int(f1_head_strikes.split()[-1])
            event_fight_data['f1_head_strikes'] = int(f1_head_strikes.split()[0])
            event_fight_data['f2_head_strike_atts'] = int(f2_head_strikes.split()[-1])
            event_fight_data['f2_head_strikes'] = int(f2_head_strikes.split()[0])

            f1_body_strikes = sig_strike_section[i+9].get_text(strip=True)
            f2_body_strikes = sig_strike_section[i+10].get_text(strip=True)

            event_fight_data['f1_body_strike_atts'] = int(f1_body_strikes.split()[-1])
            event_fight_data['f1_body_strikes'] = int(f1_body_strikes.split()[0])
            event_fight_data['f2_body_strike_atts'] = int(f2_body_strikes.split()[-1])
            event_fight_data['f2_body_strikes'] = int(f2_body_strikes.split()[0])

            f1_leg_strikes = sig_strike_section[i+11].get_text(strip=True)
            f2_leg_strikes = sig_strike_section[i+12].get_text(strip=True)

            event_fight_data['f1_leg_strike_atts'] = int(f1_leg_strikes.split()[-1])
            event_fight_data['f1_leg_strikes'] = int(f1_leg_strikes.split()[0])
            event_fight_data['f2_leg_strike_atts'] = int(f2_leg_strikes.split()[-1])
            event_fight_data['f2_leg_strikes'] = int(f2_leg_strikes.split()[0])

            # this is such a poorly made stat or I have no understanding of it
            f1_distance = sig_strike_section[i+13].get_text(strip=True)
            f2_distance = sig_strike_section[i+14].get_text(strip=True)
            event_fight_data['f1_dist_strike_atts'] = int(f1_distance.split()[-1])
            event_fight_data['f1_dist_strikes'] = int(f1_distance.split()[0])
            event_fight_data['f2_dist_strike_atts'] = int(f2_distance.split()[-1])
            event_fight_data['f2_dist_strikes'] = int(f2_distance.split()[0])
            

            f1_clinch = sig_strike_section[i+15].get_text(strip=True)
            f2_clinch = sig_strike_section[i+16].get_text(strip=True)

            event_fight_data['f1_clinch_atts'] = int(f1_clinch.split()[-1])
            event_fight_data['f1_clinchs'] = int(f1_clinch.split()[0])
            event_fight_data['f2_clinch_atts'] = int(f2_clinch.split()[-1])
            event_fight_data['f2_clinchs'] = int(f2_clinch.split()[0])


            f1_ground = sig_strike_section[i+17].get_text(strip=True)
            f2_ground = sig_strike_section[i+18].get_text(strip=True)


            event_fight_data['f1_ground_atts'] = int(f1_ground.split()[-1])
            event_fight_data['f1_grounds'] = int(f1_ground.split()[0])
            event_fight_data['f2_ground_atts'] = int(f2_ground.split()[-1])
            event_fight_data['f2_grounds'] = int(f2_ground.split()[0])

            
            event_fight_data_df = pd.DataFrame([event_fight_data])
            updated_ufc_event_fights = pd.concat([ufc_event_fights, event_fight_data_df], ignore_index=True)
            
        
            




            if not updated_ufc_event_fights.empty:
                # Reorder columns
                df = updated_ufc_event_fights[['f1_id', 'f2_id', 'f1_name', 'f2_name', 'weight_class', 'f1_knockdowns', 'f2_knockdowns', 'f1_sig_strike_atts', 'f1_sig_strikes',
                        'f2_sig_strike_atts', 'f2_sig_strikes', 'f1_tot_strike_atts', 'f1_tot_strikes','f2_tot_strike_atts', 'f2_tot_strikes',
                        'f1_takedown_atts','f1_takedowns', 'f2_takedown_atts', 'f2_takedowns', 'f1_submissions', 'f2_submissions',
                        'f1_reversals', 'f2_reversals', 'f1_ctrl_time', 'f2_ctrl_time', 'f1_head_strike_atts', 'f1_head_strikes',
                        'f2_head_strike_atts', 'f2_head_strikes', 'f1_body_strike_atts', 'f1_body_strikes', 'f2_body_strike_atts', 'f2_body_strikes',
                        'f1_leg_strike_atts','f1_leg_strikes', 'f2_leg_strike_atts', 'f2_leg_strikes', 'f1_dist_strike_atts', 'f1_dist_strikes',
                        'f2_dist_strike_atts', 'f2_dist_strikes', 'f1_clinch_atts', 'f1_clinchs', 'f2_clinch_atts', 'f2_clinchs',
                        'f1_ground_atts', 'f1_grounds', 'f2_ground_atts', 'f2_grounds', 'result', 'fights_url', 'event_url']]
               
                df.to_csv('ufc_event_fight_stats.csv', index=False)

            ufc_event_fights = pd.read_csv('ufc_event_fight_stats.csv')

print("Data has been scraped and saved to 'ufc_event_fight_stats.csv'.")

