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
from bs4 import BeautifulSoup
import os
import addfips
from selenium import webdriver
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import us
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(1024, 768))
# display.start()

# binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
# driver = webdriver.Firefox(firefox_binary=binary)

path = os.path.join(os.path.dirname(os.path.abspath('__file__')))

# path = os.path.dirname(os.path.abspath('__file__'))

# states = ['al']

af = addfips.AddFIPS()

states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id", "il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

website_president = 'http://www.cnn.com/ELECTION/2008/results/county/#'

website_house = 'http://www.cnn.com/ELECTION/2008/results/full/#val=Hp'

website_senate = 'http://www.cnn.com/ELECTION/2008/results/county/#'

website_governor = 'http://www.cnn.com/ELECTION/2008/results/county/#'

data_pres_path = path + '/data/election-2008/president/'
data_senate_path = path + '/data/election-2008/senate/'
data_house_path = path + '/data/election-2008/house/'
data_governor_path = path + '/data/election-2008/governor/'

if os.path.isdir(data_pres_path) is False:
    os.mkdir(data_pres_path)

if os.path.isdir(data_senate_path) is False:
    os.mkdir(data_senate_path)

if os.path.isdir(data_house_path) is False:
    os.mkdir(data_house_path)

if os.path.isdir(data_governor_path) is False:
    os.mkdir(data_governor_path)

system = platform.system()
if system == "Windows":
    if os.path.isdir(path + '/phantomjs-windows/') is True:

        print "true"
        for dirName, subdirList, fileList in os.walk(path + '/phantomjs-windows/', topdown=False):
            for fname in fileList:
                print('\t%s' % fname)
                if fname.startswith('phantomjs.exe'):
                    phantom_exe = dirName + "/" + fname
                    phantom_loc = dirName
                    break
elif system == "Darwin":
    if os.path.isdir(path + '/phantomjs-mac/') is True:
        for dirName, subdirList, fileList in os.walk(path + '/phantomjs-mac/', topdown=False):
            for fname in fileList:
                if fname.startswith('phantomjs.exe'):
                    phantom_exe = dirName + "/" + fname
                    phantom_loc = dirName
                    break
elif system == "Linux":
    if os.path.isdir(path + '/phantomjs-linux/') is True:
        for dirName, subdirList, fileList in os.walk(path + '/phantomjs-linux/', topdown=False):
            for fname in fileList:
                if fname.startswith('phantomjs.exe'):
                    phantom_exe = dirName + "/" + fname
                    phantom_loc = dirName
                    break
else:
    system_type = raw_input("Python could not detect your system type. Please enter your system type, one of \"Windows\", \"Mac\", \"Linux\".")
    system_type = system_type.lower()
    if os.path.isdir(path + '/phantomjs-' + system_type + '/') is True:
        for dirName, subdirList, fileList in os.walk(path + '/phantomjs-' + system_type + '/', topdown=False):
            for fname in fileList:
                if fname.startswith('phantomjs.exe'):
                    phantom_exe = dirName + "/" + fname
                    phantom_loc = dirName
                    break

phantom_exe = str(phantom_exe.replace("/", "\\"))

file_nat = open(data_pres_path + "national_2008.csv", "w")
file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Percentage,Votes\n")
file_nat.close()

for state in states:
    try:
        i = 1
        file_nat = open(data_pres_path + "national_2008.csv", "a")
        file_state = open(data_pres_path + state + "_2008.csv", "w")
        file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
        while i < 100:
            driver = webdriver.PhantomJS(executable_path = phantom_exe)
            url = website_president + state.upper() + 'P00p' + str(i)
            driver.get(url)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source)
            for res_table in soup.find_all('div', class_='cnnElex_rBoxCTY'):
                county_name = res_table.find('div', class_='cnnElex_raceState').get_text()
                for tr in res_table.find_all('tr'):
                    tds_name = tr.find('a', class_='nobio').get_text()
                    if tr.find('div', class_='cnnR_R'):
                        tds_party = "R"
                    elif tr.find('div', class_='cnnR_D'):
                        tds_party = 'D'
                    elif tr.find('div', class_='cnnR_I'):
                        tds_party = 'I'
                    else:
                        tds_party = 'Unknown'
                    tds_pct = tr.find('b').get_text()
                    tds_tot = tr.find('td', class_='vote_p').get_text()
                    try:
                        file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                    except:
                        file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
            if soup.find('div', id='cnnElex_fResPagi'):
                i = i + 1
            else:
                i = 101
            driver.close()
        file_state.close()
        file_nat.close()
        time.sleep(np.random.uniform(5,17.6))
    except:
        pass
