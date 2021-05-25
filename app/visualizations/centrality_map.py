import plotly.express as px
import pandas as pd
import json

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc


def centrality_map(server):

    data = pd.read_csv("app/data/centrality_bicing.csv")

    fig = px.scatter_mapbox(data, lat="lat", lon="lon", hover_name='address', color="Betweenness Centrality",
                            size='Betweenness Centrality', hover_data={'lat': False, 'lon': False, 'Betweenness Centrality': False},
                            color_continuous_scale=px.colors.carto.Burg, zoom=12, height=700, opacity=0.9)

    fig.update_layout(mapbox_style="carto-positron")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    dash_app = Dash(server=server, routes_pathname_prefix="/centralityMap/")

    dash_app.layout = html.Div(
        id='centrality', children=[dcc.Graph(figure=fig)])

    return dash_app.server
