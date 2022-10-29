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


def year_counts():
    """
    create year_counts_pdf.csv
    create year_counts_cdf.csv
    """

    annual_sum()

    cdf_counts()
    count_percent()
    enrolled_percent()

    # make js for plotting
    # retrieve trials.json
    js_count()
    js_enrolled()
    js_cdf_count()
    js_cdf_enroll()


    count_scatter_enrollment()
    js_scatter_enrollment()
    js_scatter_enrollment2()



def count_scatter_enrollment():
    """

    """

    datasets = []

    df_group = retrieve_df('groups')
    groups = df_group.columns

    for group in groups:

        print('group = ' + group)

        if 'url' in group: continue
        urls = list(df_group[df_group[group] > 0]['url'])

        #years = np.arange(1990, 2025, 1)
        years, enrolls = [], []

        trials = retrieve_json('trials')['trials']
        for trial in trials:

            if trial['URL'] not in urls: continue

            year_found, month, day = find_date(trial)

            years.append(year_found)
            enroll = trial['Enrollment']
            enrolls.append(enroll)

        df = pd.DataFrame()
        df['year'] = years
        df['enroll'] = enrolls
        fil_dst = os.path.join(retrieve_path('scatters'), group + '.csv')
        df.to_csv(fil_dst)


def js_scatter_enrollment():
    """

    """

    datasets = []

    fol_src = retrieve_path('scatters')
    for filename in os.listdir(fol_src):

        print('filename = ' + filename)
        fil_src = os.path.join(fol_src, filename)
        print(fil_src)
        df = retrieve_df(fil_src)

        df = df[df['year'] > 2004]

        x = list(df['year'])
        y = list(df['enroll'])

        label = filename.split('.')[0]

        if 'all' == label: continue

        datas = []
        backgroundColors = []
        for i in range(len(x)):
            inc = (random.random()*10 - 5)/10
            data = {}
            data['x'] = x[i] + inc
            data['y'] = y[i]
            data['r'] = 5

            datas.append(data)
            backgroundColors.append(calculate_color(label))

        dataset = {}
        dataset['label'] = label
        dataset['data'] = datas
        dataset['backgroundColor'] = backgroundColors
        datasets.append(dataset)
        continue

    true_var = True
    js_dataset = {}
    #js_dataset['labels'] = list(df['year'])
    js_dataset['datasets'] = datasets
    print(js_dataset)

    config = {}
    config['type'] = 'bubble'
    config['data'] = js_dataset

    options = {}
    plugins = {}
    title = {}
    title['display'] = 'true'
    title['text'] = 'Chart.js Bar Chart - Stacked'
    #plugins['title'] = title
    options['plugins'] = plugins
    options['responsive'] = true_var
    options['scales'] = { 'myScale': {'type': 'logarithmic', 'position': 'right' }}

    scales = {}
    xtitle = 'Start Year of the Trial'
    #xtitle = axes_titles[0]
    #scales['xAxes'] = [{'stacked': true_var, 'barPercentage': 1.26, 'scaleLabel': {'display': true_var, 'labelString': xtitle}, 'ticks' : {'max' : 2025,'min' : 1994}]
    ytitle = '% of Trials'
    #ytitle = axes_titles[1]
    scales['yAxes'] = [{'type': 'logarithmic'}]
    options['scales'] = scales
    config['options'] = options

    chart_name = 'scatter_enrolled'

    fil_dst = os.path.join(retrieve_path('js'), chart_name + '.js' )
    with open(fil_dst , "w") as f:

        descriptor_line = 'const data_' + str(chart_name) + ' = '
        f.write(descriptor_line)
        json.dump(js_dataset, f, indent = 4)
        f.write(';')

        descriptor_line = 'const config_' + str(chart_name) + ' = '
        f.write('\n' + '\n')
        f.write(descriptor_line)
        json.dump(config, f, indent = 4)
        f.write(';')

        f.write('\n' + '\n')
        descriptor_line = 'const ctx_' + str(chart_name) + ' = document.getElementById("' + str(chart_name) + '").getContext(\'2d\');'
        f.write(descriptor_line)

        f.write('\n' + '\n')
        descriptor_line = 'const myChart_' + str(chart_name) + ' = new Chart(ctx_' + str(chart_name) + ' ,'
        f.write(descriptor_line)
        descriptor_line = ' config_' + str(chart_name) + '  );'
        f.write(descriptor_line)
        f.write('\n' + '\n')

        f.close()


def js_scatter_enrollment2():
    """

    """

    datasets = []

    fol_src = retrieve_path('scatters')
    folder = os.listdir(fol_src)
    for filename in folder:

        j = folder.index(filename)

        print('filename = ' + filename)
        fil_src = os.path.join(fol_src, filename)
        print(fil_src)
        df = retrieve_df(fil_src)

        df = df[df['year'] > 2004]

        print(df)
        df = df.dropna()
        print(df)

        x = list(df['year'])
        y = list(df['enroll'])

        label = filename.split('.')[0]

        if 'all' == label: continue

        datas = []
        backgroundColors = []
        for i in range(len(x)):

            ymean = y[i]/sum(y)
            if y[i] >= ymean: ydel = (max(y) - y[i])*0.45/(max(y)-ymean)
            else: ydel = (y[i] - min(y))*0.45/(ymean - min(y))

            inc = (random.random()*2*ydel - ydel)

            """
            print('x = ' + str(x))
            print('y = ' + str(y))
            print('sum(y) = ' + str(sum(y)))
            print('ymean = ' + str(ymean))
            print('max(y) = ' + str(max(y)))
            print('y[i] = ' + str( y[i]))
            print('ydel = ' + str(ydel))
            print('inc = ' + str(inc))
            """

            assert inc >= -0.5 and inc <= 0.5
            data = {}
            data['x'] = j + inc
            data['y'] = y[i]
            data['r'] = 5

            datas.append(data)
            backgroundColors.append(calculate_color(label))

        dataset = {}
        dataset['label'] = label
        dataset['data'] = datas
        dataset['backgroundColor'] = backgroundColors
        datasets.append(dataset)
        continue

    true_var = True
    js_dataset = {}
    #js_dataset['labels'] = list(df['year'])
    js_dataset['datasets'] = datasets
    print(js_dataset)

    config = {}
    config['type'] = 'bubble'
    config['data'] = js_dataset

    options = {}
    plugins = {}
    title = {}
    title['display'] = 'true'
    title['text'] = 'Chart.js Bar Chart - Stacked'
    #plugins['title'] = title
    options['plugins'] = plugins
    options['responsive'] = true_var
    options['scales'] = { 'myScale': {'type': 'logarithmic', 'position': 'right' }}

    scales = {}
    xtitle = 'Start Year of the Trial'
    #xtitle = axes_titles[0]
    #scales['xAxes'] = [{'stacked': true_var, 'barPercentage': 1.26, 'scaleLabel': {'display': true_var, 'labelString': xtitle}, 'ticks' : {'max' : 2025,'min' : 1994}]
    ytitle = '% of Trials'
    #ytitle = axes_titles[1]
    scales['yAxes'] = [{'type': 'logarithmic'}]
    options['scales'] = scales
    config['options'] = options

    chart_name = 'scatter_enrolled_grouped'

    fil_dst = os.path.join(retrieve_path('js'), chart_name + '.js' )
    with open(fil_dst , "w") as f:

        descriptor_line = 'const data_' + str(chart_name) + ' = '
        f.write(descriptor_line)
        json.dump(js_dataset, f, indent = 4)
        f.write(';')

        descriptor_line = 'const config_' + str(chart_name) + ' = '
        f.write('\n' + '\n')
        f.write(descriptor_line)
        json.dump(config, f, indent = 4)
        f.write(';')

        f.write('\n' + '\n')
        descriptor_line = 'const ctx_' + str(chart_name) + ' = document.getElementById("' + str(chart_name) + '").getContext(\'2d\');'
        f.write(descriptor_line)

        f.write('\n' + '\n')
        descriptor_line = 'const myChart_' + str(chart_name) + ' = new Chart(ctx_' + str(chart_name) + ' ,'
        f.write(descriptor_line)
        descriptor_line = ' config_' + str(chart_name) + '  );'
        f.write(descriptor_line)
        f.write('\n' + '\n')

        f.close()






def annual_sum():
    # retrieve groups.csv
    df = retrieve_df('groups')

    years = np.arange(1995, 2024, 1)

    df_count = pd.DataFrame()
    df_count['year'] = years

    for col in df.columns:

        if col == 'url': continue

        counts = []
        enrolleds = []

        for year in years:

            count = 0
            enrolled = 0

            df_new = df[df[col] > 0]
            urls = list(df_new['url'])

            trials = retrieve_json('trials')['trials']
            for trial in trials:

                url = trial['URL']

                if url not in urls: continue

                year_found, month, day = find_date(trial)

                """
                date_found = trial['Start Date']
                date_split = date_found.split(' ')
                for item in date_split:
                    if item.isdigit() and len(item) == 4:
                        year_found = item
                        # print('year_found = ' + str(year_found))
                """

                if int(year_found) != int(year): continue

                count = count + 1
                try:
                    enrolled = enrolled + int(float((trial['Enrollment'])))
                except:
                    enrolled = enrolled

            counts.append(count)
            enrolleds.append(enrolled)

        #df_count = pd.DataFrame()
        #df_count['year'] = years
        df_count[str(col + '_count')] = counts
        df_count[str(col + '_enrolled')] = enrolleds
        df_count.to_csv(retrieve_path('year_counts_pdf'))


def js_cdf_enroll():
    """

    """

    df = retrieve_df('year_counts_cdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' not in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(str(col + '_pure'))
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['text'] = 'Enrolled CDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart-cdf_enroll"), '
        dst_json = os.path.join(retrieve_path('cdf_js_enroll'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()


def js_cdf_count():
    """

    """

    df = retrieve_df('year_counts_cdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(col)
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['text'] = 'Trial Count CDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart-cdf_count"), '
        dst_json = os.path.join(retrieve_path('cdf_js_count'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()


def js_enrolled():
    """

    """

    df = retrieve_df('year_counts_pdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' not in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(col)
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['test'] = 'Enrolled PDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart-enroll"), '
        dst_json = os.path.join(retrieve_path('pdf_js_enrolled'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()


def js_count():
    """

    """

    df = retrieve_df('year_counts_pdf')

    datas = []

    for col in df.columns:

        if col == 'year': continue
        if 'enroll' in col: continue


        info = {}
        info['data'] = list(df[col])
        info['label'] = col
        info['borderColor'] = calculate_color(col)
        info['fill'] ='false'

        datas.append(info)

        lines = {}
        lines['type'] = 'line'

        data = {}
        data['labels'] = list(df['year'])
        data['datasets'] = datas

        lines['data'] = data

        title = {}
        title['display'] = 'true'
        title['test'] = 'PDF'
        options = {}
        options['title'] = title

        lines['options'] = options


        # save the group as js
        descriptor_line = 'new Chart(document.getElementById("line-chart"), '
        dst_json = os.path.join(retrieve_path('pdf_js'))
        print('dst_json = ' + str(dst_json))
        with open(dst_json, "w") as f:
            f.write(descriptor_line)
            json.dump(lines, f, indent = 4)
            f.write(');')
        f.close()


def cdf_counts():
    """
    create year_counts_pdf.csv
    create year_counts_cdf.csv
    """

    # retrieve groups.csv
    df = retrieve_df('year_counts_pdf')
    df_cdf  = pd.DataFrame()

    years = list(df['year'])
    for year in years:

        df_year = df[df['year'] <= year]

        df_temp = pd.DataFrame()
        df_temp['year'] = [year]

        for col in df_year.columns:

            if col == 'year': continue

            df_temp[col] = sum(list(df_year[col]))

        df_cdf = df_cdf.append(df_temp)
        df_cdf.to_csv(retrieve_path('year_counts_cdf'))


def enrolled_scatter():
    """

    """

    for year in np.arange(2004,2024,1):

        for trial in retrieve_json('trials')['trials']:

            year_found, month, day = find_date(trial)
            if year_found != year: continue

            print('help')


def count_percent():
    """

    """

    df = retrieve_df('year_counts_pdf')
    df_per = pd.DataFrame()


    years = list(df['year'])
    for year in years:

        df_year = df[df['year'] == year]
        #print(df_year)

        df_temp = pd.DataFrame()
        df_temp['year'] = [year]

        allo = int(list(df_year['allo_count'])[0])
        auto = int( list(df_year['auto_count'])[0])
        both = int(list(df_year['both_count'])[0])

        sum = allo + auto + both

        if sum == 0: sum = 1

        df_temp['allo'] = [round(100*float(allo/sum),1)]
        df_temp['auto'] = [round(100*float(auto/sum),1)]
        df_temp['both'] = [round(100*float(both/sum),1)]

        df_per = df_per.append(df_temp)

        df_per.to_csv(retrieve_path('count_percent'))

    df = df_per[df_per['year'] > 2003]
    print(df)
    assert min(list(df['year'])) > 2003

    xtitle = 'Start Year of the Trial'
    ytitle = '% of Trials Beginning Each Year'
    axes_titles = [xtitle, ytitle]
    write_stacked_bar_js(df, 'bar_count_js', axes_titles)


def enrolled_percent():
    """

    """

    df = retrieve_df('year_counts_pdf')
    df_per = pd.DataFrame()


    years = list(df['year'])
    for year in years:

        df_year = df[df['year'] == year]
        #print(df_year)

        df_temp = pd.DataFrame()
        df_temp['year'] = [year]

        allo = int(list(df_year['allo_enrolled'])[0])
        auto = int( list(df_year['auto_enrolled'])[0])
        both = int(list(df_year['both_enrolled'])[0])

        sum = allo + auto + both

        if sum == 0: sum = 1

        df_temp['allo'] = [round(100*float(allo/sum),1)]
        df_temp['auto'] = [round(100*float(auto/sum),1)]
        df_temp['both'] = [round(100*float(both/sum),1)]

        df_per = df_per.append(df_temp)
        df_per.to_csv(retrieve_path('enrolled_percent'))


    df = df_per[df_per['year'] > 2003]
    print(df)
    assert min(list(df['year'])) > 2003

    xtitle = 'Start Year of the Trial'
    ytitle = '% Enrolled in a Clinical Trial Each Year'
    axes_titles = [xtitle, ytitle]
    write_stacked_bar_js(df, 'bar_enrolled_js', axes_titles)


def write_stacked_bar_js(df, file_dst, axes_titles):
    """
    save js
    """

    chart_name = file_dst

    years = list(df['year'])

    datasets = []
    for col in df.columns:

        print(col)

        if col == 'year': continue

        backgroundColors = []
        for i in range(len(years)):
            backgroundColors.append(calculate_color(col))

        dataset = {}
        dataset['label'] = col
        dataset['data'] = list(df[col])
        dataset['backgroundColor'] = backgroundColors
        dataset['borderColor'] = backgroundColors
        dataset['borderWidth'] = 1
        datasets.append(dataset)

        js_dataset = {}
        js_dataset['labels'] = list(df['year'])
        js_dataset['datasets'] = datasets

    print(js_dataset)

    config = {}
    config['type'] = 'bar'
    config['data'] = js_dataset

    options = {}
    plugins = {}
    title = {}
    title['display'] = 'true'
    title['text'] = 'Chart.js Bar Chart - Stacked'
    plugins['title'] = title
    options['plugins'] = plugins
    options['responsive'] = 'true'

    scales = {}
    true_var = True
    xtitle = 'Start Year of the Trial'
    xtitle = axes_titles[0]
    scales['xAxes'] = [{'stacked': true_var, 'barPercentage': 1.26, 'scaleLabel': {'display': true_var, 'labelString': xtitle}}]
    ytitle = '% of Trials'
    ytitle = axes_titles[1]
    scales['yAxes'] = [{'stacked': true_var, 'barPercentage': 1.26, 'scaleLabel': {'display': true_var, 'labelString': ytitle}, 'ticks' : {'max' : 100,'min' : 0},}]
    options['scales'] = scales

    config['options'] = options


    # save the group as js

    dst_json = os.path.join(retrieve_path(file_dst))
    print('dst_json = ' + str(dst_json))
    with open(dst_json, "w") as f:

        descriptor_line = 'const data_' + str(chart_name) + ' = '
        f.write(descriptor_line)
        json.dump(js_dataset, f, indent = 4)
        f.write(';')

        descriptor_line = 'const config_' + str(chart_name) + ' = '
        f.write('\n' + '\n')
        f.write(descriptor_line)
        json.dump(config, f, indent = 4)
        f.write(';')

        f.write('\n' + '\n')
        descriptor_line = 'const ctx_' + str(chart_name) + ' = document.getElementById("' + str(chart_name) + '").getContext(\'2d\');'
        f.write(descriptor_line)

        f.write('\n' + '\n')
        descriptor_line = 'const myChart_' + str(chart_name) + ' = new Chart(ctx_' + str(chart_name) + ' ,'
        f.write(descriptor_line)
        descriptor_line = ' config_' + str(chart_name) + '  );'
        f.write(descriptor_line)
        f.write('\n' + '\n')

        f.close()
