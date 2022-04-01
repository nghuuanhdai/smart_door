import requests
from datetime import datetime
import ast

def getFeedData():
    url = r'https://io.adafruit.com/api/v2/khanhhungvu1508/feeds/numpeople-doormonitor/data?start_time=2022-03-29T00:00:00Z'
    cont = requests.get(url)
    ret = cont.content.decode()
    ret = ast.literal_eval(ret)
    value = list()
    time = list()
    for data in ret:
        con_time = data["created_at"]
        con_time = datetime.strptime(con_time, '%Y-%m-%dT%H:%M:%SZ')
        value += [int(data["value"])]
        time += [str(con_time)]
    return time[::-1], value[::-1]