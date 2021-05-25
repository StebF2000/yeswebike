from crypt import methods
from email import header
import flask
from flask import render_template
from flask import current_app as app
import json
import pandas as pd
import os


def myround(x, base=5):
    return base * round(x/base)


@ app.route('/')
def index():

    with open("app/data/dashboard_top.json") as json_file:
        data_top = json.load(json_file)

    with open("app/data/dashboard_bottom.json") as json_file:
        data_bottom = json.load(json_file)

        data_bottom = pd.DataFrame.from_dict(
            data_bottom, orient='index', columns=['used', 'free'])

        data_bottom['total'] = data_bottom['used'] + data_bottom['free']
        data_bottom['perc'] = (data_bottom['used'] /
                               data_bottom['total']) * 100
        data_bottom['perc'] = data_bottom['perc'].apply(lambda x: round(x, 2))
        data_bottom['total'] = data_bottom['total']

        column_names_bottom = [x.title() for x in data_bottom.index]
        data_bottom['total'] = data_bottom['total'].astype(int)
        perc = [myround(x) for x in list(data_bottom["perc"].astype(int))]

        raw_data = [[x, y, z, a]
                    for x, y, z, a in zip(data_bottom["total"], data_bottom["perc"], perc, data_bottom["free"])]

        print()

    return render_template('home.html', availabe_mechanical=data_top["AvailableMechanical"],
                           availabe_electrical=data_top["AvailableElectric"], active_bikes=data_top["ActiveBikes"],
                           active_stations=data_top["ActiveStations"], column_names_bottom=column_names_bottom,
                           row_data=raw_data, zip=zip)


@app.route('/maps')
def centrality():
    with open("app/data/dashboard_top.json") as json_file:
        data_top = json.load(json_file)

    return render_template('centrality.html', availabe_mechanical=data_top["AvailableMechanical"],
                           availabe_electrical=data_top["AvailableElectric"], active_bikes=data_top["ActiveBikes"],
                           active_stations=data_top["ActiveStations"],
                           zip=zip)


@app.route('/animation')
def evolution():
    return render_template('animation.html')


@app.route('/bikesClass')
def bikes():
    return render_template('bikes_per_class.html')


@app.route('/size')
def net_size():
    return render_template('netSize.html')


@app.route('/graph', methods=["GET", "POST"])
def vizCool():
    return app.send_static_file("index.html")


@app.route('/plots')
def lines():
    with open("app/data/dashboard_top.json") as json_file:
        data_top = json.load(json_file)

    return render_template('lines.html', availabe_mechanical=data_top["AvailableMechanical"],
                           availabe_electrical=data_top["AvailableElectric"], active_bikes=data_top["ActiveBikes"],
                           active_stations=data_top["ActiveStations"],
                           zip=zip)
