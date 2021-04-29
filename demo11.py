#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 13:36:13 2021

@author: MAAT
"""

import requests
import json
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from _ast import If

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Data from U.S. Congress, Joint Economic Committee, Social Capital Project. https://www.jec.senate.gov/public/index.cfm/republicans/2018/4/the-geography-of-social-capital-in-america
api_key = "0XQf--f7nCqD5kYbCXsLaAPOCro2yNKCW5Gy4s5T_QE9dZpZTjEOwEA_KweAmKjIU9MKCmZ0QInVR5ZoxvuPc3cesNxHQiZHFuuesooHASezxNESH7OF_GOQkQfRX3Yx"
headers = {'Authorization' : 'Bearer %s' % api_key}
 
total_amount = 20
 
URL = "https://api.yelp.com/v3/businesses/search"
params = {'location' : 'Boston', 'limit' : 50}

output = []


for i in range(total_amount):
    params['offset'] = i * 50
    req = requests.get(URL, params=params, headers=headers)
    output = output + (json.loads(req.text)['businesses'])


with open('data.json','w') as f:
    json.dump(output, f, indent =4)


data =  pd.read_json('data.json')
data = data[data.is_closed == False] 
cleandata = pd.DataFrame()
cleandata['NAME'] = data['name']

category =[]
street=[]
city=[]
for i in range(len(cleandata)):
    category.append(data['categories'][i][0]['title'])
    street.append(data['location'][i]['address1'])
    city.append(data['location'][i]['city'])


cleandata['CATEGORY'] = category
cleandata['RATING'] = data['rating'].apply(str)
cleandata['PRICE'] = data['price']
cleandata["REVIEW"] = data["review_count"]
cleandata['STREET'] = street
cleandata['CITY'] = city
cleandata["PHONE"] = [str(n[2:]) for n in data.phone]


df = cleandata

df.to_csv("yelp.csv", index = False)

