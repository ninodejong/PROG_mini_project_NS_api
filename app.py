import requests
import xml.etree.ElementTree as ET
import time
from flask import Flask, render_template
app = Flask(__name__)

def ns_api(station):
    url = 'https://webservices.ns.nl/ns-api-avt?station='+station
    username = 'ninodejong@gmail.com'
    password = 'zAXbd8mqx6bgNtNKVasUxd_Pn8bKKb3SQVS-wOY365uGYhVk4t1F7w'
    auth_values = (username, password)

    response = requests.get(url, auth=auth_values)
    schedule = ET.fromstring(response.content)
    return schedule

# schedule = ns_api(',bnlnlknl')
# if schedule.find('error') != -1:
#     print('continue')
# else:
#     print('error')
#     print(schedule)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/<train_station>')
def vertrektijden(train_station):
    station = train_station
    schedule = ns_api(train_station)
    row = []
    for departure in schedule:
        carrier = departure.find('Vervoerder').text
        trainType = departure.find('TreinSoort').text
        dep_time = departure.find('VertrekTijd').text.split('T')
        timed = str(dep_time[0]+ " "+dep_time[1]).split('+')
        depart = str(time.strftime("%H:%M",time.strptime(str(timed[0]),'%Y-%m-%d %H:%M:%S')))
        to = departure.find('EindBestemming').text
        rideID = departure.find('RitNummer').text
        platform = departure.find('VertrekSpoor').text
        platformChange = departure.find('VertrekSpoor').attrib

        row.extend([[depart,to,carrier+' '+trainType,platform]])
    return render_template('app.html', **locals())

if __name__ == '__main__':
    app.run(host='127.0.0.1')