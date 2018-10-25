import requests
import xml.etree.ElementTree as ET
import time
import tkinter
from tkinter import *
from tkinter.messagebox import showinfo


def ns_api(station):
    """Voert authenticatie waardes in en returned de xml waarde voor de gegeven parameter(stations naam)."""
    url = 'https://webservices.ns.nl/ns-api-avt?station='+station
    username = 'finn.fonteijn@student.hu.nl'
    password = '0RS_2RtKZsWypx6GIqxneGyzsGOKRO8opRBLN5koe2sR7bjeYNk-XQ'
    auth_values = (username, password)

    response = requests.get(url, auth=auth_values)
    schedule = ET.fromstring(response.content)
    return schedule


def vertrektijden(train_station):
    """
    Creëert per vertrekkende trein een lijst met relevante informatie zoals:
    vertrektijd,eindbestemming,vervoerder,sprinter/intercity en plaatst deze lijsten in een omvangende lijst.
    """
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


def clicked():
    """
    Haalt de invoer van de gebruiker op uit het entry veld, en probeert met deze string een lijst te generen,
    Als dit niet lukt door een verkeerde getypte stationsnaam (de Attribute error) word functie errorpopup() uitgevoerd.
    """
    user_input = str(e1.get())
    try:
        guiwindow(user_input)
    except AttributeError:
        errorpopup(user_input)


def errorpopup(str):
    """Opent een popout venster met de invoer, een boodschap dat dat station niet valide is. """
    bericht = "{} is geen stations naam".format(str)
    showinfo(title='popup', message=bericht)


def guiwindow(str):
    """Functie die een 2de tkinter window opent,met een  lijstbox waarin de vertrektijden in worden getoont."""
    main = tkinter.Tk()
    main.geometry("700x800+200+300")
    main.title("Vetrek tijden voor station {}" .format(str))
    main.configure(background="yellow")
    main.listbox = Listbox(main)
    main.listbox.configure(font=("Comic Sans MS", 12))
    main.listbox['width'] = 50
    main.listbox['height'] = 50
    main.listbox.pack()
    for item in vertrektijden(str):
        main.listbox.insert(END, item)
    main.mainloop()


"""Input window met clicked() functie"""
entrywin = tkinter.Tk()
entrywin.geometry("300x100")
entrywin.title("Voer stations naam in:")
entrywin.configure(background="yellow")
e1 = Entry(master=entrywin, )
e1.pack(padx=10, pady=10)
button = Button(master=entrywin, text='Haal vetrektijden op', command=clicked)
button.pack(pady=10)
entrywin.mainloop()


# vertrektijden("gouda")
