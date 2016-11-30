#Election 2016 Analysis for Econsnapshot.com

Author: Ben Griffy

Institution: University of California, Santa Barbara

email: griffy@umail.ucsb.edu

website: https://sites.google.com/site/bengriffy/home

Date: 11/28/2016

Topic: 2016 election

This is a series of files written in Python to download, merge, and perform analysis on data related to the 2016 election. This code was used to generate the blog posts on the election at www.econsnapshot.com, run by Thomas Cooley, Ben Griffy, and Peter Rupert. We are releasing the data and codes so that others can explore the results that drove the election, as well as gain more experience with scraping and performing statistical analysis in Python (us included!).

1: Software

The easiest way to get all of these modules to work on a PC is to install Anaconda, as a number of the modules are at least partially Unix-based, which makes them difficult to work on a PC. A Mac or a Linux computer should not have these problems. The only non-standard program are phantomjs, which is a program required to make the web-scraper run silently. All others should be available via pip.

2: Options

At this time, the software can scrape data from 4 different websites for the 2004, 2008, 2012, and 2016 elections, including down-ballot elections. Options are given in the file "Main.py," as follows:

download_options = {'years': ['2004','2008','2012','2016'], 'replace': ['2004','2008','2012','2016'],
                    'down_ballot':True, 'covariates': ['income','unemployment','industry','demographics'],
                    'extra_datasets': True, 'merge_datasets': True,
}

download_options: check model_wrapper.py for default options.
years: select years for download. currently supports 2004, 2008, 2012, 2016.
replace: select either individual years to replace, or write True to replace all. False will download files not
found
down_ballot: download down-ballot (senate, house, local, etc.) at the county-level when available.
covariates: select covariates to download and merge. currently supports BEA income, BLS unemployment,
BLS industry, and ACS demographics. 
extra_datasets: download and merge extra sets of covariates that we used for additional analysis. this includes
data on the Voting Rights Act (RIP), manufacturing employment, and voting machines. currently not merging, but can be manually merged.
merge_datasets: combine all datasets on county_fips

Some of these options are currently unavailable, but will be updated shortly.

graphics_options = {'graph_maps': True, 'ggplot': True, 'interactive': False,
                    'diff_plots': True
}

graph_maps: plot data on maps.
interactive: plot data to interactive maps.
diff_plots: plot difference between 2012 and 2016 percent vote

At the moment, we are using a Python module to create the maps, but may use ggplot in the future. Our current setup allows for interactive plotting.

To run the program, go to the commandline or your favorite IDE and run "Main.py" with your options set.

Basic Outline:

1: Scrape data from news websites. 

2: Clean data and merge

3: Map data at the county level

4: Import into Stata for statistical analysis
