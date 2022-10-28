import csv
import pandas as pd
import requests as rq
from freedictionaryapi.clients.sync_client import DictionaryApiClient
from freedictionaryapi.errors import DictionaryApiError

API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
FP = 'Gregmat-Vocab-Grouped.csv'
DOWNLOAD = './audio_files'


def APIrequest(word):
    client = DictionaryApiClient()
    try:
        parser = client.fetch_parser(word)
    except DictionaryApiError:
        print('API error')
    client.close()

dataframe = pd.read_csv(FP)
print(dataframe.dtypes)

APIrequest('blithe')
