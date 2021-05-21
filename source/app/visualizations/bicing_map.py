from turtle import window_height
from click import style
import plotly.express as px
import pandas as pd

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc


def bare_map(server):

    bicing = pd.read_csv("data/estacions_bicing.csv")

    fig = px.scatter_mapbox(bicing, lat="latitude", lon="longitude", hover_name='streetName', hover_data={
                            'latitude': False, 'longitude': False}, color_discrete_sequence=["red"], zoom=12,
                            height=700)

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(template='plotly_white')

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    dash_app = Dash(server=server, routes_pathname_prefix="/dashapp/")

    dash_app.layout = html.Div(
        id='dash-container', children=[dcc.Graph(figure=fig)])

    return dash_app.server
