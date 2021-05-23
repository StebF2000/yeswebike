import plotly.express as px
import pandas as pd
import json

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc


def bare_map(server):

    with open("source/app/data/station_information.json") as json_file:
        data = json.load(json_file)

        bicing = pd.DataFrame(data["data"]["stations"])

    fig = px.scatter_mapbox(bicing, lat="lat", lon="lon", hover_name='address', hover_data={
                            'lat': False, 'lon': False, 'capacity': True, 'altitude': False}, zoom=11.5,
                            height=700, color_discrete_sequence=['#a64ca0'], opacity=0.9)

    fig.update_layout(mapbox_style="carto-positron")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    dash_app = Dash(server=server, routes_pathname_prefix="/dashapp/")

    dash_app.layout = html.Div(
        id='dash-container', children=[dcc.Graph(figure=fig)])

    return dash_app.server
