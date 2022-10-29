from bs4 import BeautifulSoup
import datetime
import json
import math
import numpy as np
import os
import pandas as pd
import random
import re
import requests
import time
import urllib.request

from admin import print_progress
from admin import reset_df
from admin import retrieve_df
from admin import retrieve_json
from admin import retrieve_path
from admin import  retrieve_ref
from admin import save_df
from admin import save_json

from list_trials import list_location
from write_geojson import calculate_color
from write_geojson import find_date


def sankey_count():
    """
    create year_counts_pdf.csv
    create year_counts_cdf.csv
    """

    # save a count of tissue sources as a df
    #count_sources()

    # list groups as sankey json
    write_json('count')
    write_json('enroll')


def unique_items(items):
    """
    return list
    """
    uniques = []
    for item in items:
        if item in uniques: continue
        uniques.append(item)
    return(uniques)


def write_json(type):
    """
    write json describing groups
    """

    lines = []

    df = retrieve_df('tissue_source_count')

    col1 = 'Source'
    col2 = 'TissueSource'
    col3 = 'Status'
    col4 = 'Phases'


    for line in write_line(df, col1, col2, type):
        lines.append(line)

    for line in write_line(df, col2, col4, type):
        lines.append(line)

    fil_dst = retrieve_path('sankey_data_count')
    if type == 'count': fil_dst = retrieve_path('sankey_data_count')
    if type == 'enroll': fil_dst = retrieve_path('sankey_data_enroll')


    # write the lines to a javascript file
    f = open(fil_dst, "w")
    f.write('var sankey_data_' + type + ' = [' + '\n')
    for line in lines:
        f.write(line + '\n')
    f.write('\n' + '];')
    f.close()


def write_line(df, col1, col2, type):
    """
    return list of lines
    """

    lines = []

    for item1 in unique_items(list(df[col1])):

        for item2 in unique_items(list(df[col2])):

            df_temp = df
            df_temp = df_temp[df_temp[col1] == item1]
            df_temp = df_temp[df_temp[col2] == item2]

            col = 'Enrollment'
            trial_count = len(list(df_temp[col]))
            enroll_count = sum(list(df_temp[col]))
            #print(col + ' ' + str(trial_count))

            coded_count = trial_count
            if type == 'enroll': coded_count = enroll_count


            if np.isnan(coded_count): continue
            if coded_count == np.nan: continue
            if item1 == item2: continue

            line = '{from: "' + str(item1) + '", to: "' + str(item2)
            line = line + '", weight: ' + str(coded_count ) + '},'
            print(line)
            lines.append(line)

    return(lines)


def retrieve_source_group(trial):
    """
    return group
    """

    url = trial['URL']

    df = retrieve_df('groups')
    df = df[df['url'] == url]
    del df['all']
    del df['url']

    for col in df.columns:
        if list(df[col])[0] == 1:

            if 'allo' == col: return('allogeneic')
            if 'auto' == col: return('autologous')
            return(col)


def count_sources():
    """
    count sources
    """
    trials =  retrieve_json('trials')['trials']
    df_all = pd.DataFrame()

    for trial in trials:

        df = pd.DataFrame()
        df['url'] = [trial['URL']]
        df['Status'] = [trial['Status']]
        df['Phases'] = [trial['Phases']]
        df['Source'] = [retrieve_source_group(trial)]
        df['Enrollment'] = [trial['Enrollment']]


        for file in os.listdir(retrieve_path('tissue_type_terms')):

            col_name = file.split('.')[0]
            df[col_name] = [0]

            source_tissue = ''
            fil_src = os.path.join(retrieve_path('tissue_type_terms'), file)
            if term_found(trial, fil_src) == True:
                enroll = float(trial['Enrollment'])
                df[col_name] = [1]

                source_tissue = source_tissue + ' ' + col_name
                df['TissueSource'] = source_tissue



        df_all = df_all.append(df)
        trials_found = len(list(df_all['url']))
        print('trials_found = ' + str(trials_found))
        save_df(df_all, 'tissue_source_count', 'Status')


def term_found(trial, fil_src):
    """
    return True if found
    """

    desc = str(trial['desc']).lower()

    terms = list(retrieve_df(fil_src)['term'])
    for term in terms:

        term = str(term).lower()
        if term in desc:
            return(True)

    return(False)
