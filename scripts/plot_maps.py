### color_map.py
 
import csv
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup, Tag, NavigableString
from graph_helper import linear_gradient
from wand.api import library
import wand.color
import wand.image
import os

def plot_maps(input_path, output, options, year = None, series = False):
    main_folder = os.path.dirname(os.path.abspath('__file__'))
    # Read in unemployment rates
    final_var_dict = {}
    opts = options.get(series)
    data = pd.read_csv(input_path, delimiter=",", header = 0, index_col = False)
    for i in data.iterrows():
        # try:
        if opts['subset'] == None:
            try:
                match = int(data[opts['match_column']].ix[i])
            except:
                match = 0
            if match > 0:
                try:
                    temp_var = float( data[opts['column']].ix[i].replace("%","").strip() )
                except:
                    temp_var = float( data[opts['column']].ix[i] )
                # print temp_var
                final_var_dict[match] = temp_var
        else:
            try:
                if data[opts['subset_column']].ix[i].replace("Democratic","D").replace("Dem","D").replace("GOP","R") == opts['subset']:
                    match = data[opts['match_column']].ix[i].astype(int)
                    if match > 0:
                        try:
                            temp_var = float( data[opts['column']].ix[i].replace("%","").strip() )
                        except:
                            temp_var = float( data[opts['column']].ix[i] )
                        # print temp_var
                        final_var_dict[match] = temp_var
            except:
                if data[opts['subset_column']].ix[i] == opts['subset']:
                    match = pd.to_numeric(data[opts['match_column']].ix[i], errors = 'coerce')
                    if match > 0:
                        try:
                            temp_var = float( data[opts['column']].ix[i].replace("%","").strip() )
                        except:
                            temp_var = float( data[opts['column']].ix[i] )
                        # print temp_var
                        final_var_dict[match] = temp_var
                # print county_fips
                # print final_var_dict[county_fips]
        # except:
        #     pass

    min = np.min(final_var_dict.values())
    max = np.max(final_var_dict.values())
    if np.mean(final_var_dict.values()) < max/2:
        max = np.percentile(final_var_dict.values(),90)
    if np.mean(final_var_dict.values()) > min*2:
        min = np.percentile(final_var_dict.values(),10)

        
    # Load the SVG map
    svg = open(main_folder + '/data/maps/counties.svg', 'r').read()

    # Load into Beautiful Soup
    soup = BeautifulSoup(svg, 'xml')
    if year == None:
        soup.find('tspan', attrs={'fill':'black'}).string = opts['title']
    else:
        soup.find('tspan', attrs={'fill':'black'}).string = opts['title'] + year

    # Find counties
    paths = soup.findAll('path')

    # Map colors

    # colors = ["#FF0000", "#FFFFFF", "#0000FF"]

    colors = [opts['low_color'], "#FFFFFF", opts['high_color']]

    cmap = linear_gradient(start_hex = colors[0], finish_hex = colors[1], n = 51)

    cmap = cmap + linear_gradient(start_hex = colors[1], finish_hex = colors[2], n = 50)[1:]

    soup.find('stop', attrs={'id':'stop4246'})['style'] = "stop-color:" + colors[0] + ";stop-opacity:1"
    soup.find('stop', attrs={'id':'stop4244'})['style'] = "stop-color:" + colors[1] + ";stop-opacity:1"
    soup.find('stop', attrs={'id':'stop4242'})['style'] = "stop-color:" + colors[2] + ";stop-opacity:1"

    # County style
    path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1; \
    stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

    # Color the counties based on unemployment rate
    for p in paths:

        if p['id'] not in ["State_Lines", "separator"]:
            # print p['id']
            try:
                pct_var = final_var_dict[int(p['id'])]
                name = p['inkscape:label']
                p['onmouseover']="displayName(" +" \'" + name + "\'" + ");displayVar("  +" \'" + str(pct_var) + "\'" + ")"
            except:
                continue
            if np.int((pct_var - min)/(max - min)*99) < 99 and np.int((pct_var - min)/(max - min)*99) > 0:
                color_class = np.int((pct_var - min)/(max - min)*99)
            elif np.int((pct_var - min)/(max - min)*99) >= 99:
                color_class = 99
            elif np.int((pct_var - min)/(max - min)*99) <= 0:
                color_class = 0
            try:
                color = cmap[color_class]
            except:
                print "there's a problem... " + str(color_class)
            p['style'] = path_style + color

    soup.find('text', attrs={'id':'textLB'}).string = '< ' + str(int(min))
    soup.find('text', attrs={'id':'textUB'}).string = '> ' + str(int(max))

    html = soup.prettify("utf-8")
    with open(output + '.svg', "wb") as file:
        file.write(html)

    svg_file = open(output + '.svg', "r")

    with wand.image.Image() as image:
        with wand.color.Color('white') as background_color:
            library.MagickSetBackgroundColor(image.wand, 
                                             background_color.resource) 
        image.read(blob=svg_file.read())
        png_image = image.make_blob("png32")

    with open(output + '.png', "wb") as out:
        out.write(png_image)
