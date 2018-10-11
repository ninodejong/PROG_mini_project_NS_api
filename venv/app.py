import requests
import xml.etree.ElementTree as ET
import time
from flask import Flask
app = Flask(__name__)

def api(station):
    url = 'https://webservices.ns.nl/ns-api-avt?station='+station
    username = 'ninodejong@gmail.com'
    password = 'zAXbd8mqx6bgNtNKVasUxd_Pn8bKKb3SQVS-wOY365uGYhVk4t1F7w'
    auth_values = (username, password)

    response = requests.get(url, auth=auth_values)
    schedule = ET.fromstring(response.content)

    return schedule

@app.route('/')
def nstijden():
    retar = []
    station = 'Utrecht Centraal'
    # tut https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Create-your-first-GUI-application     https://www.tutorialspoint.com/python/tk_text.htm
    schedule = api(station)
    # print("Vertrek tijden: "+station)
    for train in schedule:
        carrier = train.find('Vervoerder').text
        trainType = train.find('TreinSoort').text
        dep_time = train.find('VertrekTijd').text.split('T')
        timed = str(dep_time[0] + " " + dep_time[1]).split('+')
        to = train.find('EindBestemming').text
        rideID = train.find('RitNummer').text
        platform = train.find('VertrekSpoor').text

        platformChange = train.find('VertrekSpoor').attrib
        departure = str(time.strftime("%H:%M %d %b, %Y",
                                      time.strptime(str(timed[0]), '%Y-%m-%d %H:%M:%S')))
        retar.append("<li>" + carrier + " " + trainType + " naar: " + to +
                     " vertrekt om: " + departure + " vannaf spoor: " + platform+"</li>")
    return(str(retar))

if __name__ == '__main__':
    app.run()