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
from admin import save_json
from admin import save_value

from list_trials import list_location


def write_geojson():
    """
    create geojson.json
    """

    time_begin = datetime.datetime.today()
    print('begin write_geojson ' + str(time_begin))

    df = retrieve_df('groups')
    for col in df.columns:

        print('col = ' + str(col))

        if 'url' == col: continue
        #if 'all' == col: continue

        df = retrieve_df('groups')
        df_new = df[df[col] > 0]
        urls = list(df_new['url'])
        print(len(urls))

        features = []
        features_recent = []

        trials = retrieve_json('trials')['trials']
        for trial in trials:

            if str(trial['URL']) not in urls: continue

            progress = round(trials.index(trial) / len(trials) * 100 , 3)
            print(col + ' ' + str(progress) + '% progress: i = ' + str(len(urls)))

            fillColor = calculate_color(col)
            #print('fillColor = ' + str(fillColor))

            locations = str(trial['Locations'])
            #print('locations = ' + str(locations))
            for loc in list_location(locations):

                #print('loc = ' + str(loc))

                feature = {}
                feature['type'] =  "Feature"
                feature['properties'] = write_prop(trial, loc, fillColor, col)
                feature['geometry'] = write_geo(loc)
                if feature['geometry'] == False: continue

                if feature in features: continue
                #print('feature = ')
                #print(feature)
                features.append(feature)

                features_dict = {}
                features_dict['feature_count'] = len(features)
                features_dict['type'] = ["FeatureCollection"]
                features_dict['features'] = features
                save_json(features_dict, 'geojson')

                # save the group as js
                dst_json = os.path.join(retrieve_path('js'), col + '.js')
                #print('dst_json = ' + str(dst_json))
                with open(dst_json, "w") as f:
                    f.write('var ' + ' group' + col + ' = ')
                    json.dump(features_dict, f, indent = 4)
                f.close()
                #print('dst_json = ' + str(dst_json))
                save_value('geojson entry count ' + col, len(features))

                year, month, day = find_date(trial)

                # save all trials
                if year < 2020: continue

                features_recent.append(feature)

                features_dict = {}
                features_dict['feature_count'] = len(features_recent)
                features_dict['type'] = ["FeatureCollection"]
                features_dict['features'] = features_recent

                # save the group as js
                dst_json = os.path.join(retrieve_path('js'), col + '_recent' + '.js')
                #print('dst_json = ' + str(dst_json))
                with open(dst_json, "w") as f:
                    f.write('var ' + ' group' + col + '_recent' + ' = ')
                    json.dump(features_dict, f, indent = 4)
                f.close()

                save_value('geojson entry count ' + col + '_recent', len(features_recent))
                save_value('geojson recent percent ' + col, round(len(features_recent)/len(features)*100,2))


    time_end = datetime.datetime.today()
    print('completed assign_groups ' + str(time_end))


def calculate_color(col):
    """
    determine color
    """

    if 'allo' in col: color = retrieve_ref('colorOrange')
    elif 'auto' in col: color = retrieve_ref('colorPurple')
    elif 'both' in col: color = retrieve_ref('colorBlueLight')
    elif 'undec' in col: color = retrieve_ref('colorGray')
    else: color = retrieve_ref('colorGray')


    r = color[0] + get_random_increment(col)
    if r > 1: r = 1
    if r < 0: r = 0
    r = int(255*r)

    g = color[1] + get_random_increment(col)
    if g > 1: g = 1
    if g < 0: g = 0
    g = int(255*g)


    b = color[2] + get_random_increment(col)
    if b > 1: b = 1
    if b < 0: b = 0
    b = int(255*b)

    color = 'rgb('  + str(r) + ', ' + str(g) + ', ' + str(b) + ')'

    return(color)


def get_random_increment(col):
    """
    return random increment
    """

    skip_terms = ['undec', '_pure']

    for term in skip_terms:

        if term in col:
            return(0)

    inc = (random.random()*10 - 5)/100
    return(inc)


def write_prop(trial, loc, fillColor, col):
    """
    return geojson for prop field
    """

    prop = {}

    # descriptors
    prop['name'] = trial['Title']
    prop['aff'] = loc
    prop['url'] = trial['URL']
    prop['status'] = trial['Status']

    try:
        prop['enrolled'] = int(float(trial['Enrollment']))
    except:
        prop['enrolled'] = 0

    # marker properties
    prop['radius'] = define_radius(trial)

    prop['color'] = "rgb(100, 100, 100)"
    prop['fillColor'] = fillColor


    status = trial['Status']
    preferred_status = ['Active, not recruiting', 'Available', 'Completed', 'Enrolling by invitation', 'Recruiting']
    if status in preferred_status:
        prop['opacity'] = 0.8
        prop['fillOpacity'] = 0.8
    else:
        print('Outside preferred status: ' + str(trial['URL']))
        prop['opacity'] = 0.4
        prop['fillOpacity'] = 0.4

    z_offset = 0
    if col == 'all': z_offset = 1
    if col == 'undeclared': z_offset = 2
    if col == 'auto': z_offset = 3
    if col == 'allo': z_offset = 4
    if col == 'both': z_offset = 5

    # z dimension
    zindex = int(9000 - int(prop['radius']) + 1000*z_offset)
    #if zindex < 0: zindex = 1
    #if zindex > 999: zindex = 999
    prop['zindex'] = int(zindex)
    prop['paneLabel'] = 'pane' + str(prop['zindex'])

    # animation times
    year, month, day = find_date(trial)
    date =  str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
    prop['start'] = date

    prop['end'] = "2023-09-30"

    return(prop)


def define_radius(trial):
    """
    return radius
    """

    #prop = write_prop(trial, '', '', '')

    #prop['radius'] = 10
    if 'Enrollment' in trial.keys():
        try:
            enrolled = int(float(trial['Enrollment']))
        except:
            print('no enrolled found: ')
            print(trial['URL'])
            enrolled = 0

    radius = int(math.sqrt(enrolled) + 10)

    return(radius)



def find_date(trial):
    """
    return a list of three numbers
    """

    year, month, day = 1900, 0, 0

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Sep', 'Oct', 'Nov', 'Dec']

    date_fields = ['Start Date', 'First Posted', 'Last Update Posted', 'Results First Posted']

    for field in date_fields:

        date = trial[field]

        date = re.sub(r'[^a-zA-z0-9\s_]+', ' ', date)
        date = date.split(' ')


        # find the year
        if date[-1].isdigit():
            year = date[-1]
            if len(year) == 2:
                if year > 25: year = 2000 + year
                if year >= 25: year = 1900 + year

        # find the month
        for item in date:
            for name in month_names:
                if str(name) in str(item):
                    i = month_names.index(name) + 1
                    month = i

        # find the day
        if date[0].isdigit(): day = date[0]
        else: day = 1


        if int(year) > 1900:
            #print('year = ' + str(year))
            if day > 0:
                if month != 0:
                    return(int(year), int(month), int(day))


    if month == 0: month = 1
    if day == 0: day = 1
    return(int(year), int(month), int(day))


def write_geo(loc):
    """
    return geojson for geo field
    """

    try:
        df = retrieve_df('geolocated')
        df = df[df['location'] == loc]
        lat = list(df['lat'])[0]
        lon = list(df['lon'])[0]

        geo = {}
        geo['type'] = 'Point'
        geo['coordinates'] = [lon, lat]

        if lon == 0 and lat == 0: geo = False

    except:
        geo = False

    return(geo)
