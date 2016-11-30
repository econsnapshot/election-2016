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

def clean_covariates(series, output_path, replace_files):

    states = ["ak","al","ar","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id","il","in","ks","ky","la","ma","md","me","mh","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj","nm","nv","ny", "oh","ok","or","pa","pr","pw","ri","sc","sd","tn","tx","ut","va","vi","vt","wa","wi","wv","wy"]

    main_folder = os.path.dirname(os.path.abspath('__file__'))

    fips = pd.read_csv(main_folder + '/data/fips/' + 'fips.csv')

    af = addfips.AddFIPS()

    data_location_path = main_folder + '/data/covariates/location/'
    data_industry_path = main_folder + '/data/covariates/industry/'
    data_unemp_path = main_folder + '/data/covariates/unemp/'
    data_income_path = main_folder + '/data/covariates/income/'

    if os.path.isdir(data_location_path) is False:
        os.mkdir(data_location_path)

    if os.path.isdir(data_industry_path) is False:
        os.mkdir(data_industry_path)

    if os.path.isdir(data_unemp_path) is False:
        os.mkdir(data_unemp_path)

    if os.path.isdir(data_income_path) is False:
        os.mkdir(data_income_path)


    crosswalk = us.states.mapping('name','abbr')

    if series == "income":
        inc_data = pd.read_excel(data_income_path + "/income_uncleaned.xlsx", header = None, names=['County','Inc_2013','Inc_2014','Inc_2015','Inc_Rank','Pct_Chg_2014','Pct_Chg_2015','Pct_Rank'], skiprows = 6)
        inc_data = inc_data.dropna()
        state_temp = []

        for i in inc_data.iterrows():
            try:
                state_temp.append(crosswalk[inc_data['County'].ix[i]])
            except:
                state_temp.append("")

        inc_data['drop'] = state_temp

        for i in range(0,len(state_temp)):
            if i > 0:
                if state_temp[i] == "":
                    state_temp[i] = state_temp[i-1]

        inc_data['State'] = state_temp

        county_fips = []
        for i in inc_data.iterrows():
            try:
                county_fips.append(str(af.get_county_fips(str(inc_data['County'].ix[i]), str(inc_data['State'].ix[i]))))
            except:
                county_fips.append(str(0))

        inc_data['County_FIPS'] = county_fips

        inc_data = inc_data[inc_data['drop'] == ""]

        inc_data = inc_data.drop('drop', axis = 1)


        inc_data.to_csv(main_folder + '/data/covariates/income.csv', index = False, sep = ",", encoding='utf-8', mode = 'w')

    if series == "industry":
        ind_data = pd.read_csv(data_industry_path + "/10.csv")
        ind_data = ind_data.rename(columns={'area_fips':'County_FIPS'})
        ind_data = ind_data[ind_data['agglvl_code'] == 70]
        ind_data.to_csv(main_folder + '/data/covariates/industry.csv', index = False, mode = 'w')

    if series == "unemp":
        unemp_data = pd.read_table(data_unemp_path + "/unemployment.txt", sep = '|', skiprows = 6, header = None, names = ['LAUS','FIPS1','FIPS2','Name','Period','Labor_Force','Employed','Unemp_Level','Unemp_Rate'])
        unemp_data['County_FIPS'] = unemp_data['LAUS'].str.slice(start=3,stop=8)
        unemp_data = unemp_data[unemp_data['Period'].str.strip().isin(['Sep-16(p)'])]
        unemp_data = unemp_data[['Name','Labor_Force','Employed','Unemp_Level','Unemp_Rate','County_FIPS']]
        unemp_data = unemp_data[['Name','Labor_Force','Employed','Unemp_Level','Unemp_Rate','County_FIPS']]
        drop = []
        for i in unemp_data.iterrows():
            try:
                float(unemp_data['County_FIPS'].ix[i])
                drop.append(0)
            except:
                drop.append(1)
        unemp_data['drop'] = drop
        unemp_data = unemp_data[unemp_data['drop'] == 0]
        unemp_data = unemp_data.drop('drop',axis=1)
        # unemp_data['Unemp_Rate'] = unemp_data['Unemp_Rate'].str.replace(',','')
        # unemp_data['Unemp_Level'] = unemp_data['Unemp_Level'].str.replace(',','')
        # unemp_data['Employed'] = unemp_data['Employed'].str.replace(',','')
        # unemp_data['Labor_Force'] = unemp_data['Labor_Force'].str.replace(',','')
        unemp_data.to_csv(main_folder + '/data/covariates/unemp.csv', index = False, mode = 'w')

def clean_demographics(output_path):
    main_folder = os.path.dirname(os.path.abspath('__file__'))
    data_path = main_folder + '/data/covariates/demographics/'

    if os.path.isdir(data_path) is False:
        os.mkdir(data_path)

    pop_data_temp = pd.read_csv(data_path + "/demographics.csv", skiprows = 1, header = 0)
    pop_data_temp = pop_data_temp.rename(columns={'Id2':'County_FIPS'})
    pop_data = pop_data_temp[['County_FIPS','HC01_VC03','HC03_VC04','HC03_VC05','HC03_VC28','HC03_VC88','HC03_VC94','HC03_VC95']]
    pop_data = pop_data.rename(columns={'HC01_VC03':'total_pop','HC03_VC04':'pct_male','HC03_VC05':'pct_female','HC03_VC28':'pct_old','HC03_VC88':'pct_latino','HC03_VC94':'pct_white','HC03_VC95':'pct_black'})
    pop_data.to_csv(main_folder + '/data/covariates/demographics.csv', index = False, mode = 'w')

    ed_data = pd.read_csv(data_path + "/education.csv", header = 0)
    ed_data = ed_data.rename(columns={'HD01_VD01':'total_pop','HD01_VD02':'pct_no_hs','HD01_VD03':'pct_some_hs','HD01_VD04':'pct_hs','HD01_VD05':'pct_some_college','HD01_VD06':'pct_associates','HD01_VD07':'pct_bachelors','HD01_VD08':'pct_graduate'})
    ed_data['pct_no_hs'] = ed_data['pct_no_hs']/ed_data['total_pop']*100
    ed_data['pct_some_hs'] = ed_data['pct_some_hs']/ed_data['total_pop']*100
    ed_data['pct_hs'] = ed_data['pct_hs']/ed_data['total_pop']*100
    ed_data['pct_some_college'] = ed_data['pct_some_college']/ed_data['total_pop']*100
    ed_data['pct_associates'] = ed_data['pct_associates']/ed_data['total_pop']*100
    ed_data['pct_bachelors'] = ed_data['pct_bachelors']/ed_data['total_pop']*100
    ed_data['pct_graduate'] = ed_data['pct_graduate']/ed_data['total_pop']*100
    ed_data['pct_hs_less'] = ed_data['pct_hs'] + ed_data['pct_some_hs'] + ed_data['pct_no_hs']
    ed_data = ed_data[['County_FIPS','pct_no_hs','pct_some_hs','pct_hs','pct_some_college','pct_associates','pct_bachelors','pct_graduate','pct_hs_less']]
    ed_data.to_csv(main_folder + '/data/covariates/education.csv', index = False, mode = 'w')
