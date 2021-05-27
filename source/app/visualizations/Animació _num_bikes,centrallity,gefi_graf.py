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
import datetime
import plotly.graph_objs as go
import plotly
import numpy as np
import psycopg2 as psy
from scipy.spatial import ConvexHull

conn = psy.connect(
        dbname="postgres",
        user="admin",
        host="172.28.1.4",
        password="admin"
    )


# In[ ]:


df = pd.read_query("Select * from estacions;", conn)
df2 = pd.read_csv("Select * from estat;", conn)


# In[ ]:


df2['id'] = df2['station_id']
df2 = df2.drop('station_id', axis = 1)


# In[ ]:


var = list(df.id.unique())
df2 = df2[df2.id.isin(var)]


# In[ ]:


df = pd.merge(df2, df, on = 'id')


# In[ ]:


df = df.sort_values("last_updated")


# In[ ]:


fig = px.scatter_mapbox(df.iloc[:int(1e6)], lat="lat", lon="lon",
            animation_frame = 'last_updated',  
            color="status", size=" num_bikes_available_types.mechanical",
            color_continuous_scale=px.colors.cyclical.IceFire, 
            size_max=10, zoom=12, 
            #hover_data = ['Confirmed', 'Deaths', 'Recovery'], 
            title = 'Visualizing spread of COVID from 22/1/2020 to17/6/2020')
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()


# In[ ]:


df = df.drop('Unnamed: 0',axis=1).sort_values("last_updated")


# In[ ]:


fig = px.scatter_mapbox(df.iloc[:100], lat="lat", lon="lon",
            animation_frame = 'last_updated',  
            size=" num_bikes_available",
            color = ' num_bikes_available',
            color_continuous_scale=px.colors.carto.Burg, 
            size_max=15, zoom=12,
            #hover_data = ['Confirmed', 'Deaths', 'Recovery'], 
            title = 'Visualizing spread of COVID from 22/1/2020 to17/6/2020')

fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()


# In[ ]:


fig.write_html("animation.html")


# In[ ]:


fig = px.scatter_mapbox(df.iloc[:10000], lat="lat", lon="lon",
            animation_frame = 'last_updated',  
            size=" num_bikes_available",
            color = ' num_bikes_available',
            color_continuous_scale=px.colors.cyclical.IceFire, 
            size_max=15, zoom=12, 
            #hover_data = ['Confirmed', 'Deaths', 'Recovery'], 
            title = 'Visualizing spread of COVID from 22/1/2020 to17/6/2020')

fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()


# In[ ]:


idxs = df.groupby("last_updated").agg(a = ("id","unique"))


# In[ ]:



def smooth(x,ma):
    ones = np.ones(ma)/ma
    return np.convolve(x,ones,mode='same')

vals = [len(x) for x in idxs['a']]
mean_var = 2000
df2 = pd.DataFrame()
df2['Station Number'] = vals + [x for x in smooth(vals,mean_var)[mean_var:-mean_var]]
df2[' '] = [datetime.datetime.fromtimestamp(x) for x in idxs.index] + [datetime.datetime.fromtimestamp(x) for x in idxs.index][mean_var:-mean_var]
df2['class'] = ['Station Number Over time' for _ in range(len(vals))] +  ['Station Number Smoothed Over Time' for _ in range(len(vals)-2*mean_var)]


# In[ ]:


fig = px.line(df2,x=' ',y='Station Number',color="class",title="Network size on the last two years")
fig.write_image("fig2.svg")


# In[ ]:


data = plotly.io.to_html(fig,"NetworkSize.html")


# In[ ]:


with open("SizeNetworkPlot.html",'w') as hdlr:
    hdlr.write(data)


# In[ ]:


df2 = pd.read_query("select * from estacions", conn)


# In[ ]:


dic = {}
nodes = df2['id'].unique()
threshold = 1
vals= df2.values[:,1:3]
n = 0
k = 7
q = 0
edges = []
graf = nx.DiGraph()
for i in range(len(df2)):
        node = df2.iloc[i]['id']
        graf.add_node(node,label = df2.iloc[i]['address'] )
        val_x,val_y = vals[i]
        dist = (np.sum((vals - np.asarray([val_x,val_y]))**2,axis=1))
        idxes = np.argsort(dist)
        i = 0
        for every_option in df2['id'].values[idxes][1 : k+1 ] :
            idx = np.argmax(df2['id'] == every_option)
            node2 = every_option
            val_x,val_y = vals[idx]
            dist2 = (np.sum((vals - np.asarray([val_x,val_y]))**2,axis=1))
            idxes2 = np.argsort(dist2)
            if node in idxes2:
                if node2 not in graf.nodes(): graf.add_node(node2,label = df2.iloc[idx]['address'])
                graf.add_edge(node, node2, weight=1e-5/(dist[idxes][i+1] + 1e-5))

            i+=1 
            
        

nx.write_gexf(graf, "test.gexf")

n+=1
graf
    


# In[ ]:


G = nx.readwrite.gexf.read_gexf('graf.gexf')
nodes = G.nodes(data=True)
dic_nodes_class = {'id':[],'MClass':[],'Betweenness Centrality':[],"Eccentricity":[],"Strongly-Connected ID":[],"indegree":[],"outdegree":[]}

for x in nodes:
    dic_nodes_class['id'].append(x[0])
    bc = x[1]['Modularity Class']
    bc1 = x[1]['Betweenness Centrality']
    bc2 = x[1]['Eccentricity']
    bc3 = x[1]['Strongly-Connected ID']
    bc4 = x[1]['Grado de entrada']
    bc5 = x[1]['Grado de salida']
    dic_nodes_class['MClass'].append(x[1]['Modularity Class'])
    dic_nodes_class['Betweenness Centrality'].append(x[1]['Betweenness Centrality'])
    dic_nodes_class['Eccentricity'].append(x[1]['Eccentricity'])
    dic_nodes_class['Strongly-Connected ID'].append(x[1]['Strongly-Connected ID'])
    dic_nodes_class['indegree'].append( x[1]['Grado de entrada'])
    dic_nodes_class['outdegree'].append(x[1]['Grado de salida'])

df3 = pd.DataFrame(dic_nodes_class)


# In[ ]:


df.id = [str(x) for x in df.id]
df = df.merge(df3,on='id',how='left')


# In[ ]:


df = df.groupby(by=["MClass","last_updated"]).agg(
                            mean_bikes_available = (" num_bikes_available", np.mean),
                            max_bikes_available = (" num_bikes_available", "max"),
                            min_bikes_available = (" num_bikes_available", "min"),
                            sum_bikes_available = (" num_bikes_available", "sum"),

                            mean_num_bikes_available_types_mechanical = (" num_bikes_available_types.mechanical", np.mean),
                            max_num_bikes_available_types_mechanical = (" num_bikes_available_types.mechanical", "max"),
                            min_num_bikes_available_types_mechanical = (" num_bikes_available_types.mechanical", "min"),                                      
                            sum_num_bikes_available_types_mechanical = (" num_bikes_available_types.mechanical", "sum"),  
                            
                            mean_num_bikes_available_types_ebike	 = (" num_bikes_available_types.ebike", np.mean),
                            max_num_bikes_available_types_ebike	 = (" num_bikes_available_types.ebike", "max"),
                            min_num_bikes_available_types_ebike	 = (" num_bikes_available_types.ebike", "min"),
                            sum_num_bikes_available_types_ebike	 = (" num_bikes_available_types.ebike", "sum"),

                            mean_num_docks_available = (" num_docks_available ", np.mean),
                            max_num_docks_available = (" num_docks_available ", np.max),
                            min_num_docks_available = (" num_docks_available ", np.min),
                            sum_num_docks_available = (" num_docks_available ", np.sum),                                                                                                   
                            mean_BetweennessCentrality = ("Betweenness Centrality", np.mean),
                            max_BetweennessCentrality = ("Betweenness Centrality", np.max),
                            min_BetweennessCentrality = ("Betweenness Centrality", np.min),
                            
                            mean_Eccentricity = ("Eccentricity", np.mean),
                            max_Eccentricity = ("Eccentricity", np.max),
                            min_Eccentricity = ("Eccentricity", np.min),
                            )


# In[ ]:


res = []
names = ['Dreta de l eixample' , 'Sagrada Familia' , 'Sant Pere', 'La Barceloneta', 'Vila Olímpica','El Raval','Sant Antoni',
          'Universitat' , 'Esquerra de l eixample', "Les corts" ,"Glories", "El besoós i maresme","La marina","Sant Andreu",
          'Horta', 'Bonanova']
for x in df.index:
    if x[0] < len(names):
        res.append(names[x[0]])
    else:
        res.append(str(x[0]))


# In[ ]:


df['class'] = res
df[' '] = [datetime.datetime.fromtimestamp(x[1]) for x in df.index]


# In[ ]:



from PIL import Image
fig2 = px.line(df,x=' ',y="mean_bikes_available",color='class', title="Mean of available bikes through time per class")
x1 = datetime.datetime(year=2020,day=17,month=3)
x2 = datetime.datetime(year=2020,day=22,month=4)
fig = (go.Scatter(x=[x1,x1,x2,x2], y=[0,200,200,0],name="COVID-19",fillcolor='red',line_color='red',fill='toself',opacity=0.1))
fig2.add_trace(fig)
fig2.write_image("fig1.svg")
fig2.write_html("fig1.html")


# In[ ]:


x1 = datetime.datetime(year=2020,day=17,month=3)
x2 = datetime.datetime(year=2020,day=22,month=4)
fig2 = go.Figure((go.Scatter(x=[x1,x1,x2,x2], y=[0,200,200,0], fill="toself",opacity=0.1)))
fig2


# In[ ]:


df4.id = [str(x) for x in df4.id]
df5 = df3.merge(df4,on='id')
df5 = df5.sort_values('MClass')
df5.shape


# In[ ]:


hulls = []
points_ = []
others = []
for class_ in df5.MClass.unique():
    values = df5[df5.MClass == class_]
    points = values[['lat','lon']].values
    if points.shape[0]>=3:
        points_.append(points)
        hulls.append(ConvexHull(points))
    else:
        others.append(points.flatten())


# In[ ]:


centers = []
for hull in hulls:
     cx = np.mean(hull.points[hull.vertices,0])
     cy = np.mean(hull.points[hull.vertices,1])
     centers.append((cx,cy))


# In[ ]:


import plotly.graph_objects as go
fig = go.Figure(go.Scattermapbox(
        lat=['38.91427','38.91538','38.91458',
             '38.92239','38.93222','38.90842',
             '38.91931','38.93260','38.91368',
             '38.88516','38.921894','38.93206',
             '38.91275'],
        lon=['-77.02827','-77.02013','-77.03155',
             '-77.04227','-77.02854','-77.02419',
             '-77.02518','-77.03304','-77.04509',
             '-76.99656','-77.042438','-77.02821',
             '-77.01239'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=["The coffee bar","Bistro Bohem","Black Cat",
             "Snap","Columbia Heights Coffee","Azi's Cafe",
             "Blind Dog Cafe","Le Caprice","Filter",
             "Peregrine","Tryst","The Coupe",
             "Big Bear Cafe"],
    ))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        bearing=0,
        center=dict(
            lat=38.92,
            lon=-77.07
        ),
        pitch=0,
        zoom=10
    ),
)

fig.show()


# In[ ]:


lat,lon = points_[0][hulls[0].vertices,0], points_[0][hulls[0].vertices,1]

fig = go.Figure([go.Scattermapbox(
        lat=points_[i][hulls[i].vertices,0],
        lon= points_[i][hulls[i].vertices,1],
        mode='markers',marker=go.scattermapbox.Marker(size=3)
        ,fill="toself",hovertext='District: '+names[i] , name = names[i])
         for i in range(len(points_))] +

          [go.Scattermapbox(
        lat=[others[i][0]],
        lon=[others[i][1]],
        mode='markers',marker=go.scattermapbox.Marker(size=10)
        ,hovertext=str(i))
         for i in range(len( others ) ) ] +

         [go.Scattermapbox(
        lat=[x[0] for x in centers],
        lon=[x[1] for x in centers], 
        name='',
        mode='text',text=['Class: '+str(x) for x in range(len(centers))],texttemplate = '% {text: .10s} ' ,  textposition = 'top right',
                        textfont=dict(size=16, color='black')
        ,hovertext=['District: '+names[x] for x in range(len(centers))] ) ])

fig.update_layout(mapbox_style="carto-positron",)
fig.update_mapboxes( center_lon =2.1706023 ,center_lat=41.3949085,zoom=11)
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},showlegend=False)
fig.write_html('fig3.html')


# In[ ]:


go.Figure([go.Scattermapbox(
        lat=[centers[0][0]],
        lon=[centers[0][1]], 
        name='',
        mode='text',text=['Class: '+str(0)],textposition='top right', textfont=dict(size=16, color='black') ,hovertext=str(0) ) ])

