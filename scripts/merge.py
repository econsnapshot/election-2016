################################################################################################################
#Author: Ben Griffy
#Institution: University of California, Santa Barbara
#email: griffy@umail.ucsb.edu
#website: https://sites.google.com/site/bengriffy/home
#Date:
################################################################################################################

from __future__ import division

import pandas as pd
import os

def merge_data(series, merge_opts, output, temp, merge_var, year = None):

    print series
    print year

    if os.path.isdir(temp) is False:
        os.mkdir(temp)

    data_temp = pd.read_csv(series, delimiter = ',', header = 0)
    if merge_opts['pivot_column'] == None:
        data_temp[merge_var] = pd.to_numeric(data_temp[merge_var], errors = 'coerce')
        data_temp[merge_var] = data_temp[merge_var].astype(float)
        if os.path.isfile(output):
            data = pd.read_csv(output, delimiter = ',', header = 0)
            data_final = pd.merge(data, data_temp, on = merge_var, how = 'outer')
            data_final.to_csv(output, sep = ',', index = False, mode = 'w')
        else:
            data_temp.to_csv(output, sep = ',', index = False, mode = 'w')

    else:
        for pv_vals in merge_opts['pivot_values']:
            # try:
            data_temp[pv_vals] = data_temp[pv_vals].str.replace("%","")
            data_temp[pv_vals] = pd.to_numeric(data_temp[pv_vals], errors = 'coerce')
            # except:
            #     pass
                # print pv_vals
                # print data_temp[pv_vals]
        
        data_temp[merge_opts['pivot_column']] = data_temp[merge_opts['pivot_column']].str.replace("Dem","D")
        data_temp[merge_opts['pivot_column']] = data_temp[merge_opts['pivot_column']].str.replace("Democrat","D")
        data_temp[merge_opts['pivot_column']] = data_temp[merge_opts['pivot_column']].str.replace("GOP","R")
        data_temp[merge_opts['pivot_column']] = data_temp[merge_opts['pivot_column']].str.replace("Rep","R")
        data_temp[merge_opts['pivot_column']] = data_temp[merge_opts['pivot_column']].str.replace("Republican","R")
        data_temp.loc[~(data_temp[merge_opts['pivot_column']].isin(['D','R'])),merge_opts['pivot_column']] = "I"
        data_temp = data_temp.pivot_table(index = merge_var, columns = merge_opts['pivot_column'], values = merge_opts['pivot_values'])
        data_temp.columns = ['_'.join(col).strip() + "_" + year for col in data_temp.columns.values]
        data_temp[merge_var] = data_temp.index
        data_temp[merge_var] = data_temp[merge_var].astype(float)
        # for i in data_temp.iterrows():
        #     if data_temp.index.ix[i] == merge_var:
        #         data_temp[:].ix[i] = 
        #     except:
        #         pass
        if os.path.isfile(output):
            data = pd.read_csv(output, delimiter = ',', header = 0)
            data_final = pd.merge(data, data_temp, on = merge_var, how = 'outer')
            # data_temp.to_csv(temp + '/temp.csv', sep = ',', index = False, mode = 'w')
            # data = pd.read_csv(temp + '/temp.csv', delimiter = ',', header = 0)
            data_final.to_csv(output, sep = ',', index = False, mode = 'w')
        else:
            data_temp.to_csv(output, sep = ',', index = False, mode = 'w')
