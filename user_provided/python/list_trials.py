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

from pytrials.client import ClinicalTrials
from build_dataset import clinicaltrials_query


from admin import reset_df
from admin import retrieve_df
from admin import retrieve_path
from admin import retrieve_json
from admin import save_json
from admin import save_value


def list_trials():
    """
    Objective
    Map clinical trials
    """

    tasks = [0, 1, 2, 3, 4]

    time_begin = datetime.datetime.today()
    print('begin list_df ' + str(time_begin))
    if 0 in tasks: list_df()
    print('trials found = ' + str(len(list(retrieve_df('trials_all_archive')['URL']))))

    time_begin = datetime.datetime.today()
    print('begin list_df ' + str(time_begin))
    if 1 in tasks: list_included()
    print('trials found = ' + str(len(list(retrieve_df('trials_all')['URL']))))

    print('begin list_json ' + str(datetime.datetime.today()))
    if 2 in tasks: list_json()
    print('completed list_json ' + str(datetime.datetime.today()))

    print('begin list_locations ' + str(datetime.datetime.today()))
    if 3 in tasks: list_locations()
    print('completed list_locations ' + str(datetime.datetime.today()))


def list_df():
    """
    create csv
    """

    time_begin = datetime.datetime.today()
    print('begin list_trials ' + str(time_begin))

    df_all = retrieve_df('scraped_trials_df')
    save_value('scraped trials count', len(list(df_all['URL'])))

    src = retrieve_path('clinical_src')
    for file in os.listdir(src):

        df = retrieve_df(os.path.join(src, file))
        del df['Rank']

        for url in list(df['URL']):

            known_urls = list(df_all['URL'])

            if url in known_urls: continue

            nctid = str(url.split('/')[-1])
            clinicaltrials_query(nctid)

            df_url = df[df['URL'] == url]
            df_all = df_all.append(df_url)
            df_all = df_all.drop_duplicates(subset = "URL", keep='first')
            df_all = reset_df(df_all.sort_values(by='Enrollment', ascending=False))
            df_all.to_csv(retrieve_path('trials_all_archive'))

        print('trials found = ' + str(len(list(retrieve_df('trials_all_archive')['URL']))))
        save_value('scraped + downloaded trials count', len(list(df_all['URL'])))


def list_included():
    """
    list only trials that pass an exclusion test
    """
    append_list('trials_removed', 'reset')
    build_included_df('reset')

    # retrieve all found trials
    df = retrieve_df('trials_all_archive')
    nums = list(df['NCT Number'])

    for num in nums:

        i = nums.index(num)
        url = df.at[i, 'URL']
        desc = df.at[i, 'desc']

        print('url = ' + str(url))

        # do not append the trial, if it is listed in te "excluded trial" list
        if specified_excluded(url) == True:
            append_list('trials_removed', url)
            continue

        # do not append the trial, if keywords are not found in the title, summary, or intervention
        if keyword_found(desc) == False:
            append_list('trials_removed', url)
            continue

        df_temp = df[df['NCT Number'] == num]
        build_included_df(df_temp)


def keyword_found(desc):
    """
    return True is keyword found
    else False
    """

    print(np.isnan(np.inf))
    if pd.isnull(desc) == True: return(False)
    desc = str(desc).lower()
    #if np.isnan(desc) == True: return(False)

    mandatory_terms = ['mesenchymal', 'msc', 'prochymal']
    mandatory_terms.append('bone marrow cells')
    mandatory_terms.append('ALLO-ASC-SHEET')
    mandatory_terms.append('FANCA Gene Transfer for Fanconi Anemia Using a High-safety')
    mandatory_terms.append('gene transfer for ada-scid using an improved lentiviral vector (tyf-ada) gene transfer for adenosine deaminase-severe combined immunodeficiency')
    mandatory_terms.append('autologous adipose-derived stromal cells delivered intra-articularly in patients with osteoarthritis. an open-label, non-randomized, multi-center study ')
    mandatory_terms.append('3d tissue engineered bone equivalent for treatment of traumatic bone defects safety and efficacy study of traumatic bone defects treatment with use of')
    mandatory_terms.append('FURESTEM-CD Inj.')
    mandatory_terms.append('Bone Marrow Stem Cells')
    mandatory_terms.append('AVB-114')
    mandatory_terms.append('NeoFuse')
    mandatory_terms.append('bone marrow derived mesenchymal stem cells')
    mandatory_terms.append('adipose tissue derived stromal cells')
    mandatory_terms.append('Ex Vivo Expansion of Umbilical Cord Blood')
    mandatory_terms.append('AlloStem')

    for mandatory_term in mandatory_terms:
        #print('mandatory_term = ' + str(mandatory_term))
        mandatory_term = str(mandatory_term)
        #print('mandatory_term = ' + str(mandatory_term))
        mandatory_term = mandatory_term.lower()
        #print('mandatory_term = ' + str(mandatory_term))
        #print('desc = ')
        #print(desc)
        if mandatory_term in desc:
            return(True)

    return(False)


def specified_excluded(url):
    """
    return True if found in excluded list
    """

    excluded = list(retrieve_df('excluded_trials')['url'])
    assert len(excluded) > 1

    if url in excluded: return(True)

    for item in excluded:

        url_id = str(url.split('/')[-1])
        excluded_id = str(item.split('/')[-1])

        if str(url_id) in str(excluded_id):
            print('listed_excluded url = ' + str(item))
            print('url = ' + str(url))
            return(True)

    return(False)


def build_included_df(df_temp):
    """
    append trial that passed inclusion check
    """

    try:
        if df_temp == 'reset':
            print('reset')
            if os.path.exists(retrieve_path('trials_all')):
                os.remove(retrieve_path('trials_all'))
            return()
    except:
        df_temp = df_temp

    try:
        df = retrieve_df('trials_all')
        df = df.append(df_temp)
    except:
        df = df_temp

    try:
        df = reset_df(df.sort_values(by='Enrollment'))
    except:
        print(df)
        df = reset_df(df)

    df.to_csv(retrieve_path('trials_all'))


def append_list(path, value):
    """
    list found values
    """

    if value == 'reset':
        df = pd.DataFrame()
        df['term'] = []
        df.to_csv(retrieve_path(path))
        return()

    try:
        df = retrieve_df(path)
        df = df[df['term'] != value]

    except:
        df = pd.DataFrame()
        df['term'] = []

    df_temp = pd.DataFrame()
    df_temp['term'] = [value]
    df = df.append(df_temp)
    df = reset_df(df.sort_values(by='term'))
    df.to_csv(retrieve_path(path))

    save_value('trials removed for applicability', len(list(df['term'])))


def list_json():
    """
    save csv
    """

    trials = []
    df_all = retrieve_df('trials_all')

    items = list(df_all['NCT Number'])
    for item in items:

        i = items.index(item)

        trial = {}

        for col in df_all.columns:

            if col == 'Rank': continue

            value = df_all.at[i, col]

            if 'Condition' in col:
                value = scrub_conditions(value)

            trial[col] = str(value)

        if trial in trials:
            #print('duplicate found: ')
            #print(trial)
            continue

        trials.append(trial)

        trials_dict = {}
        trials_dict['item_count'] = len(trials)
        trials_dict['trials'] = trials
        save_json(trials_dict, 'trials')

        print('trials json-ed = ' + str(len(trials)))
        save_value('json-ed trials', len(trials))


    time_end = datetime.datetime.today()
    print('completed list_trials ' + str(time_end))


def scrub_conditions(value):
    """
    return value
    """

    #print('value = ')
    #print(value)

    value = str(value)
    if value == 'nan': return(value)
    if pd.isna(value) == True: return(value)

    if 'Knee Osteoarthritis' == value:
        #print('value = ')
        #print(value)
        value = str('Osteoarthritis, Knee')

    if 'Covid19' == value or "Corona Virus Disease 2019(COVID-19)" == value or "COVID" == value or "Covid 19" == value or "Coronavirus Infection" == value or "Coronavirus Disease 2019 (COVID-19) Pneumonia" == value  or 'Corona Virus Infection|Covid19' == value:
        #print('value = ')
        #print(value)
        value = str('COVID-19')

    if 'Acute Myocardial Infarction' == value:
        #print('value = ')
        #print(value)
        value = str('Myocardial Infarction')

    if 'Crohn Disease' == value:
        #print('value = ')
        #print(value)
        value = str('Crohn\'s Disease')

    if 'Spinal Cord Injuries' == value:
        #print('value = ')
        #print(value)
        value = str('Spinal Cord Injury')

    return(value)


def list_locations():
    """
    create list of locations
    locations.csv
    """

    locations = []

    trials = retrieve_json('trials')['trials']

    print('trials found: ' + str(len(trials)))

    for trial in trials:

        location = trial['Locations']

        print('location = ')
        print(location)

        location_list = list_location(location)

        for item in location_list:

            if item in locations: continue
            locations.append(item)

        df = pd.DataFrame()
        df['location'] = locations
        df = reset_df(df.sort_values(by='location'))
        df.to_csv(retrieve_path('location'))

        save_value('location unique count', len(list(df['location'])))


def list_location(location):
    """
    return a list of locations
    """

    location_list = []

    if '|' in location:

        loc = location.split('|')

        for item in loc:
            if item in location_list: continue
            location_list.append(item)

    else:
        location_list = [location]

    return(location_list)
