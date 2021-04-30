#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:48:29 2021

@author: MAAT
"""

import dash  # Dash 1.16 or higher
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from numpy import arange

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("yelp.csv")


app.layout = html.Div([
    html.H2("Find your ideal restaurants in Massachusetts ", style = {"textAlign" : "center"}),
    html.Label("What is this dashboard about?",
               style = {"fontSize" : 20, "textAlign" : "left"}),
    html.P("This dashboard summarizes the information of over one thousand restaurants in MA from Yelp. It allows an user to find the restaurant basded on the following three search criteria:"),
    html.P(" 1. Category - a list of all avalibale categories, such as Chinese food', 'Japanese food', etc"),
    html.P(" 2. Price - price per person"),
    html.P("   -   $ = inexpensive, usually $10 and under;"),
    html.P("   -   $$ = Moderately expensive, usually between $10 - $25;"),
    html.P("   -   $$$ = Expensive, usually between $25 - $45;"),
    html.P("   -   $$$$ = Very Expensive, usually $50 and up."),
    html.P(" 3. Rating - an online review site in which customers shared their experiences in that restaurant "),
    html.Label("Category: ", 
               style={'fontSize':16, 'textAlign':'left'}),
    dcc.Dropdown(
        id='cate-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(df.CATEGORY.unique())],
        value=["Chinese"],
        multi = True
    ),
    
    html.Label("Price: ", style={'fontSize':16, 'textAlign':'left'}),
    dcc.Dropdown(
        id = "price-dpdn",
        options=[{'label': s, 'value': s} for s in ["$","$$","$$$","$$$$"]],
        value = ["$", "$$"],
        multi = True
    ),
        
    html.Div([
    html.Label("Rating: ", style={'fontSize':16, 'textAlign':'left'}),
    dcc.RangeSlider(
        min = 2, 
        max = 6, 
        step = 0.5, 
        value = [3,5], 
        id = "RatingSlider", 
        marks = {i:str(i) for i in [3, 3.5, 4, 4.5, 5]},
        ),
    ],style = {"width" : "70%", "textAlign": "left"}),
    
    html.Label("Restaurants Table!",
               style = {'fontSize' : 20, "textAlign" : "left"}),
    html.Div([
    dash_table.DataTable(
        id='datatable_id',
        data=df.to_dict('records'),
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
        ],
 
        page_size = 15,
        page_action = "native",
        row_deletable = True,
        
        # filter_action = "custom",
        sort_action = "native",
        sort_mode = "single",
        ),
    
    ], className='row'),
    
    html.Label("Just go there !",
               style = {'fontSize' : 20, "textAlign" : "left"}),
    html.Div([
        dcc.Graph(id = "graph"),
    ], className = "row")
])

@app.callback(
    [Output('datatable_id', "data"),
    Output("graph", "figure")],
    [Input('RatingSlider', "value"),
    Input("price-dpdn", "value"),
    Input("cate-dpdn", "value")]
    )

def update_table(ratings, prices, categories):
    ratingCond = [n in arange(ratings[0],ratings[1]+0.5,0.5) for n in df.RATING]
    data2 = df[ratingCond]
    # data2 = data2[(data2.CITY.isin(cities)) & (data2.PRICE.isin(prices)) 
    #               & (data2.CATEGORY.isin(categories))]
    data2 = data2[(data2.PRICE.isin(prices)) & (data2.CATEGORY.isin(categories))]
    # data2 = df[(df.CITY==city) & (df.PRICE.isin(prices))].to_dict('records')
    # data2 = data2[data2.PRICE.isin(prices)].to_dict('records')
    
    y = data2
    y["count"] = 1
    y = data2.groupby(["CITY"], as_index = False)["count"].sum()
    fig = px.bar(y, x = "CITY", y = "count", color = "CITY")
    
    data2 = data2.to_dict("record")
    return data2, fig

server = app.server


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
