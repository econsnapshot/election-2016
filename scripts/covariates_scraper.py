################################################################################################################
#Author: Ben Griffy
#Institution: University of California, Santa Barbara
#email: griffy@umail.ucsb.edu
#website: https://sites.google.com/site/bengriffy/home
#Date:
################################################################################################################

from __future__ import division

import numpy as np
import pandas as pd
import time
import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import addfips
import time
import us

def scraper_economics(series, output_path, replace_files):

    states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id","il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

    main_folder = os.path.dirname(os.path.abspath('__file__'))

    fips = pd.read_csv(main_folder + '/data/fips/' + 'fips.csv')

    af = addfips.AddFIPS()

    location_empwage_data_url = 'http://data.bls.gov/cew/data/api/2016/1/area/'
    industry_empwage_data_url = 'http://data.bls.gov/cew/data/api/2016/1/industry/'
    # unemp_data_url = 'http://www.bls.gov/lau/laucnty'
    unemp_data_url = 'http://www.bls.gov/web/metro/laucntycur14.txt'
    income_data_url = 'http://www.bea.gov/newsreleases/regional/lapi/2016/xls/lapi1116.xlsx'
    data_location_empwage_path = main_folder + '/data/covariates/location/'
    data_industry_empwage_path = main_folder + '/data/covariates/industry/'
    data_unemp_path = main_folder + '/data/covariates/unemp/'
    data_income_path = main_folder + '/data/covariates/income/'

    if os.path.isdir(data_location_empwage_path) is False:
        os.mkdir(data_location_empwage_path)
    if os.path.isdir(data_industry_empwage_path) is False:
        os.mkdir(data_industry_empwage_path)
    if os.path.isdir(data_unemp_path) is False:
        os.mkdir(data_unemp_path)
    if os.path.isdir(data_income_path) is False:
        os.mkdir(data_income_path)


    crosswalk = us.states.mapping('name','abbr')

    if series == "area":

        for loc in fips['fips']:
            loc = str(loc)
            if len(loc) < 5:
                st = str(us.states.lookup('0' + loc[0]))
                st = crosswalk[st].lower()
            else:
                st = str(us.states.lookup(loc[:2]))
                st = crosswalk[st].lower()
            state_loc = data_location_empwage_path + '/' + st + '/'
            if os.path.isdir(state_loc) is False:
                os.mkdir(state_loc)
            if len(loc) < 4:
                urllib.urlretrieve(location_empwage_data_url + '0' + loc + '.csv', state_loc + str(st) + '.csv')
            else:
                urllib.urlretrieve(location_empwage_data_url + loc + '.csv', state_loc + str(st) + '.csv')

    if series == "industry":
        i = 10
        urllib.urlretrieve(industry_empwage_data_url + str(i) + '.csv', data_industry_empwage_path + str(i) + '.csv')

        # while i < 999:
        #     try:
        #         urllib.urlretrieve(industry_empwage_data_url + str(i) + '.csv', data_industry_empwage_path + str(i) + '.csv')
        #         i = i + 1
        #     except:
        #         i = i + 1
        #         pass

    if series == "unemp":
        urllib.urlretrieve(unemp_data_url, data_unemp_path + '/unemployment.txt')
        # i = 15

        # while i > 9:
        #     try:
        #         urllib.urlretrieve(unemp_data_url + str(i) + '.txt', data_unemp_path + str(i) + '.txt')
        #         i = i - 1
        #     except:
        #         i = i - 1
        #         pass

        # while i >= 0:
        #     try:
        #         urllib.urlretrieve(unemp_data_url + '0' + str(i) + '.txt', data_unemp_path + str(i) + '.txt')
        #         i = i - 1
        #     except:
        #         i = i - 1
        #         pass

        # i = 99

        # while i >= 90:
        #     try:
        #         urllib.urlretrieve(unemp_data_url + str(i) + '.txt', data_unemp_path + str(i) + '.txt')
        #         i = i - 1
        #     except:
        #         i = i - 1
        #         pass

    if series == "income":
        urllib.urlretrieve(income_data_url, data_income_path + '/income_uncleaned.xlsx')
