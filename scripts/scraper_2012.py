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
import us
import re
# from selenium import webdriver
# from contextlib import closing
# from selenium.webdriver import Firefox # pip install selenium
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# states = ['al']

def scraper_2012(output_path, scrape_all, replace):

    af = addfips.AddFIPS()

    states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id", "il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

    website_president = 'http://www.politico.com/2012-election/results/president/'

    website_house = 'http://www.politico.com/2012-election/results/house/'

    website_senate = 'http://www.politico.com/2012-election/results/senate/'

    website_governor = 'http://www.politico.com/2012-election/results/governor/'

    data_pres_path = output_path + '/president/'
    data_senate_path = output_path + '/senate/'
    data_house_path = output_path + '/house/'
    data_governor_path = output_path + '/governor/'

    if os.path.isdir(output_path) is False:
        os.mkdir(output_path)

    if os.path.isdir(data_pres_path) is False:
        os.mkdir(data_pres_path)

    file_nat = open(data_pres_path + "national_2012.csv", "w")
    file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Percentage,Votes\n")
    file_nat.close()

    for state in states:
        try:
            st = us.states.lookup(state)
            st = str(st).replace(" ","-").lower()
            print st
            # try:
            url = website_president + st + '/'
            hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
            req = urllib2.Request(url, None, headers = hdrs)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page.read())
            file_nat = open(data_pres_path + "national_2012.csv", "a")
            file_state = open(data_pres_path + state + "_2012.csv", "w")
            file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
            # try:
            # except:
            if soup.find('tbody', id=re.compile('(county.*)[0-9]')) == False:
                for res_table in soup.find_all('tbody'):
                    county_name = state
                    for tr in res_table.find_all('tr'):
                        th_name = tr.find('th', class_='results-candidate').get_text()
                        tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                        if tds_party != "R" and tds_party != "D":
                            tds_party = 'I'
                        tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                        tds_tot = tr.find('td', class_='results-popular').get_text()
                        try:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        except:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
            else:
                for res_table in soup.find_all('tbody', id=re.compile('(county.*)[0-9]')):
                    county_name = res_table.find('th', class_='results-county').get_text()
                    del_temp = res_table.find('span', class_='precincts-reporting').get_text()
                    county_name = str(county_name).split(" " + str(del_temp))[0]
                    if not "County" in county_name and not "City" in county_name:
                        county_name = county_name + " County"
                    for tr in res_table.find_all('tr'):
                        th_name = tr.find('th', class_='results-candidate').get_text()
                        tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                        if tds_party != "R" and tds_party != "D":
                            tds_party = 'I'
                        tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                        tds_tot = tr.find('td', class_='results-popular').get_text()
                        try:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        except:
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
            file_state.close()
            file_nat.close()
            time.sleep(np.random.uniform(5,17.6))
        except:
            pass

    if scrape_all == True:

        if os.path.isdir(data_senate_path) is False:
            os.mkdir(data_senate_path)

        if os.path.isdir(data_house_path) is False:
            os.mkdir(data_house_path)

        if os.path.isdir(data_governor_path) is False:
            os.mkdir(data_governor_path)

        file_nat = open(data_senate_path + "national_2012.csv", "w")
        file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Votes,Percentage\n")
        file_nat.close()

        for state in states:
            try:
                st = us.states.lookup(state)
                st = str(st).replace(" ","-").lower()
                # try:
                url = website_senate + st + '/'
                hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                req = urllib2.Request(url, None, headers = hdrs)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page.read())
                file_nat = open(data_senate_path + "national_2012.csv", "a")
                file_state = open(data_senate_path + state + "_2012.csv", "w")
                file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
                # try:
                # except:
                if soup.find('tbody', id=re.compile('(county.*)[0-9]')) == False:
                    for res_table in soup.find_all('tbody'):
                        county_name = state
                        for tr in res_table.find_all('tr'):
                            th_name = tr.find('th', class_='results-candidate').get_text()
                            tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                            if tds_party != "R" and tds_party != "D":
                                tds_party = 'I'
                            tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                            tds_tot = tr.find('td', class_='results-popular').get_text()
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                else:
                    for res_table in soup.find_all('tbody', id=re.compile('(county.*)[0-9]')):
                        county_name = res_table.find('th', class_='results-county').get_text()
                        del_temp = res_table.find('span', class_='precincts-reporting').get_text()
                        county_name = str(county_name).split(" " + str(del_temp))[0]
                        if not "County" in county_name and not "City" in county_name:
                            county_name = county_name + " County"
                        for tr in res_table.find_all('tr'):
                            th_name = tr.find('th', class_='results-candidate').get_text()
                            tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                            if tds_party != "R" and tds_party != "D":
                                tds_party = 'I'
                            tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                            tds_tot = tr.find('td', class_='results-popular').get_text()
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                file_state.close()
                file_nat.close()
                time.sleep(np.random.uniform(5,17.6))
            except:
                pass

        file_nat = open(data_governor_path + "national_2012.csv", "w")
        file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Votes,Percentage\n")
        file_nat.close()

        for state in states:
            try:
                st = us.states.lookup(state)
                st = str(st).replace(" ","-").lower()
                # try:
                url = website_governor + st + '/'
                hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                req = urllib2.Request(url, None, headers = hdrs)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page.read())
                file_nat = open(data_senate_path + "national_2012.csv", "a")
                file_state = open(data_governor_path + state + "_2012.csv", "w")
                file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
                # try:
                # except:
                if soup.find('tbody', id=re.compile('(county.*)[0-9]')) == False:
                    for res_table in soup.find_all('tbody'):
                        county_name = state
                        for tr in res_table.find_all('tr'):
                            th_name = tr.find('th', class_='results-candidate').get_text()
                            tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                            if tds_party != "R" and tds_party != "D":
                                tds_party = 'I'
                            tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                            tds_tot = tr.find('td', class_='results-popular').get_text()
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                else:
                    for res_table in soup.find_all('tbody', id=re.compile('(county.*)[0-9]')):
                        county_name = res_table.find('th', class_='results-county').get_text()
                        del_temp = res_table.find('span', class_='precincts-reporting').get_text()
                        county_name = str(county_name).split(" " + str(del_temp))[0]
                        if not "County" in county_name and not "City" in county_name:
                            county_name = county_name + " County"
                        for tr in res_table.find_all('tr'):
                            th_name = tr.find('th', class_='results-candidate').get_text()
                            tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                            if tds_party != "R" and tds_party != "D":
                                tds_party = 'I'
                            tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                            tds_tot = tr.find('td', class_='results-popular').get_text()
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                file_state.close()
                file_nat.close()
                time.sleep(np.random.uniform(5,17.6))
            except:
                pass

        file_nat = open(data_house_path + "national_2012.csv", "w")
        file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Votes,Percentage\n")
        file_nat.close()

        for state in states:
            try:
                st = us.states.lookup(state)
                st = str(st).replace(" ","-").lower()
                # try:
                url = website_house + st + '/'
                hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                req = urllib2.Request(url, None, headers = hdrs)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page.read())
                file_nat = open(data_house_path + "national_2012.csv", "a")
                file_state = open(data_house_path + state + "_2012.csv", "w")
                file_state.write("District,Party,St_FIPS,Candidate,Votes,Percentage\n")
                if soup.find('tbody', id=re.compile('(district.*)[0-9]')) == False:
                    for res_table in soup.find_all('tbody'):
                        county_name = state
                        for tr in res_table.find_all('tr'):
                            th_name = tr.find('th', class_='results-candidate').get_text()
                            tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                            if tds_party != "R" and tds_party != "D":
                                tds_party = 'I'
                            tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                            tds_tot = tr.find('td', class_='results-popular').get_text()
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                else:
                    for res_table in soup.find_all('tbody', id=re.compile('(district.*)[0-9]')):
                        county_name = res_table.find('th', class_='results-county').get_text()
                        del_temp = res_table.find('span', class_='precincts-reporting').get_text()
                        county_name = str(county_name).split(" " + str(del_temp))[0]
                        for tr in res_table.find_all('tr'):
                            th_name = tr.find('th', class_='results-candidate').get_text()
                            tds_party = tr.find('td', class_='results-party').get_text().replace("Dem", "D").replace("GOP", "R")
                            if tds_party != "R" and tds_party != "D":
                                tds_party = 'I'
                            tds_pct = tr.find('td', class_='results-percentage').get_text().replace("%","")
                            tds_tot = tr.find('td', class_='results-popular').get_text()
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + th_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                file_state.close()
                file_nat.close()
                time.sleep(np.random.uniform(5,17.6))
            except:
                pass
