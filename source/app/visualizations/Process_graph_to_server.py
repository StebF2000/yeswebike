#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx
import pandas as pd
from turtle import window_height
from click import style
import plotly.express as px
import pandas as pd
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from IPython.core.display import display, HTML
import plotly
import numpy as np

import psycopg2 as psy
import plotly.express as px

conn = psy.connect(
    dbname="postgres",
    user="admin",
    host="172.28.1.4",
    password="admin"
)

G = nx.readwrite.gml.read_gml('graf.gml')
estacions = pd.read_query("select * from estacions;", conn)


# In[ ]:


dic = {'id': [], 'lat': [], 'lon': [],
       'BetweennessCentrality': [], 'address': []}
data = nx.get_node_attributes(G, 'BetweennessCentrality')
for node in data:

    dic['id'].append(node)
    dic['BetweennessCentrality'].append(float(data[node]))
    row = estacions[estacions['id'] == int(node)]
    dic['address'].append(row['streetName'].iloc[0])
    dic['lat'].append(row['latitude'].iloc[0])
    dic['lon'].append(row['longitude'].iloc[0])


# In[ ]:


df = pd.DataFrame(dic)


# In[ ]:


def bare_map(server, df):

    bicing = df

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name='address', color="BetweennessCentrality", size='BetweennessCentrality', hover_data={
                            'lat': False, 'lon': False}, color_discrete_sequence=["red"], zoom=12, height=700)

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(template='plotly_white')

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


bare_map('', df).show()


# In[ ]:


df = pd.read_query('select * from Estat', conn)


# In[ ]:


df = df.values


# In[ ]:


new_row = np.asarray(
    '1,16,16,0,14,1,1,1,True,IN_SERVICE,1553795923,(1; 1553795923)'.split(','))
df = np.vstack((df, new_row))


# In[ ]:


df = pd.DataFrame(df)


# In[ ]:


idx = 'station_id    name    physical_configuration    lat    lon    altitude    address    post_code    capacity    last_updated    ttl   pk'.split(
    '   ')
df.columns = idx
