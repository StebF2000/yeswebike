#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from turtle import window_height
from click import style
import plotly.express as px
import pandas as pd
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from IPython.core.display import display, HTML
import plotly
import networkx as nx
import pandas as pd
import psycopg2 as psy

conn = psy.connect(
        dbname="postgres",
        user="admin",
        host="172.28.1.4",
        password="admin"
    )

df = pd.read_query('select * from estat', conn)
fig = px.scatter_mapbox(df.iloc[:int(1e3)], lat="lat", lon="lon",
            animation_frame = 'last_updated',  
            color="status", size=" num_bikes_available_types.mechanical",
            color_continuous_scale=px.colors.cyclical.IceFire, 
            size_max=10, zoom=12, 
            title = 'Visualizing spread of COVID from 22/1/2020 to17/6/2020')
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
data_canada = px.data.gapminder().query("country == 'Canada'")
fig2= px.bar(data_canada, x='year', y='pop')

fig.add_trace(fig2)

fig.show()


# In[ ]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PolyCollection
import numpy as np

map = Basemap(llcrnrlon=-20,llcrnrlat=0,urcrnrlon=15,urcrnrlat=50,)

fig = plt.figure()
ax = Axes3D(fig)

ax.set_axis_off()
ax.azim = 270
ax.dist = 7

polys = []
for polygon in map.landpolygons:
    polys.append(polygon.get_coords())


lc = PolyCollection(polys, edgecolor='black',
                    facecolor='#DDDDDD', closed=False)

ax.add_collection3d(lc)
ax.add_collection3d(map.drawcoastlines(linewidth=0.25))
ax.add_collection3d(map.drawcountries(linewidth=0.35))

lons = np.array([-13.7, -10.8, -13.2, -96.8, -7.99, 7.5, -17.3, -3.7])
lats = np.array([9.6, 6.3, 8.5, 32.7, 12.5, 8.9, 14.7, 40.39])
cases = np.array([1971, 7069, 6073, 4, 6, 20, 1, 1])
deaths = np.array([1192, 2964, 1250, 1, 5, 8, 0, 0])
places = np.array(['Guinea', 'Liberia', 'Sierra Leone','United States', 'Mali', 'Nigeria', 'Senegal', 'Spain'])

x, y = map(lons, lats)

ax.bar3d(x, y, np.zeros(len(x)), 2, 2, deaths, color= 'r', alpha=0.8)

plt.show()


# In[ ]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PolyCollection
import numpy as np

map = Basemap(llcrnrlon=-20,llcrnrlat=0,urcrnrlon=15,urcrnrlat=50,)

fig = plt.figure()
ax = Axes3D(fig)

ax.set_axis_off()
ax.azim = 270
ax.dist = 7

polys = []
for polygon in map.landpolygons:
    polys.append(polygon.get_coords())


lc = PolyCollection(polys, edgecolor='black',
                    facecolor='#DDDDDD', closed=False)

ax.add_collection3d(lc)
ax.add_collection3d(map.drawcoastlines(linewidth=0.25))
ax.add_collection3d(map.drawcountries(linewidth=0.35))

lons = np.array([-13.7, -10.8, -13.2, -96.8, -7.99, 7.5, -17.3, -3.7])
lats = np.array([9.6, 6.3, 8.5, 32.7, 12.5, 8.9, 14.7, 40.39])
cases = np.array([1971, 7069, 6073, 4, 6, 20, 1, 1])
deaths = np.array([1192, 2964, 1250, 1, 5, 8, 0, 0])
places = np.array(['Guinea', 'Liberia', 'Sierra Leone','United States', 'Mali', 'Nigeria', 'Senegal', 'Spain'])

x, y = map(lons, lats)

ax.bar3d(x, y, np.zeros(len(x)), 2, 2, deaths, color= 'r', alpha=0.8)

plt.show()


# In[ ]:


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from numpy import array
from numpy import max


map = Basemap(llcrnrlon=-0.5,llcrnrlat=39.8,urcrnrlon=4.,urcrnrlat=43.,
             resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = 1)


map.readshapefile('../sample_files/lightnings', 'lightnings')

x = []
y = []
c = []

for info, lightning in zip(map.lightnings_info, map.lightnings):
    x.append(lightning[0])
    y.append(lightning[1])
    
    if float(info['amplitude']) < 0:
        c.append(-1 * float(info['amplitude']))
    else:
        c.append(float(info['amplitude']))
    
plt.figure(0)

map.drawcoastlines()
map.readshapefile('../sample_files/comarques', 'comarques')

map.hexbin(array(x), array(y))

map.colorbar(location='bottom')



plt.figure(1)

map.drawcoastlines()
map.readshapefile('../sample_files/comarques', 'comarques')

map.hexbin(array(x), array(y), gridsize=20, mincnt=1, cmap='summer', bins='log')

map.colorbar(location='bottom', format='%.1f', label='log(# lightnings)')



plt.figure(2)

map.drawcoastlines()
map.readshapefile('../sample_files/comarques', 'comarques')

map.hexbin(array(x), array(y), gridsize=20, mincnt=1, cmap='summer', norm=colors.LogNorm())

cb = map.colorbar(location='bottom', format='%d', label='# lightnings')

cb.set_ticks([1, 5, 10, 15, 20, 25, 30])
cb.set_ticklabels([1, 5, 10, 15, 20, 25, 30])




plt.figure(3)

map.drawcoastlines()
map.readshapefile('../sample_files/comarques', 'comarques')

map.hexbin(array(x), array(y), C = array(c), reduce_C_function = max, gridsize=20, mincnt=1, cmap='YlOrBr', linewidths=0.5, edgecolors='k')

map.colorbar(location='bottom', label='Mean amplitude (kA)')


plt.show()

