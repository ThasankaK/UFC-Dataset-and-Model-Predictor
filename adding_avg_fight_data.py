

import pandas as pd
from datetime import datetime
import os 
import csv
import numpy as np


ufc_fighters = pd.read_csv('ufc_fighters.csv')

ufc_fighters['avg_knockdowns'] = pd.NA
ufc_fighters['avg_sig_strike_atts'] = pd.NA
ufc_fighters['avg_sig_strikes'] = pd.NA
ufc_fighters['avg_tot_strike_atts'] = pd.NA
ufc_fighters['avg_tot_strikes'] = pd.NA
ufc_fighters['avg_takedown_atts'] = pd.NA
ufc_fighters['avg_takedowns'] = pd.NA
ufc_fighters['avg_clinch_atts'] = pd.NA
ufc_fighters['avg_clinchs'] = pd.NA
ufc_fighters['avg_ctrl_time'] = pd.NA
ufc_fighters['avg_fight_time'] = pd.NA
ufc_fighters['avg_submissions'] = pd.NA
ufc_fighters['avg_reversals'] = pd.NA
ufc_fighters['avg_head_strike_atts'] = pd.NA
ufc_fighters['avg_head_strike'] = pd.NA
ufc_fighters['avg_body_strike_atts'] = pd.NA
ufc_fighters['avg_body_strikes'] = pd.NA
ufc_fighters['avg_leg_strike_atts'] = pd.NA
ufc_fighters['avg_leg_strikes'] = pd.NA
ufc_fighters['avg_dist_strike_atts'] = pd.NA
ufc_fighters['avg_dist_strikes'] = pd.NA
ufc_fighters['avg_ground_atts'] = pd.NA
ufc_fighters['avg_grounds'] = pd.NA


fighter_ids = ufc_fighters['fighter_id'].tolist()

for id in fighter_ids:
    ufc_event_fight_stats = pd.read_csv('ufc_event_fight_stats.csv')

    filtered_df = ufc_event_fight_stats[(ufc_event_fight_stats['f1_id'] == id) | (ufc_event_fight_stats['f2_id'] == id)]

    f1_id = False
    f2_id = False

    knockdown_count = 0 
    sig_strike_atts_count = 0
    sig_strike_count = 0

    tot_strike_atts_count = 0
    tot_strike_count = 0

    takedown_atts_count = 0
    takedowns_count = 0 

    submissions_count = 0
    reversals_count = 0

    ctrl_time = 0

    head_strike_atts_count = 0
    head_strike_count = 0 

    body_strike_atts_count = 0
    body_strike_count = 0

    leg_strike_atts_count = 0
    leg_strike_count = 0 

    dist_strike_atts_count = 0
    dist_strike_count = 0

    clinch_atts_count = 0
    clinch_count = 0

    ground_atts_count = 0
    ground_count = 0

    tot_fight_time = 0 

    fight_counts = 0 

    for row in filtered_df.itertuples(index=False):
        if row.f1_id == id:
            f1_id = True
        elif row.f2_id == id:
            f2_id = True
 

        knockdown_count +=  row.f1_knockdowns if f1_id == True else row.f2_knockdowns
        sig_strike_atts_count += row.f1_sig_strike_atts if f1_id == True else row.f2_sig_strike_atts
        sig_strike_count += row.f1_sig_strikes if f1_id == True else row.f2_sig_strikes

        tot_strike_atts_count += row.f1_tot_strike_atts if f1_id == True else row.f2_tot_strike_atts
        tot_strike_count += row.f1_tot_strikes if f1_id == True else row.f2_tot_strikes

        takedown_atts_count += row.f1_takedown_atts if f1_id == True else row.f2_takedown_atts
        takedowns_count += row.f1_takedowns if f1_id == True else row.f2_takedowns

        clinch_atts_count += row.f1_clinch_atts if f1_id == True else row.f1_clinch_atts
        clinch_count += row.f1_clinchs if f1_id == True else row.f2_clinchs

        submissions_count += row.f1_submissions if f1_id == True else row.f2_submissions
        reversals_count += row.f1_reversals if f1_id == True else row.f2_reversals

        head_strike_atts_count += row.f1_head_strike_atts if f1_id == True else row.f2_head_strike_atts
        head_strike_count += row.f1_head_strikes if f1_id == True else row.f2_head_strikes

        body_strike_atts_count += row.f1_body_strike_atts if f1_id == True else row.f2_body_strike_atts
        body_strike_count += row.f1_body_strikes if f1_id == True else row.f2_body_strikes


        leg_strike_atts_count += row.f1_leg_strike_atts if f1_id == True else row.f2_leg_strike_atts
        leg_strike_count += row.f1_leg_strikes if f1_id == True else row.f2_leg_strikes
        
        dist_strike_atts_count += row.f1_dist_strike_atts if f1_id == True else row.f2_dist_strike_atts
        dist_strike_count += row.f1_dist_strikes if f1_id == True else row.f2_dist_strikes
        
        ctrl_time += row.f1_ctrl_time if f1_id == True else row.f2_ctrl_time
        tot_fight_time += row.total_fight_time

        ground_atts_count += row.f1_ground_atts if f1_id == True else row.f2_ground_atts
        ground_count += row.f1_grounds if f1_id == True else row.f2_grounds

        fight_counts += 1

    if fight_counts == 0:
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_knockdowns'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_sig_strike_atts'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_sig_strikes'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_tot_strike_atts'] =  0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_tot_strikes'] =  0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_takedown_atts']  =  0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_takedowns'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_clinch_atts'] =  0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_clinchs'] =0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_fight_time'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_ctrl_time'] =0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_submissions'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_reversals'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_head_strike_atts'] =  0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_head_strike'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_body_strike_atts'] =0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_body_strikes'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_leg_strike_atts'] =0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_leg_strikes'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_dist_strike_atts'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_dist_strikes'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_ground_atts'] = 0
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_grounds'] = 0

    else:

        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_knockdowns'] = knockdown_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_sig_strike_atts'] = sig_strike_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_sig_strikes'] = sig_strike_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_tot_strike_atts'] =  tot_strike_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_tot_strikes'] =  tot_strike_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_takedown_atts']  =  takedown_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_takedowns'] = takedowns_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_clinch_atts'] =  clinch_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_clinchs'] = clinch_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_fight_time'] = tot_fight_time / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_ctrl_time'] = ctrl_time / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_submissions'] = submissions_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_reversals'] = reversals_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_head_strike_atts'] =  head_strike_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_head_strikes'] = head_strike_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_body_strike_atts'] = body_strike_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_body_strikes'] = body_strike_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_leg_strike_atts'] = leg_strike_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_leg_strikes'] = leg_strike_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_dist_strike_atts'] = dist_strike_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_dist_strikes'] = dist_strike_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_ground_atts'] = ground_atts_count / fight_counts
        ufc_fighters.loc[ufc_fighters['fighter_id'] == id, 'avg_grounds'] = ground_count / fight_counts



    # Save the updated DataFrame back to the CSV file
    ufc_fighters.to_csv('ufc_fighters.csv', index=False)
        




