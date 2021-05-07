import py7zr
import os
for data in ['Estacions','Informacio']:
    for x in os.listdir(f'datasets/{data}'):
        archive = py7zr.SevenZipFile(f'datasets/{data}/{x}', mode='r')
        archive.extractall(path=f"datasets/{data}_csv/")
        archive.close()

