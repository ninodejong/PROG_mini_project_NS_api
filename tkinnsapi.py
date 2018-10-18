import requests
import xml.etree.ElementTree as ET
import time
import tkinter
from tkinter import *


def ns_api(station):
    url = 'https://webservices.ns.nl/ns-api-avt?station='+station
    username = 'finn.fonteijn@student.hu.nl'
    password = '0RS_2RtKZsWypx6GIqxneGyzsGOKRO8opRBLN5koe2sR7bjeYNk-XQ'
    auth_values = (username, password)

    response = requests.get(url, auth=auth_values)
    schedule = ET.fromstring(response.content)
    return schedule


def vertrektijden(train_station):
    station = train_station
    schedule = ns_api(train_station)
    row = []
    for departure in schedule:
        carrier = departure.find('Vervoerder').text
        trainType = departure.find('TreinSoort').text
        dep_time = departure.find('VertrekTijd').text.split('T')
        timed = str(dep_time[0] + " "+dep_time[1]).split('+')
        depart = str(time.strftime("%H:%M", time.strptime(
            str(timed[0]), '%Y-%m-%d %H:%M:%S')))
        to = departure.find('EindBestemming').text
        rideID = departure.find('RitNummer').text
        platform = departure.find('VertrekSpoor').text
        platformChange = departure.find('VertrekSpoor').attrib
        row.extend([[depart, to, carrier+' '+trainType, platform, ]])
    return (row)


def guiwindow():
    window = tkinter.Tk()
    window.geometry("700x800+300+300")
    window.title("NS TIJDEN V1N Groep 3")
    window.configure(background="yellow")
    img = PhotoImage(file="C:\HU\PRIVATE\logo.png")
    label = Label(image=img)
    label.image = img
    label.pack()

    window.listbox = Listbox(window)
    window.listbox.configure(font=("Comic Sans MS", 12))
    window.listbox['width'] = 50
    window.listbox['height'] = 50
    window.listbox.pack()

    for item in vertrektijden("utrecht centraal"):
        window.listbox.insert(END, item)

    window.mainloop()


guiwindow()

# vertrektijden("gouda")
