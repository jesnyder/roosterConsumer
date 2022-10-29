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


def prepare_html():
    """
    list js
    """

    # list all js scripts
    list_js()

    # insert list js to index.html
    #insert_list_js()


def list_js():
    """
    list js
    """

    fil_dst = retrieve_path('script_list')
    with open(fil_dst, "w") as f:

        for file in os.listdir(retrieve_path('js')):


            # define the script
            line = '<script '
            line = line + 'src="js/' + file + '">'
            line = line + '</script>'
            f.write(line)
            f.write('\n')

        f.write('\n')
        f.write('\n')
        for file in os.listdir(retrieve_path('js')):

            div_name = file.split('.')[0]

            # comment area
            line = '<!-- '
            line = line + file
            line = line + ' -->'
            f.write(line)
            f.write('\n')

            line = ''
            line = line + '<div id="text" style="width:80% ; margin-left: 10%; font-family: Calibri;">'
            line = line + '<p> <br> Explain the chart! </p> </div>'
            f.write(line)
            f.write('\n')

            """
            # create div with filename
            line = '<div id="'
            line = line + div_name
            line = line + '"></div>'
            f.write(line)
            f.write('\n')
            """

            # create canvas within a div
            line = '<div id="container" style="text-align:center; '
            line = line + 'width:80%; margin-left: 10%; '
            line = line + 'font-family: Calibri;">'
            f.write(line)
            f.write('\n')
            line = '<canvas id="'
            line = line + div_name + '" '
            line = line + 'height="125"  style="border:0px solid"></canvas>'
            f.write(line)
            f.write('\n')
            f.write('</div>')
            f.write('\n')

            # define the script
            line = '<script '
            line = line + 'src="js/' + file + '">'
            line = line + '</script>'
            f.write(line)
            f.write('\n')
            f.write('\n')

    f.close()


def insert_list_js():
    """




    # Using readlines()
    fil_dst = retrieve_path('script_list')
    f1 = open(fil_dst, 'r')
    lines1 = f1.readlines()
    f1.close()


    fil_dst = retrieve_path('index')
    f2 = open(fil_dst, 'r')
    lines2 = f2.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if '!!insert list js!!' in line:
        line = line.replace('!!insert list js!!', lines1)
        lines[i] = line
    f2.close()


    # write revised text
    fil_dst = retrieve_path('index')
    f1 = open(fil_dst, 'w+')
    for line in lines:
        f.write(line)
    f.close()
    """
