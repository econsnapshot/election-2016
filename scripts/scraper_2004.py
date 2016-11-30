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
from bs4 import BeautifulSoup
import os
import addfips
import re
import us


# states = ['al']
def scraper_2004(output_path, scrape_all, replace):
    af = addfips.AddFIPS()

    states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id", "il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

    website_president = 'http://www.cnn.com/ELECTION/2004/pages/results/states/'

    website_house = 'http://www.cnn.com/ELECTION/2004/pages/results/states/'

    website_senate = 'http://www.cnn.com/ELECTION/2004/pages/results/states/'

    website_governor = 'http://www.cnn.com/ELECTION/2004/pages/results/states/'

    data_pres_path = output_path + '/president/'
    data_senate_path = output_path + '/senate/'
    data_house_path = output_path + '/house/'
    data_governor_path = output_path + '/governor/'

    if os.path.isdir(data_pres_path) is False:
        os.mkdir(data_pres_path)

    file_nat = open(data_pres_path + "national_2004.csv", "w")
    file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Percentage,Votes\n")
    file_nat.close()

    for state in states:
        file_nat = open(data_pres_path + "national_2004.csv", "a")
        file_state = open(data_pres_path + state + "_2004.csv", "w")
        file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
        i = 0
        try:
            while i < 100:
                url = website_president + state.upper() + '/P/00/county' + '.00' + str(i) + '.html'
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page.read())
                for res_row in soup.find_all('tr', align='center'):
                    if res_row.find('td', class_="dataTableRace"):
                        county_name = res_row.find('td', class_="dataTableRace").find('b').get_text()
                    tds_name = res_row.find('a', href=re.compile('(javascript.*)')).get_text()
                    if res_row.find('img', class_="dataIcon")['alt'] == 'Republican':
                        tds_party = "R"
                    elif res_row.find('img', class_="dataIcon")['alt'] == 'Democrat':
                        tds_party = 'D'
                    elif res_row.find('img', class_="dataIcon")['alt'] == 'Independent':
                        tds_party = 'I'
                    elif res_row.find('img', class_="dataIcon")['alt'] != '':
                        tds_party = str(res_row.find('img', class_="dataIcon")['alt']).replace("Democratic","D")
                    else:
                        tds_party = 'I'
                    for res_col in res_row.find_all('td'):
                        if len(res_col.attrs) == 0 and len(list(res_col.descendants)) == 1 and res_col.string != None:
                            tds_tot = res_col.get_text()
                        elif len(res_col.attrs) == 0 and len(list(res_col.descendants)) == 2 and res_col.string != None:
                            tds_pct = res_col.get_text()
                    try:
                        file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                    except:
                        file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                i = i + 1
        except:
            pass
        file_state.close()
        file_nat.close()
        time.sleep(np.random.uniform(5,17.6))

    if scrape_all == True:

        if os.path.isdir(data_senate_path) is False:
            os.mkdir(data_senate_path)

        if os.path.isdir(data_house_path) is False:
            os.mkdir(data_house_path)

        if os.path.isdir(data_governor_path) is False:
            os.mkdir(data_governor_path)

        file_nat = open(data_senate_path + "national_2004.csv", "w")
        file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Percentage,Votes\n")
        file_nat.close()

        for state in states:
            file_nat = open(data_senate_path + "national_2004.csv", "a")
            file_state = open(data_senate_path + state + "_2004.csv", "w")
            file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
            i = 0
            try:
                while i < 100:
                    url = website_senate + state.upper() + '/S/01/county' + '.00' + str(i) + '.html'
                    page = urllib2.urlopen(url)
                    soup = BeautifulSoup(page.read())
                    for res_row in soup.find_all('tr', align='center'):
                        if res_row.find('td', class_="dataTableRace"):
                            county_name = res_row.find('td', class_="dataTableRace").find('b').get_text()
                        tds_name = res_row.find('a', href=re.compile('(javascript.*)')).get_text()
                        if res_row.find('img', class_="dataIcon")['alt'] == 'Republican':
                            tds_party = "R"
                        elif res_row.find('img', class_="dataIcon")['alt'] == 'Democrat':
                            tds_party = 'D'
                        elif res_row.find('img', class_="dataIcon")['alt'] == 'Independent':
                            tds_party = 'I'
                        elif res_row.find('img', class_="dataIcon")['alt'] != '':
                            tds_party = str(res_row.find('img', class_="dataIcon")['alt']).replace("Democratic","D")
                        else:
                            tds_party = 'I'
                        for res_col in res_row.find_all('td'):
                            if len(res_col.attrs) == 0 and len(list(res_col.descendants)) == 1 and res_col.string != None:
                                tds_tot = res_col.get_text()
                            elif len(res_col.attrs) == 0 and len(list(res_col.descendants)) == 2 and res_col.string != None:
                                tds_pct = res_col.get_text()
                        try:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        except:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                    i = i + 1
            except:
                pass
            file_state.close()
            file_nat.close()
            time.sleep(np.random.uniform(5,17.6))

        file_nat = open(data_house_path + "national_2004.csv", "w")
        file_nat.write("State,District,Party,St_FIPS,Candidate,Percentage,Votes\n")
        file_nat.close()

        for state in states:
            file_nat = open(data_house_path + "national_2004.csv", "a")
            file_state = open(data_house_path + state + "_2004.csv", "w")
            file_state.write("District,Party,Candidate,Percentage,Votes\n")
            i = 1
            try:
                while i < 100:
                    if i < 10:
                        url = website_house + state.upper() + '/H/0' + str(i) + '/index.html'
                    else:
                        url = website_house + state.upper() + '/H/' + str(i) + '/index.html'
                    # print url
                    page = urllib2.urlopen(url)
                    soup = BeautifulSoup(page.read())
                    for res_row in soup.find_all('tr', align='center'):
                        if res_row.find('td', class_="dataTableRace"):
                            county_name = res_row.find('td', class_="dataTableRace").find('b').get_text()
                        tds_name = res_row.find('a', href=re.compile('(javascript.*)')).get_text()
                        # print tds_name
                        if res_row.find('img', class_="dataIcon")['alt'] == 'Republican':
                            tds_party = "R"
                        elif res_row.find('img', class_="dataIcon")['alt'] == 'Democrat':
                            tds_party = 'D'
                        elif res_row.find('img', class_="dataIcon")['alt'] == 'Independent':
                            tds_party = 'I'
                        elif res_row.find('img', class_="dataIcon")['alt'] != '':
                            tds_party = str(res_row.find('img', class_="dataIcon")['alt']).replace("Democratic","D")
                        else:
                            tds_party = 'I'
                        if 'unopposed' in res_row.get_text():
                            tds_tot = 'unopposed'
                            tds_pct = 'unopposed'
                        else:
                            for res_col in res_row.find_all('td'):
                                if len(res_col.attrs) == 1 and len(list(res_col.descendants)) == 1 and res_col.string != None:
                                    tds_tot = res_col.get_text()
                                elif len(res_col.attrs) == 1 and len(list(res_col.descendants)) == 2 and res_col.string != None:
                                    tds_pct = res_col.get_text()
                        try:
                            file_nat.write(state.upper() + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        except:
                            file_nat.write(state.upper() + "," + str(us.states.lookup(state)) + " " + str(i) + "," + tds_party + "," + af.get_state_fips(state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(str(us.states.lookup(state)) + " " + str(i) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                    i = i + 1
            except:
                pass
            file_state.close()
            file_nat.close()
            time.sleep(np.random.uniform(5,17.6))

        file_nat = open(data_governor_path + "national_2004.csv", "w")
        file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Percentage,Votes\n")
        file_nat.close()

        for state in states:
            file_nat = open(data_governor_path + "national_2004.csv", "a")
            file_state = open(data_governor_path + state + "_2004.csv", "w")
            file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
            i = 0
            try:
                while i < 100:
                    url = website_governor + state.upper() + '/G/00/county' + '.00' + str(i) + '.html'
                    page = urllib2.urlopen(url)
                    soup = BeautifulSoup(page.read())
                    for res_row in soup.find_all('tr', align='center'):
                        if res_row.find('td', class_="dataTableRace"):
                            county_name = res_row.find('td', class_="dataTableRace").find('b').get_text()
                        tds_name = res_row.find('a', href=re.compile('(javascript.*)')).get_text()
                        if res_row.find('img', class_="dataIcon")['alt'] == 'Republican':
                            tds_party = "R"
                        elif res_row.find('img', class_="dataIcon")['alt'] == 'Democrat':
                            tds_party = 'D'
                        elif res_row.find('img', class_="dataIcon")['alt'] == 'Independent':
                            tds_party = 'I'
                        elif res_row.find('img', class_="dataIcon")['alt'] != '':
                            tds_party = str(res_row.find('img', class_="dataIcon")['alt']).replace("Democratic","D")
                        else:
                            tds_party = 'I'
                        for res_col in res_row.find_all('td'):
                            if len(res_col.attrs) == 0 and len(list(res_col.descendants)) == 1 and res_col.string != None:
                                tds_tot = res_col.get_text()
                            elif len(res_col.attrs) == 0 and len(list(res_col.descendants)) == 2 and res_col.string != None:
                                tds_pct = res_col.get_text()
                        try:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        except:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                    i = i + 1
            except:
                pass
            file_state.close()
            file_nat.close()
            time.sleep(np.random.uniform(5,17.6))
