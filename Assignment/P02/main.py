###############################################################################
#author: Prakash Tamang
#Instructor: Prof. Griffin
#Class: CMPS 4553 Spatial DS 
#
#function: to load both data files into a geopandas geoseries spatial index.
#          to calculate the distance from each city to every other city and
#          to store those values in either a csv or json file for use at a later
#          time.to determine a metric or threshold to "assign" a UFO sighting
#          to a particular city. Maybe average the distance to the 100 closest
#          UFO's as a start.                                     
#                                                               
###############################################################################

import pandas as pd
import json
import random as rand
from math import acos
import numpy as np
import math

# first read and print out ufo sighting 
df1 = pd.read_csv('Assignments/P02/ufo_data.csv')
print(df1.head(20))

df2= pd.read_csv('Assignments/P02/StateCapitals.csv')
print(df2.head(10))
print(df2['state'])

#bounding box for the united states
#north
top = 49.3457868
#west
leftborder = -124.7844079
#east
rightborder = -66.9513812
#south
bottom =  24.7433195

# drop uneccesary of the left bounding box border of us both past or before 
# based on the top and bottom vals
df3 = df3.drop(df3[(df3['lon'] <= leftborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] <= leftborder) & (df3['lat'] >= top)].index)
df3 = df3.drop(df3[(df3['lon'] >= leftborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] >= leftborder) & (df3['lat'] >= top)].index)

# drop uneccesary of the right bounding box border of us both past or before 
# based on the top and bottom vals
df3 = df3.drop(df3[(df3['lon'] >= rightborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] >= rightborder) & (df3['lat'] >= top)].index)
df3 = df3.drop(df3[(df3['lon'] <= rightborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] <= rightborder) & (df3['lat'] >= top)].index)

# there is one outlier that didnt get removed so look at the outlier
# lat and long and hard code in to remove it(over in europe)
df3 = df3.drop(df3[(df3['lon'] == -8.5962) & (df3['lat'] == 42.3358)].index)

# want to test the number of occurances in each state
print("The number of occurances in each state are :\n")
print(df3['state']. value_counts())
# number of occurances in city data
print("The number of occurances in each city  are :\n")
print(df3['city']. value_counts()) 

df3['lat'] = df3['lat'].astype(float)
df3['lon'] = df3['lon'].astype(float)
df3['state'] = df3['state'].str.title()
df3['city'] = df3['city'].str.title()


def df_to_geojson(df3, properties, lat='lat', lon='lon'):
    geojson = {'type':'FeatureCollection', 'features':[]}

    for _, row in df3.iterrows():
        
        # random rgb color between 0 and 255
        Red = lambda: rand.randint(0,255)
        Green = lambda: rand.randint(0,255)
        Blue = lambda: rand.randint(0,255)
        ColorGeneration= f'#%02X%02X%02X' % (Red(),Blue(),Green())
        featured = {'type':'Feature',
                   "properties":
                   {
                    "marker-color": ColorGeneration,
                    "city": row['city'],
                    "state" : row['state'],
                    "longitude": row['lon'],
                    "latitude": row['lat']
                    },     
                    # points for geometry   
                   'geometry':{'type':'Point',
                               'coordinates':[row['lon'],row['lat']]
                              }
                    }
        geojson['features'].append(featured)
    #to return geojson
    return geojson

cols = ['state', 'city', 'lat', 'lon']
geojson = df_to_geojson(df3, cols)
print(geojson)
try:
    with open('Assignments/P02/output.geojson', 'w') as file:
        file.write(json.dumps(geojson, indent=4))
