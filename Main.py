###########################################Author###############################################################
#Author: Ben Griffy
#Institution: University of California, Santa Barbara
#email: griffy@umail.ucsb.edu
#website: https://sites.google.com/site/bengriffy/home
#Date: Nov. 2016
#Created for: econsnapshot.com
################################################################################################################

from __future__ import division
import os
from Model_Wrapper import ModelWrapper

###########################################Modules##############################################################
#required programs: python, R, Stata (for statistical analysis)
#python modules:
#R modules:
################################################################################################################

path = os.path.dirname(os.path.abspath(__file__))

# data_path = pd.read_csv(path + "/Data/Smoothed_Profiles.csv", delimiter=",")
# script_path = pd.read_csv(path + "/Data/Weights.csv", delimiter=",")
data_path = path + '/data/'
scripts_path = path + '/scripts/'
graphics_path = path + '/graphics/'

############################################Options#############################################################
#download_options: check model_wrapper.py for default options.
#years: select years for download. currently supports 2004, 2008, 2012, 2016.
#replace: select either individual years to replace, or write True to replace all. False will download files not
#found
#down_ballot: download down-ballot (senate, house, local, etc.) at the county-level when available.
#covariates: select covariates to download and merge. currently supports BEA income, BLS unemployment,
#BLS industry, and ACS demographics. 
#extra_datasets: download and merge extra sets of covariates that we used for additional analysis. this includes
#data on the Voting Rights Act (RIP), manufacturing employment, and voting machines.
#merge_datasets: combine all datasets on county_fips
#graphics_options:
#graph_maps: plot data on maps. Only requires beautifulsoup, as the image is generated on an SVG document.
#interactive: plot data to interactive maps.
#diff_plots: plot difference between 2012 and 2016 percent vote
################################################################################################################

# download_options = {'years': ['2004','2008','2012','2016'], 'replace': ['2004','2008','2012','2016'],
#                     'down_ballot':True, 'covariates': ['income','unemployment','industry','demographics'],
#                     'extra_datasets': True, 'merge_datasets': True,
# }

download_options = {'years': ['2004','2008','2012','2016'], 'replace': False,
                    'down_ballot': True, 'covariates': ['income','unemp','demographics','education','industry'],
                    'extra_datasets': False, 'merge_datasets': False,
}

graphics_options = {'graph_maps': True, 'interactive': True,
                    'diff_plots': False,
}

opts = {
    'download_opts':download_options,
    'graphics_opts':graphics_options,
    'data_loc': data_path,
    'scripts_loc': scripts_path,
    'graphics_loc': graphics_path,
}


model = ModelWrapper(opts = opts)

model.Run_Model()
