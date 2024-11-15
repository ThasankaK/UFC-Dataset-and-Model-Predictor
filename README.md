# UFC Dataset and Fight Predictor
Hello and welcome to my UFC Dataset and Fight Predictor, you can find more about this dataset and my fight predictor model at these Kaggle links

[UFC Dataset](https://www.kaggle.com/datasets/thasankakandage/ufc-dataset-2024/data)
[UFC Fight Predictor](https://www.kaggle.com/code/thasankakandage/ufc-fight-predictor)

- **`ufc_events.csv`** This keeps track of every single fight card that has taken place in the UFC with the following data, {event_id, event_name, event_date, url_link}.

- **`ufc_events.py`** This is the web scrapping code to attain `ufc_events.csv`, if an already existing `ufc_events.csv` is in your directory, you can run `ufc_events.py` to get the new events that are not in the dataset yet.

- **`ufc_fighters.csv`** This keeps track of stats of every fighter that has fought in the UFC. 

- **`ufc_fighters.py`** This is the web scrapping code to attain `ufc_fighters.csv`, if an already existing `ufc_fighters.csv` is in your directory, you **CAN** run it to get **NEW** fighters however this is **NOT** recommended. Instead you should delete the old .csv file and run the code to attain a completely new one, as this will have the up-to-date, adjusted stats for each fighter that has had new fights. 

The below link is an example of the fighter page that is being scrapped
http://www.ufcstats.com/fighter-details/749f572d1d3161fb 

- **`ufc_event_fight_stats.csv`** This keeps track of every single fight within every single UFC card and the stats for the fight. 

- **`ufc_event_fight_stats.py`** This is the web scrapping code to attain `ufc_event_fight_stats.csv`, if an already existing `ufc_event_fight_stats.py` is in your directory, you can run it again to get the new up-to-date event fights if there are unscrapped fights from new events in the `ufc_events.csv`. **YOU MUST** have `ufc_events.csv` and `ufc_fighters.csv` already existing in your directory to be able to run this code. 

The below link is an example of a fight detail page that is being scrapped
http://www.ufcstats.com/fight-details/33655fd07cfbe034 

- **`adding_(MEDIAN/AVG)_fight_data.csv`** This keeps track of stats of every fighter that has  fought in the UFC, similar to `ufc_fighters.csv`, but it also has median/average
stats taken from every fight the fighter has had.

- **`adding_(MEDIAN/AVG)_fight_data.py`** This is the web scrapping code to attain `adding_(MEDIAN_AVG)_fight_data.csv`. If you want to have an updated .csv you would have to rerun this file to get an entirely new .csv file. 
