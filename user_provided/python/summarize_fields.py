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

from list_trials import list_location
from write_geojson import calculate_color
from write_geojson import find_date


def summarize_fields():
    """
    summarize each field as a df and js variable
    """

    count_fields()
    count_fields_grouped()

    write_doughnut_js()
    write_grouped_doughnut_js()

    write_table_data()
    write_products()


def count_fields_grouped():
    """
    save each field as a count
    """


    fol_src = retrieve_path('summary')
    for filename in os.listdir(fol_src):

        # skip fields with many unique responses
        if 'Acronym' in filename: continue
        if 'Age' in filename: continue
        if 'Completion Date' in filename: continue
        if 'Condition' in filename: continue
        if 'desc' in str(filename): continue
        if 'Enrollment' in filename: continue
        if 'First Posted' in filename: continue
        if 'Interventions' in filename: continue
        if 'Last Update Posted' in filename: continue
        if 'Locations' in filename: continue
        if 'NCT Number' in filename: continue
        if 'Other IDs' in filename: continue
        if 'Outcome Measures' in filename: continue
        if 'Primary Completion Date' in filename: continue
        if 'Results First Posted' in filename: continue
        if 'Sponsor_Collaborators' in filename: continue
        if 'Start Date' in filename: continue
        if 'Study Designs' in filename: continue
        if 'Study Documents' in filename: continue
        #if 'Study Results' in filename: continue
        if 'Title' in filename: continue
        if 'URL' in filename: continue

        key = filename.split('.')[0]

        print('key = ' + str(key))

        fil_src = os.path.join(fol_src, filename)
        df = retrieve_df(fil_src)

        df_group = retrieve_df('groups')
        #print(df_group)
        # for each of the groups
        for col in df_group.columns:

            if col == 'url': continue
            urls = list(df_group[df_group[col] > 0]['url'])

            df[str(col + '_count')] = [0] * len(list(df['count']))
            df[str(col + '_enroll')] = [0] * len(list(df['count']))

            term_name = df.columns[0]
            terms = list(df[term_name])
            for i in range(len(terms)):

                term = terms[i]
                #print(term)

                # retrieve json
                trials = retrieve_json('trials')['trials']
                for trial in trials:

                    if trial['URL'] not in urls: continue
                    if trial[term_name] == term:

                        col_name = str(col + '_count')
                        value = df.at[i, col_name] + 1
                        df.at[i, col_name] = value

                        col_name = str(col + '_enroll')
                        try:
                            enroll = int(float(trial['Enrollment']))
                        except:
                            enroll = 0

                        value = df.at[i, col_name] + enroll
                        df.at[i, col_name] = value


        print(df)

        fil_dst = os.path.join(retrieve_path('summary_group'), filename)
        df.to_csv(fil_dst)


def write_grouped_doughnut_js():
    """

    """

    data = {}

    true_bool = True

    fol_src = retrieve_path('summary_group')
    for filename in os.listdir(fol_src):

        df = retrieve_df(os.path.join(fol_src, filename))
        df = df.dropna()
        df = reset_df(df)

        print(df)

        col = df.columns[0]
        print(col)

        labels = list(df[col])
        backgroundColors = list(retrieve_df('backgroundColors')['color'])
        backgroundColors = backgroundColors[:len(labels)]

        datasets = []
        for col in df.columns:

            if 'enroll' in col: continue
            if '_' not in col: continue
            if 'all_' in col: continue

            dataset = {}
            dataset['label'] = col
            dataset['data'] = list(df[col])
            dataset['backgroundColor'] =  backgroundColors
            datasets.append(dataset)

        data = {}
        data['labels'] = labels
        data['datasets'] = datasets

        config = {}
        config['type'] = "doughnut"
        config['data'] = data

        plugins = {}
        plugins['title'] = {'display': true_bool, 'text': 'Chart.js Doughnut Chart'}

        options = {}
        options['responsive'] = true_bool
        options['legend'] = {'position': 'right'}
        options['plugins'] = plugins
        config['options'] = options


        chart_name = str(filename.split('.')[0] + '_grouped')
        chart_name = chart_name.replace(' ', '_')

        dst_json = os.path.join(retrieve_path('js'), 'doughnut_' + str(chart_name) + '.js')
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:


            descriptor_line = 'const config_' + str(chart_name) + ' = '
            f.write('\n' + '\n')
            f.write(descriptor_line)
            json.dump(config, f, indent = 4)
            f.write(';')

            f.write('\n' + '\n')
            descriptor_line = 'const ctx_' + str(chart_name) + ' = document.getElementById("' + 'doughnut_' + str(chart_name) + '").getContext(\'2d\');'
            f.write(descriptor_line)

            f.write('\n' + '\n')
            descriptor_line = 'const myChart_' + str(chart_name) + ' = new Chart(ctx_' + str(chart_name) + ' ,'
            f.write(descriptor_line)
            descriptor_line = ' config_' + str(chart_name) + '  );'
            f.write(descriptor_line)
            f.write('\n' + '\n')

            f.close()


def write_doughnut_js():
    """

    """

    data = {}

    true_bool = True

    fol_src = retrieve_path('summary')
    for filename in os.listdir(fol_src):

        df = retrieve_df(os.path.join(fol_src, filename))
        df = df.dropna()
        df = reset_df(df)

        print(df)

        col = df.columns[0]
        print(col)

        labels = list(df[col])
        backgroundColor = ['rgb(212,178,212)', 'rgb(255,105,140)', 'rgb(92,141,255)']
        backgroundColor.append('rgb(127,212,85)')
        backgroundColor.append('rgb(89,212,126)')
        backgroundColor.append('rgb(85,212,212)')
        backgroundColor.append('rgb(89,212,126)')
        backgroundColor.append('rgb(212,81,177)')
        backgroundColor.append('rgb(89,212,126)')

        backgroundColor = backgroundColor[:len(labels)]

        dataset = {}
        dataset['label'] = 'all'
        dataset['data'] = list(df['enrolled'])
        dataset['backgroundColor'] =  backgroundColor

        data = {}
        data['labels'] = labels
        data['datasets'] = [dataset]

        config = {}
        config['type'] = "doughnut"
        config['data'] = data

        plugins = {}
        plugins['title'] = {'display': true_bool, 'text': 'Chart.js Doughnut Chart'}

        options = {}
        options['responsive'] = true_bool
        options['legend'] = {'position': 'right'}
        options['plugins'] = plugins
        config['options'] = options


        chart_name = filename.split('.')[0]

        dst_json = os.path.join(retrieve_path('js'), 'doughnut_' + str(chart_name) + '.js')
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:


            descriptor_line = 'const config_' + str(chart_name) + ' = '
            f.write('\n' + '\n')
            f.write(descriptor_line)
            json.dump(config, f, indent = 4)
            f.write(';')

            f.write('\n' + '\n')
            descriptor_line = 'const ctx_' + str(chart_name) + ' = document.getElementById("' + 'doughnut_' + str(chart_name) + '").getContext(\'2d\');'
            f.write(descriptor_line)

            f.write('\n' + '\n')
            descriptor_line = 'const myChart_' + str(chart_name) + ' = new Chart(ctx_' + str(chart_name) + ' ,'
            f.write(descriptor_line)
            descriptor_line = ' config_' + str(chart_name) + '  );'
            f.write(descriptor_line)
            f.write('\n' + '\n')

            f.close()


def count_fields():
    """
    save each field as a count
    """

    # retrieve json
    trials = retrieve_json('trials')['trials']
    how_many_trials = len(trials)
    keys = trials[0].keys()

    for key in keys:

        values = []
        enrolled = []
        for trial in trials:

            value = trial[key]
            values.append(value)

            try:
                enrolled.append(int(float((trial['Enrollment']))))
            except:
                enrolled.append(0)

        df_temp = pd.DataFrame()
        df_temp['term'] = values
        df_temp['enrollment'] = enrolled

        how_many_enrolled = sum(enrolled)


        terms, counts, enrolled = [], [], []
        for value in list(df_temp['term']):

            if value in terms: continue

            df_value = df_temp[df_temp['term'] == value]

            terms.append(value)

            count = list(df_temp['term']).count(value)
            counts.append(count)

            enroll = sum(list(df_value['enrollment']))
            enrolled.append(enroll)

        terms.append('NaN')
        counts.append(how_many_trials - sum(counts))
        enrolled.append(how_many_enrolled - sum(enrolled))

        df = pd.DataFrame()
        df[key] = terms
        df['count'] = counts
        df['enrolled'] = enrolled
        key_name = key.replace('/','_')
        print('key_name = ' + str(key_name))
        file_dst = os.path.join(retrieve_path('summary'), key_name + '.csv')
        df = reset_df(df.sort_values(by='count', ascending=False))
        df.to_csv(file_dst)


def write_table_data():
    """
    create .js
    """

    fol_src = retrieve_path('summary')
    for file in os.listdir(fol_src):

        filename = file.split('.')[0]

        print('filename = ' + filename)

        fil_src = os.path.join(fol_src, file)
        df = retrieve_df(fil_src)

        df = df.dropna()

        df = df[df['count'] > 0]
        if len(list(df['count'])) < 0: continue
        df = reset_df(df)

        print('df = ')
        print(df)

        lines = []
        for i in range(len(list(df['count']))):

            line = {}
            for col in df.columns:

                #print('col = ' + col)
                #print('i = ' + str(i))
                value = df.at[i, col]
                #print('value = ' + str(value))
                line[col] = value

            #print('line = ')
            #print(line)
            lines.append(line)

        #print('lines = ')
        #print(lines)

        # save the group as js
        descriptor_line = 'var table' + str(filename) + ' = '
        dst_json = os.path.join(retrieve_path('tableData'), filename + '.js')
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line + '\n' + '[' + '\n')

            for line in lines:
                print(line)
                f.write(str(line) + ' , ' + '\n')
            #json.dump(lines, f, indent = 4)
            #f.write(');')
            f.write( ']' + '\n')
        f.close()


def write_products():
    """
    create .js
    """

    # open user provided file
    file_src = retrieve_path('products')
    f = open(file_src,"r")
    lines = f.readlines()
    f.close()

    # open destination file
    file_dst = retrieve_path('products_js')
    f = open(file_src,"w+")
    for line in lines:
        f.write(line)
    f.close()
