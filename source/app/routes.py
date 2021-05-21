from crypt import methods
from email import header
from flask import render_template
from flask import current_app as app
import json
import pandas as pd


def myround(x, base=5):
    return base * round(x/base)


with open("source/data/data_dashboard_top.json") as json_file:
    data_top = json.load(json_file)

with open("source/data/dashboard_bottom_left.json") as json_file:
    data_bottom = json.load(json_file)

    data_bottom = pd.DataFrame.from_dict(
        data_bottom, orient='index', columns=['used', 'free'])

    data_bottom['total'] = data_bottom['used'] + data_bottom['free']
    data_bottom['perc'] = (data_bottom['used'] / data_bottom['total']) * 100
    data_bottom['perc'] = data_bottom['perc'].apply(lambda x: round(x, 2))
    data_bottom['total'] = data_bottom['total']

    column_names_bottom = [x.title() for x in data_bottom.index]
    data_bottom['total'] = data_bottom['total'].astype(int)
    perc = [myround(x) for x in list(data_bottom["perc"].astype(int))]

    raw_data = [[x, y, z]
                for x, y, z in zip(data_bottom["total"], data_bottom["perc"], perc)]


@ app.route('/')
def index():
    return render_template('dashboard_template.html', availabe_mechanical=data_top["AvailableMechanical"],
                           availabe_electrical=data_top["AvailableElectric"], active_bikes=data_top["ActiveBikes"],
                           active_stations=data_top["ActiveStations"], column_names_bottom=column_names_bottom,
                           row_data=raw_data, zip=zip)
