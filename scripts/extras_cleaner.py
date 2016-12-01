
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
import matplotlib
import time
matplotlib.use('Agg')
import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import addfips
from selenium import webdriver
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import us
import wget
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(1024, 768))
# display.start()

# binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
# driver = webdriver.Firefox(firefox_binary=binary)

def clean_extras(series, output_path, replace_files):

    states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id","il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

    main_folder = os.path.dirname(os.path.abspath('__file__'))

    af = addfips.AddFIPS()

    data_path = main_folder + '/data/extras/'

    if os.path.isdir(data_path) is False:
        os.mkdir(data_path)

    voting_machines_data = pd.read_csv(data_path + "/voting_machines.csv", header = 0, names=['FIPS code', 'State', 'Jurisdiction','Division','Precincts','Total Registration','Make','Model','Equipment Type','VVPAT','Accessible Use','Early Voting','Absentee Ballots','Polling Place','County_FIPS'])

    paper = []
    electronic = []

    fips_temp = []

    for i in voting_machines_data.iterrows():
        fips_temp.append(int(voting_machines_data['FIPS code'].ix[i]/100000))
        if voting_machines_data['Equipment Type'].ix[i] == "DRE-Touchscreen" or voting_machines_data['Equipment Type'].ix[i] == "DRE-Push Button" or voting_machines_data['Equipment Type'].ix[i] == "DRE-Dial":
            paper.append(0)
            electronic.append(1)
        else:
            paper.append(1)
            electronic.append(0)

    voting_machines_data['County_FIPS'] = fips_temp

    voting_machines_data['Paper'] = paper
    voting_machines_data['Electronic'] = electronic
    
    voting_machines_data = voting_machines_data.pivot_table(columns = 'County_FIPS', values = ['Paper','Electronic']).transpose()

    voting_machines_data.to_csv(main_folder + '/data/covariates/voting_machines.csv', index = True, sep = ",", encoding='utf-8', mode = 'w')

