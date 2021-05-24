import plotly.express as px
import pandas as pd
import json

from dash import Dash
import dash_html_components as html
import dash_core_components as dcc

from psycopg2 import connect
import pandas.io.sql as sqlio


def read_db(query):
    conn = connect(
        dbname="postgres",
        user="admin",
        host="172.28.1.4",
        password="admin"
    )

    return sqlio.read_sql_query(query, conn)


def bare_map(server):

    bicing = read_db("SELECT * FROM estacions")

    fig = px.scatter_mapbox(bicing, lat="latitud", lon="longitud", hover_name='carrer', hover_data={
                            'latitud': False, 'longitud': False}, zoom=11.5,
                            height=700, color_discrete_sequence=['#a64ca0'], opacity=0.9)

    fig.update_layout(mapbox_style="carto-positron")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    dash_app = Dash(server=server, routes_pathname_prefix="/dashapp/")

    dash_app.layout = html.Div(
        id='dash-container', children=[dcc.Graph(figure=fig)])

    return dash_app.server
