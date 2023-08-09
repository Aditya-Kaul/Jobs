import requests
from data_input import data_inp

URL='http://127.0.0.1:5000/predict'

headers = {"Content-Type": "application/json"}
data = {"input": data_inp }

r = requests.get(URL,headers=headers,json=data)

r.json()