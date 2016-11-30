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

states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id","il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

data_types = ['']

main_folder = os.path.join(os.path.dirname(os.path.abspath('__file__')), '..')

# states = ['al']

af = addfips.AddFIPS()

machine_data_url_1 = 'https://www.verifiedvoting.org/api?advanced&state_fips='
machine_data_url_2 = '&equip_type=&make=&model=&year=2016&download=csv'

data_path_2016 = main_folder + '/voting_machines/2016'

data_path_2014 = main_folder + '/voting_machines/2014'

data_path_2012 = main_folder + '/voting_machines/2012'

if os.path.isdir(data_path_2016) is False:
    os.mkdir(data_path_2016)

if os.path.isdir(data_path_2014) is False:
    os.mkdir(data_path_2014)

if os.path.isdir(data_path_2012) is False:
    os.mkdir(data_path_2012)

crosswalk = us.states.mapping('name','abbr')

# for state in states:
#     st = af.get_state_fips(state)
#     urllib.urlretrieve(machine_data_url_1 + str(st) + machine_data_url_2, data_path_2016 + '/' + str(state) + '.csv')

# machine_data_url_1 = 'https://www.verifiedvoting.org/api?advanced&state_fips='
# machine_data_url_2 = '&equip_type=&make=&model=&year=2014&download=csv'

# for state in states:
#     st = af.get_state_fips(state)
#     urllib.urlretrieve(machine_data_url_1 + str(st) + machine_data_url_2, data_path_2014 + '/' + str(state) + '.csv')

# machine_data_url_1 = 'https://www.verifiedvoting.org/api?advanced&state_fips='
# machine_data_url_2 = '&equip_type=&make=&model=&year=2012&download=csv'

# for state in states:
#     st = af.get_state_fips(state)
#     urllib.urlretrieve(machine_data_url_1 + str(st) + machine_data_url_2, data_path_2012 + '/' + str(state) + '.csv')

file_nat = open(data_path_2016 + "national_2016.csv", "w")
file_nat.write("FIPS code,State,Jurisdiction,Division,Precincts,Total Registration,Make,Model,Equipment Type,VVPAT,Accessible Use,Early Voting,Absentee Ballots,Polling Place\n")
file_nat.close()

for state in states:
    print state
    try:
        data = pd.read_csv(data_path_2016 + '/' + str(state) + '.csv', delimiter = ",", header = 1, names = ['FIPS code','State','Jurisdiction','Division','Precincts','Total Registration','Make','Model','Equipment Type','VVPAT','Accessible Use','Early Voting','Absentee Ballots','Polling Place'], index_col = False)
        county_fips = []
        data['Jurisdiction'] = data['Jurisdiction'].str.replace(" County","")
        data['Jurisdiction'] = data['Jurisdiction'].str.strip()
        for i in data.iterrows():
            county_fips.append(str(af.get_county_fips(str(data['Jurisdiction'].ix[i]), str(data['State'].ix[i]))))
        data['county_fips'] = county_fips
        data['county_fips'] = data['county_fips'].apply(str)
        with open(data_path_2016 + '/' + 'national_2016.csv', 'a') as f:
            data.to_csv(f, header=False, index = False)
    except:
        print "problem " + str(state)
        pass
    
file_nat = open(data_path_2014 + "national_2014.csv", "w")
file_nat.write("FIPS code,State,Jurisdiction,Division,Precincts,Total Registration,Make,Model,Equipment Type,VVPAT,Accessible Use,Early Voting,Absentee Ballots,Polling Place\n")
file_nat.close()

for state in states:
    print state
    try:
        data = pd.read_csv(data_path_2014 + '/' + str(state) + '.csv', delimiter = ",", header = 1, names = ['FIPS code','State','Jurisdiction','Division','Precincts','Total Registration','Make','Model','Equipment Type','VVPAT','Accessible Use','Early Voting','Absentee Ballots','Polling Place'], index_col = False)
        county_fips = []
        data['Jurisdiction'] = data['Jurisdiction'].str.replace(" County","")
        data['Jurisdiction'] = data['Jurisdiction'].str.strip()
        for i in data.iterrows():
            county_fips.append(str(af.get_county_fips(str(data['Jurisdiction'].ix[i]), str(data['State'].ix[i]))))
        data['county_fips'] = county_fips
        with open(data_path_2014 + '/' + 'national_2014.csv', 'a') as f:
            data.to_csv(f, header=False, index = False)
    except:
        print "problem " + str(state)
        pass

file_nat = open(data_path_2012 + "national_2012.csv", "w")
file_nat.write("FIPS code,State,Jurisdiction,Division,Precincts,Total Registration,Make,Model,Equipment Type,VVPAT,Accessible Use,Early Voting,Absentee Ballots,Polling Place\n")
file_nat.close()

for state in states:
    print state
    try:
        data = pd.read_csv(data_path_2012 + '/' + str(state) + '.csv', delimiter = ",", header = 1, names = ['FIPS code','State','Jurisdiction','Division','Precincts','Total Registration','Make','Model','Equipment Type','VVPAT','Accessible Use','Early Voting','Absentee Ballots','Polling Place'], index_col = False)
        county_fips = []
        data['Jurisdiction'] = data['Jurisdiction'].str.replace(" County","")
        data['Jurisdiction'] = data['Jurisdiction'].str.strip()
        for i in data.iterrows():
            county_fips.append(str(af.get_county_fips(str(data['Jurisdiction'].ix[i]), str(data['State'].ix[i]))))
        data['county_fips'] = county_fips
        with open(data_path_2012 + '/' + 'national_2012.csv', 'a') as f:
            data.to_csv(f, header=False, index = False)
    except:
        print "problem " + str(state)
        pass
