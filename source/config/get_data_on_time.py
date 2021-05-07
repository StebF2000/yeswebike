import urllib.request, json 
import multiprocessing
import time



class GetData:

	def __init__(self,time_waiting):

		self.estat_url ="https://opendata-ajuntament.barcelona.cat/data/dataset/6aa3416d-ce1a-494d-861b-7bd07f069600/resource/b20e711d-c3bf-4fe5-9cde-4de94c5f588f/download"
		self.info_url =  "https://opendata-ajuntament.barcelona.cat/data/dataset/bd2462df-6e1e-4e37-8205-a4b8e7313b84/resource/e5adca8d-98bf-42c3-9b9c-364ef0a80494/download"


	def get_data1(self):
		start = time.time()
		with urllib.request.urlopen("https://opendata-ajuntament.barcelona.cat/data/dataset/6aa3416d-ce1a-494d-861b-7bd07f069600/resource/b20e711d-c3bf-4fe5-9cde-4de94c5f588f/download") as url:
			data = json.loads(url.read().decode())

		with open('station_status.json','w') as hdlr:
			json.dump(data,hdlr)


	def get_data2(self):
		with urllib.request.urlopen("https://opendata-ajuntament.barcelona.cat/data/dataset/bd2462df-6e1e-4e37-8205-a4b8e7313b84/resource/e5adca8d-98bf-42c3-9b9c-364ef0a80494/download") as url:
			data2 = json.loads(url.read().decode())

		with open('station_information.json','w') as hdlr:
			json.dump(data2,hdlr)


	def get_data_background(self):

		p1 = multiprocessing.Process(target= self.get_data1)
		p2 = multiprocessing.Process(target=self.get_data2)
		p1.start()
		p2.start()
		print(f"Processes had started")

	def get_all_data(self):
		p1 = multiprocessing.Process(target=self.get_data_background)
		p1.start()

if __name__ == '__main__':

	getter = GetData(0)
	getter.get_all_data()
	print(f"Wrokflows continues")
