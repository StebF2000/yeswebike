import urllib.request
import json
import multiprocessing
import time
import datetime


class GetData:

    def __init__(self, time_waiting):

        self.estat_url = "https://opendata-ajuntament.barcelona.cat/data/dataset/6aa3416d-ce1a-494d-861b-7bd07f069600/resource/b20e711d-c3bf-4fe5-9cde-4de94c5f588f/download"
        self.info_url = "https://opendata-ajuntament.barcelona.cat/data/dataset/bd2462df-6e1e-4e37-8205-a4b8e7313b84/resource/e5adca8d-98bf-42c3-9b9c-364ef0a80494/download"
        self.data1 = []
        self.data2 = {}

    def get_data1(self):
        start = time.time()
        with urllib.request.urlopen(self.estat_url) as url:
            data = json.loads(url.read().decode())

        dic = {'AvailableMechanical': 0, 'AvailableElectric': 0,
               "ActiveBikes": 0, 'ActiveStations': 0}

        stations = []
        for station in data['data']['stations']:
            dic['AvailableMechanical'] += station['num_bikes_available_types']['mechanical']
            dic['AvailableElectric'] += station['num_bikes_available_types']['ebike']
            dic['ActiveBikes'] += station['num_docks_available']
            dic['ActiveStations'] += 1 if station['status'] == 'IN_SERVICE' else 0
            stations.append(
                (station['station_id'], station['num_docks_available'], station['num_bikes_available']))

        with open("app/data/dashboard_top.json", 'w') as hdlr:
            json.dump(dic, hdlr)

        self.data1 = stations

        with open('app/data/station_status.json', 'w') as hdlr:
            json.dump(data, hdlr)

    def get_data2(self):
        with urllib.request.urlopen(self.info_url) as url:
            data2 = json.loads(url.read().decode())

        self.data2 = {x['station_id']: x['address']
                      for x in data2['data']['stations']}

        with open('app/data/station_information.json', 'w') as hdlr:
            json.dump(data2, hdlr)

    def get_data3(self, number_items=10):

        self.data1 = sorted(self.data1, key=lambda x: x[1], reverse=True)[
            :number_items]

        res = [(self.data2[x[0]], x[1], x[2]) for x in self.data1]
        res = {x[0]: (x[1], x[2]) for x in res}

        labels = sorted(
            res, key=lambda x: res[x][0]/(res[x][0]+res[x][1]))[::-1]

        res = {x: res[x] for x in labels}

        with open('app/data/dashboard_bottom.json', 'w') as hdlr:
            json.dump(res, hdlr)

    def get_data_background(self):

        self.get_data1()
        self.get_data2()
        self.get_data3()

    def get_all_data(self):
        self.get_data_background()


if __name__ == '__main__':

    while True:

        getter = GetData(0)
        getter.get_all_data()

        print(f"Fetched {datetime.datetime.now()}")

        time.sleep(300)
