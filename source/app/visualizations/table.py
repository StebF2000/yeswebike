import dash
import dash_table
import pandas as pd


def dash_t(server):

    df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

    app = dash.Dash(server=server, routes_pathname_prefix="/dashapp/tables/", external_stylesheets=[
        '/static/css/soft-ui-dashboard.css'
    ])

    app.layout = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )

    return app.server
