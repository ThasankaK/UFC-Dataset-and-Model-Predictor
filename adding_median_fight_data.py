import pandas as pd
from datetime import datetime
import os 
import csv
import numpy as np

ufc_fighters = pd.read_csv('ufc_fighters.csv')
ufc_event_fight_stats = pd.read_csv("ufc_event_fight_stats.csv")

stat_columns = [
    "knockdowns", "sig_strike_atts", "sig_strikes", "tot_strike_atts", "tot_strikes",
    "takedown_atts", "takedowns", "clinch_atts", "clinchs", "ctrl_time", "total_fight_time",
    "submissions", "reversals", "head_strike_atts", "head_strikes", "body_strike_atts",
    "body_strikes", "leg_strike_atts", "leg_strikes", "dist_strike_atts", "dist_strikes",
    "ground_atts", "grounds"
]

# create  new columns and initialize
for stat_column in stat_columns:
    ufc_fighters[f"median_{stat_column}"] = np.nan


for fighter_id in ufc_fighters["fighter_id"].unique():
    # new df will be rows where the fighter_id is either f1 or f2 
    filtered_df = ufc_event_fight_stats[(ufc_event_fight_stats["f1_id"] == fighter_id) | 
                                        (ufc_event_fight_stats["f2_id"] == fighter_id)]

    if filtered_df.empty:
        # no fights found
        for stat_column in stat_columns:
            ufc_fighters.loc[ufc_fighters["fighter_id"] == fighter_id, f"median_{stat_column}"] = 0
        continue


    for stat_column in stat_columns:
        f1_stat_column = f"f1_{stat_column}"
        f2_stat_column = f"f2_{stat_column}"


        stats_as_f1 = filtered_df[filtered_df["f1_id"] == fighter_id][f1_stat_column].values
        stats_as_f2 = filtered_df[filtered_df["f2_id"] == fighter_id][f2_stat_column].values

        
        all_stats_for_fighter = np.concatenate((stats_as_f1, stats_as_f2))
        median_stat = np.median(all_stats_for_fighter) if all_stats_for_fighter.size > 0 else 0

        # .loc(row selection, column selection) 
        ufc_fighters.loc[ufc_fighters["fighter_id"] == fighter_id, f"median_{stat_column}"] = median_stat


ufc_fighters.to_csv("ufc_fighters_median.csv", index=False)
