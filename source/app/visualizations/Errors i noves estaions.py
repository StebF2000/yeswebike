#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
import numpy as np
import os
from datetime import datetime
import psycopg2 as psy
import plotly.express as px
conn = psy.connect(
    dbname="postgres",
    user="admin",
    host="172.28.1.4",
    password="admin"
)


# In[ ]:


Estacions = pd.read_query("Select * from estacions;", conn)
Estat = pd.read_query("Select * from estat;", conn)
Informacio = pd.read_query("Select * from informacio", conn)


# In[ ]:


Errors = Estat[(Estat["is_installed"] == 1) & (
    (Estat["is_renting"] == 0) | (Estat["is_returning"] == 0))]


# In[ ]:


Errors = (Errors[Errors["status"] == "MAINTENANCE"])


# In[ ]:


Errors["id"] = Errors["station_id"]
Errors = Errors.drop("station_id", axis=1)


# In[ ]:


grouped = Errors.groupby('id', as_index=False).count()[['id', 'is_renting']]


# In[ ]:


Estacions_c = Estacions[Estacions["id"].isin(list(map(str, Errors["id"])))]


# In[ ]:


Estacions_c["id"] = list(map(int, Estacions_c["id"]))


# In[ ]:


Stations_all = Estacions_c.merge(grouped, on="id")


# In[ ]:


fig = px.scatter_mapbox(Stations_all[Stations_all.is_renting < 1000], lat="latitud", lon="longitud", color_continuous_scale=px.colors.cyclical.IceFire, color='is_renting', size_max=10, zoom=10, hover_name='carrer', hover_data={
    'latitud': False, 'longitud': False})
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()


# In[ ]:


Informacio = pd.read_csv('data/Informacio.csv')


# In[ ]:


Info = Estat.groupby('station_id').agg(date=('last_updated', 'min'))


# In[ ]:


Info['id'] = list(Info.index)
date = list(map(datetime.fromtimestamp, Info['date']))
Info['date'] = date
Info['year'] = [str(x.year) for x in date]


# In[ ]:


Info = Info[Info.id.isin(Estacions.id)]


# In[ ]:


Info = Info.merge(Estacions, on='id')


# In[ ]:


Info.year.unique()


# In[ ]:


np.random.seed(1)
fig = px.scatter_mapbox(Info, lat="latitud", lon="longitud", color='year', size_max=10, hover_name='carrer', hover_data={
    'latitud': False, 'longitud': False}, zoom=12, height=700, color_discrete_sequence=np.random.choice(px.colors.carto.Bold, 3))
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()


# In[ ]:
