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

def scraper_2016(output_path, scrape_all, replace):

    af = addfips.AddFIPS()

    states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id", "il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

    data_pres_path = output_path + '/president/'
    data_senate_path = output_path + '/senate/'
    data_house_path = output_path + '/house/'
    data_governor_path = output_path + '/governor/'

    if os.path.isdir(output_path) is False:
        os.mkdir(output_path)
    
    if os.path.isdir(data_pres_path) is False:
        os.mkdir(data_pres_path)

    website_president = 'http://www.realclearpolitics.com/elections/live_results/2016_general/president/'
    website_president_2_part1 = 'http://uselectionatlas.org/RESULTS/datagraph.php?year=2016&fips='
    website_president_2_part2 = '&f=1&off=0&elect=0'
    website_senate = 'http://www.realclearpolitics.com/elections/live_results/2016_general/senate/'
    website_house = 'http://www.realclearpolitics.com/elections/live_results/2016_general/house/'
    website_governor = 'http://www.realclearpolitics.com/elections/live_results/2016_general/governor/'

    file_nat = open(data_pres_path + "national_2016.csv", "w")
    file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Percentage,Votes\n")
    file_nat.close()
    for state in states:
        county_fips = 1
        while county_fips != None:
            try:
                url = website_president + state + '.html'
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                req = urllib2.Request(url, None, headers)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page.read())
                file_nat = open(data_pres_path + "national_2016.csv", "a")
                file_state = open(data_pres_path + state + "_2016.csv", "w")
                file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
                for res_table in soup.find_all('div', class_='county_section'):
                    for head in res_table.find_all('div', class_='header'):
                        county_name = head.find('span', class_='title').get_text()
                        county_name = str(county_name).split(" County")[0] + " County"
                        county_fips = af.get_county_fips(county_name, state)
                    for tr in res_table.find_all('tr'):
                        tds_name = tr.find('td', class_='name').get_text()
                        tds_party = tr.find('span', class_='bubble').get_text().replace('GOP','R').replace('Dem','D').replace('Ind','I')
                        tds_pct = tr.find('td', class_='percentage').get_text().replace("%","")
                        tds_tot = tr.find('td', class_='votes').get_text()
                        if county_name != 'Final Results' and county_fips != None:
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                        elif state == 'ak' and county_name != 'Final Results':
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            county_fips = 1
                        elif 'City' in str(county_name):
                            county_fips = 1
                file_state.close()
                file_nat.close()
                time.sleep(np.random.uniform(5,17.6))
            except:
                pass
            break

        if county_fips == None:
            df = pd.read_csv(data_pres_path + "national_2016.csv")
            df = df[df['State'] != state]
            df.to_csv(data_pres_path + "national_2016.csv", index = False)
            if af.get_state_fips(state)[0] == '0':
                url = website_president_2_part1 + str(af.get_state_fips(state)[1]) + website_president_2_part2
            else:
                url = website_president_2_part1 + str(af.get_state_fips(state)) + website_president_2_part2
            hdrs = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*", 
            # "Accept-Encoding": "gzip, deflate, sdch, br", 
            "Accept-Language": "en-US,en;q=0.8", "Upgrade-Insecure-Requests": "1", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
            req = urllib2.Request(url, None, headers = hdrs)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page.read())
            file_nat = open(data_pres_path + "national_2016.csv", "a")
            file_state = open(data_pres_path + state + "_2016.csv", "w")
            file_state.write("County,County_FIPS,Party,Candidate,Percentage,Votes\n")
            for res_table in soup.find_all('table'):
                # print res_table
                for head in res_table.find_all('td', rowspan='4'):
                    county_name = head.find('b').get_text()
                    county_fips = af.get_county_fips(county_name, state)
                for tr in res_table.find_all('tr'):
                    try:
                        try:
                            tds_name = tr.find('td', class_='cnd').get_text()
                        except:
                            tds_name = tr.find_all('td')[0].get_text()
                        if tds_name == 'Clinton':
                            tds_party = 'D'
                        elif tds_name == 'Trump':
                            tds_party = 'R'
                        elif tds_name == 'Stein':
                            tds_party = 'I'
                        elif tds_name == 'Johnson':
                            tds_party = 'I'
                        elif tds_name == 'McMullin':
                            tds_party = 'I'
                        else:
                            tds_party = 'Unknown'
                        tds_pct = tr.find('td', class_='per').get_text()
                        tds_tot = tr.find('td', class_='dat').get_text()
                        if county_name != 'Final Results':
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
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

        file_nat = open(data_senate_path + "national_2016.csv", "w")
        file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Votes,Percentage\n")
        file_nat.close()

        for state in states:
            try:
                url = website_senate + state + '.html'
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                req = urllib2.Request(url, None, headers)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page.read())
                file_nat = open(data_senate_path + "national_2016.csv", "a")
                file_state = open(data_senate_path + state + "_2016.csv", "w")
                file_state.write("County,County_FIPS,Party,Candidate,Votes,Percentage\n")
                for res_table in soup.find_all('div', class_='county_section'):
                    for head in res_table.find_all('div', class_='header'):
                        county_name = head.find('span', class_='title').get_text()
                    for tr in res_table.find_all('tr'):
                        tds_name = tr.find('td', class_='name').get_text()
                        tds_party = tr.find('span', class_='bubble').get_text().replace('GOP','R').replace('Dem','D').replace('Ind','I')
                        tds_pct = tr.find('td', class_='percentage').get_text().replace("%","")
                        tds_tot = tr.find('td', class_='votes').get_text()
                        if county_name != 'Final Results':
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                file_state.close()
                file_nat.close()
                time.sleep(np.random.uniform(5,17.6))
            except:
                pass

        file_nat = open(data_house_path + "general_2016.csv", "w")
        file_nat.write("State,District,Party,St_FIPS,Candidate,Votes,Percentage\n")
        file_nat.close()

        for state in states:
            try:
                url = website_house + state + '.html'
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                req = urllib2.Request(url, None, headers)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page.read())
                file_nat = open(data_house_path + "national_2016.csv", "a")
                file_state = open(data_house_path + state + "_2016.csv", "w")
                file_state.write("District,Party,St_FIPS,Candidate,Votes,Percentage\n")
                for res_table in soup.find_all('div', class_='county_section'):
                    for head in res_table.find_all('div', class_='header'):
                        county_name = head.find('span', class_='title').get_text()
                    for tr in res_table.find_all('tr'):
                        tds_name = tr.find('td', class_='name').get_text()
                        tds_party = tr.find('span', class_='bubble').get_text().replace('GOP','R').replace('Dem','D').replace('Ind','I')
                        tds_pct = tr.find('td', class_='percentage').get_text().replace("%","")
                        tds_tot = tr.find('td', class_='votes').get_text()
                        if county_name != 'Final Results':
                            file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            file_state.write(county_name + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                file_state.close()
                file_nat.close()
                time.sleep(np.random.uniform(5,17.6))
            except:
                pass

        file_nat = open(data_governor_path + "national_2016.csv", "w")
        file_nat.write("State,County,Party,St_FIPS,County_FIPS,Candidate,Votes,Percentage\n")
        file_nat.close()

        for state in states:
            try:
                url = website_governor + state + '.html'
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
                req = urllib2.Request(url, None, headers)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page.read())
                file_nat = open(data_governor_path + "national_2016.csv", "a")
                file_state = open(data_governor_path + state + "_2016.csv", "w")
                file_state.write("County,County_FIPS,Party,Candidate,Votes,Percentage\n")
                for res_table in soup.find_all('div', class_='county_section'):
                    for head in res_table.find_all('div', class_='header'):
                        county_name = head.find('span', class_='title').get_text()
                    for tr in res_table.find_all('tr'):
                        tds_name = tr.find('td', class_='name').get_text()
                        tds_party = tr.find('span', class_='bubble').get_text().replace('GOP','R').replace('Dem','D').replace('Ind','I')
                        tds_pct = tr.find('td', class_='percentage').get_text().replace("%","")
                        tds_tot = tr.find('td', class_='votes').get_text()
                        if county_name != 'Final Results':
                            try:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + af.get_county_fips(county_name, state) + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + af.get_county_fips(county_name, state) + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                            except:
                                file_nat.write(state + "," + county_name + "," + tds_party + "," + af.get_state_fips(state) + "," + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                                file_state.write(county_name + "," + "," + tds_party + "," + tds_name + "," + tds_pct + "," + tds_tot.replace(",","") + "\n")
                file_state.close()
                file_nat.close()
                time.sleep(np.random.uniform(5,17.6))
            except:
                pass
