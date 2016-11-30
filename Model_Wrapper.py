################################################################################################################
#Author: Ben Griffy
#Institution: University of California, Santa Barbara
#email: griffy@umail.ucsb.edu
#website: https://sites.google.com/site/bengriffy/home
#Date:
################################################################################################################
from __future__ import division
import os
from scripts.scraper_2016 import scraper_2016
from scripts.scraper_2012 import scraper_2012
from scripts.scraper_2004 import scraper_2004
from scripts.covariates_scraper import scraper_economics
from scripts.covariates_cleaner import clean_covariates
from scripts.covariates_cleaner import clean_demographics
from scripts.covariates_scraper import scraper_economics as scraper_demographics
# from scripts import scraper_unemp
# from scripts import scraper_demog
# from scripts import scraper_ind
# from scripts import scraper_extras
from scripts.plot_maps import plot_maps
from scripts.merge import merge_data
import platform
import zipfile as zf
import subprocess as subprocess

path = os.path.dirname(os.path.abspath(__file__))

class ModelWrapper:

    def __init__(self, **kwargs):
        
        default_download_options = {'years': ['2004','2008','2012','2016'], 'replace': False,
                                    'down_ballot': ['2004','2008','2012','2016'], 'covariates': ['income','unemployment','industry','demographics'],
                                    'extra_datasets': True, 'merge_datasets': True,
        }
        default_graphics_options = {'graph_maps': True, 'ggplot': True, 'interactive': False,
                                    'diff_plots': True
        }
        
        default_series_options = {'president':{'title':'Presidential Election (% Dem Votes), ','column':'Percentage','subset':'D','subset_column':'Party','match_column':'County_FIPS','low_color':"#FF0000",'high_color':"#0000FF"},
                                  'senate':{'title':'Senate Elections (% Dem Votes), ','column':'Percentage','subset':'D','subset_column':'Party','match_column':'County_FIPS','low_color':"#FF0000",'high_color':"#0000FF"},
                                  'house':{'title':'House Elections (% Dem Votes), ','column':'Percentage','subset':'D','subset_column':'Party','match_column':'County_FIPS','low_color':"#FF0000",'high_color':"#0000FF"},
                                  'governor':{'title':'Gubernatorial Elections (% Dem Votes), ','column':'Percentage','subset':'D','subset_column':'Party','match_column':'County_FIPS','low_color':"#FF0000",'high_color':"#0000FF"},
                                  'income':{'title':'Income Levels','column':'Inc_2015','subset':None,'subset_column':'Party','match_column':'County_FIPS','low_color':"#00fa9a",'high_color':"#ffd700"},
                                  'unemp':{'title':'Unemployment Rate','column':'Unemp_Rate','subset':None,'subset_column':'Party','match_column':'County_FIPS','low_color':"#00fa9a",'high_color':"#ffd700"},
                                  'education':{'title':'Percent with HS Degree or less','column':'pct_hs_less','subset':None,'subset_column':'Party','match_column':'County_FIPS','low_color':"#00fa9a",'high_color':"#ffd700"},
                                  'industry':{'title':'Estabs % Change','column':'oty_qtrly_estabs_pct_chg','subset':10,'subset_column':'industry_code','match_column':'County_FIPS','low_color':"#00fa9a",'high_color':"#ffd700"},
                                  'demographics':{'title':'Percent White','column':'pct_white','subset':None,'subset_column':'Party','match_column':'County_FIPS','low_color':"#00fa9a",'high_color':"#ffd700"},
        }

        default_merge_options = {'president':{'pivot_column':'Party','pivot_values':['Percentage'],},
                                  'senate':{'pivot_column':'Party','pivot_values':['Percentage','Votes'],},
                                  'house':{'pivot_column':'Party','pivot_values':['Percentage','Votes'],},
                                  'governor':{'pivot_column':'Party','pivot_values':['Percentage','Votes'],},
                                  'income':{'pivot_column':None,'pivot_values':['Percentage','Votes'],},
                                  'unemp':{'pivot_column':None,'pivot_values':['Percentage','Votes'],},
                                  'education':{'pivot_column':None,'pivot_values':['Percentage','Votes'],},
                                  'industry':{'pivot_column':None,'pivot_values':['Percentage','Votes'],},
                                  'demographics':{'pivot_column':None,'pivot_values':['Percentage','Votes'],},
        }
        
        self.opts = kwargs.get('opts')
        self.download_opts = self.opts.get('download_opts',default_download_options)
        self.graphics_opts = self.opts.get('graphics_opts',default_graphics_options)
        self.series_opts = self.opts.get('series_opts',default_series_options)
        self.merge_opts = self.opts.get('merge_opts',default_merge_options)
        self.data_path = self.opts.get('data_loc',path + '/data/')
        self.graphics_path = self.opts.get('graphics_loc',path + '/graphics/')
        
    def Run_Model(self):
        os.environ['PATH'] += str(';' + path)
        if self.download_opts['replace'] == True:
            system = platform.system()
            if system == "Windows":
                if os.path.isdir(path + '/scripts/phantomjs-windows/') is False:
                    install_phantomjs = raw_input("To download all of the data, you need PhantomJS. Install? [y/n] ")
                    if install_phantomjs == "y":
                        for filename in os.listdir(path + '/scripts/'):
                            if filename.endswith('-windows.zip'):
                                with zf.ZipFile(path + "/scripts/" + filename, "r") as z:
                                    z.extractall(path + "/scripts/phantomjs-windows/")
            elif system == "Darwin":
                if os.path.isdir(path + '/scripts/phantomjs-mac/') is False:
                    install_phantomjs = raw_input("To download all of the data, you need PhantomJS. Install? [y/n] ")
                    if install_phantomjs == "y":
                        for filename in os.listdir(path + '/scripts/'):
                            if filename.endswith('-macosx.zip'):
                                with zf.ZipFile(path + "/scripts/" + filename, "r") as z:
                                    z.extractall(path + "/scripts/phantomjs-windows/")
            elif system == "Linux":
                if os.path.isdir(path + '/scripts/phantomjs-linux/') is False:
                    install_phantomjs = raw_input("To download all of the data, you need PhantomJS. Install? [y/n] ")
                    if install_phantomjs == "y":
                        for filename in os.listdir(path + '/scripts/'):
                            if filename.endswith('-linux-x86_64.zip'):
                                with zf.ZipFile(path + "/scripts/" + filename, "r") as z:
                                    z.extractall(path + "/scripts/phantomjs-windows/")
            else:
                system_type = raw_input("Python could not detect your system type. Please enter your system type, one of \"Windows\", \"Mac\", \"Linux\".")
                system_type = system_type.lower()
                syst_dict = {'windows':'windows','mac':'macosx','linux':'linux-x86_64'}
                if os.path.isdir(path + '/scripts/phantomjs-' + system_type + '/') is False:
                    install_phantomjs = raw_input("To download all of the data, you need PhantomJS. Install? [y/n] ")
                    if install_phantomjs == "y":
                        for filename in os.listdir(path + '/scripts/'):
                            if filename.endswith('-' + syst_dict[system_type] + '.zip'):
                                with zf.ZipFile(path + "/scripts/" + filename, "r") as z:
                                    z.extractall(path + "/scripts/phantomjs-" + system_type + "/")
                        
        
        if self.download_opts['replace'] == True:
            for year in self.download_opts['years']:
                if self.download_opts['down_ballot'] == True:
                    down_ballot_scrape = True
                else:
                    down_ballot_scrape = False
                self.download_election_data(date = year, output_path = self.data_path + 'election-' + str(year) + '/', down_ballot_scrape = down_ballot_scrape, replace_files = self.download_opts['replace'])
            for covariate in self.download_opts['covariates']:
                self.download_covariate_data(covariate, self.data_path + '/covariates/' + str(covariate) + '/', self.download_opts['replace'])
                self.clean_covariate_data(covariate, self.data_path + '/covariates/' + str(covariate) + '/', self.download_opts['replace'])
                self.clean_covariate_data(covariate, self.data_path + '/covariates/' + str(covariate) + '/', self.download_opts['replace'])
        # if self.download_opts['extra_datasets'] == True:
        #     self.download_extra_data(self.data_path + '/other/')
        if self.graphics_opts['graph_maps'] == True:
            for year in self.download_opts['years']:
                print year
                self.graph_maps(input_path = self.data_path + '/election-' + str(year) + '/president/national_' + str(year) + '.csv', series_name = 'president', output_path = self.graphics_path, year = year, series_options = self.series_opts)
                if self.download_opts['down_ballot'] == True:
                # for year in self.download_opts['down_ballot']:
                    try:
                        self.graph_maps(input_path = self.data_path + '/election-' + str(year) + '/senate/national_' + str(year) + '.csv', series_name = 'senate', output_path = self.graphics_path, year = year, series_options = self.series_opts)
                    # self.graph_maps(input_path = self.data_path + '/election-' + str(year) + '/house/national_' + str(year) + '.csv', series_name = 'house', output_path = self.graphics_path, year = year, series_options = self.series_opts)
                        self.graph_maps(input_path = self.data_path + '/election-' + str(year) + '/governor/national_' + str(year) + '.csv', series_name = 'governor', output_path = self.graphics_path, year = year, series_options = self.series_opts)
                    except:
                        pass
            for covariate in self.download_opts['covariates']:
                self.graph_maps(input_path = self.data_path + '/covariates/' + str(covariate) + '.csv', series_name = covariate, year = None, output_path = self.graphics_path, series_options = self.series_opts)

        if os.path.isfile(self.data_path + '/merged_data.csv'):
            os.remove(self.data_path + '/merged_data.csv')

        for year in self.download_opts['years']:
            self.merge_vars(series = self.data_path + 'election-' + str(year) + '/president/national_' + str(year) + '.csv', merge_opts = self.merge_opts.get('president'), output = self.data_path + '/merged_data.csv', temp = self.data_path + '/tmp/', year = year, merge_var = 'County_FIPS')

        for covariate in self.download_opts['covariates']:
            self.merge_vars(series = self.data_path + '/covariates/' + str(covariate) + '.csv', merge_opts = self.merge_opts.get(covariate), output = self.data_path + '/merged_data.csv', temp = self.data_path + '/tmp/', year = year, merge_var = 'County_FIPS')

    def download_election_data(self, date, output_path, down_ballot_scrape, replace_files):
        if date == '2016':
            scraper_2016(output_path, down_ballot_scrape, replace_files)
        if date == '2012':
            scraper_2012(output_path, down_ballot_scrape, replace_files)
        if date == '2008':
            subprocess.call(['python', path + '/scripts/scraper_2008.py'], shell = True)
            if down_ballot_scrape == True:
                subprocess.call(['python', path + '/scripts/scraper_2008_downballot.py'], shell = True)
        if date == '2004':
            scraper_2004(output_path, down_ballot_scrape, replace_files)

    def download_covariate_data(self, series, output_path, replace_files):
        if series != "demographics":
            scraper_economics(series, output_path, replace_files)
        if series == "demographics":
            pass
            # scraper_demographics(series, output_path, replace_files)

    def clean_covariate_data(self, series, output_path, replace_files):
        clean_covariates(series, output_path, replace_files)
        if series == 'demographics':
            clean_demographics(output_path)

    # def download_extra_data(output_path):
    #     scraper_extras(output_path)

    def graph_maps(self, input_path, series_name, output_path, series_options, year = None):
        if year == None:
            output = output_path + '/' + series_name
        else:
            output = output_path + '/' + series_name + "_" + year
        plot_maps(input_path, output, series_options, year, series_name)

    def merge_vars(self, series, merge_opts, output, temp, merge_var, year = None):
        merge_data(series, merge_opts, output, temp, merge_var, year)
