import requests
import xml.etree.ElementTree as ET
import time
import tkinter
from tkinter import *
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image


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


def clicked():
    user_input = str(e1.get())
    try:
        guiwindow(user_input)
    except AttributeError:
        errorpopup(user_input)
    return(user_input)


def errorpopup(str):
    bericht = "{} is geen stations naam".format(str)
    showinfo(title='popup', message=bericht)


def guiwindow(str):
    main = tkinter.Tk()
    main.geometry("700x800+200+300")
    main.title("Vetrek tijden voor station {}" .format(str))
    main.configure(background="yellow")
    # main.panel = Label(
    #     main, text="Vertrektijden voor station {}" .format(str))
    # main.label.pack()
    main.listbox = Listbox(main)
    main.listbox.configure(font=("Comic Sans MS", 12))
    main.listbox['width'] = 50
    main.listbox['height'] = 50
    main.listbox.pack()
    for item in vertrektijden(str):
        main.listbox.insert(END, item)
    main.mainloop()


entrywin = tkinter.Tk()
entrywin.geometry("300x100")
entrywin.title("Voer stations naam in:")
entrywin.configure(background="yellow")
e1 = Entry(master=entrywin, )
e1.pack(padx=10, pady=10)
button = Button(master=entrywin, text='Druk hier', command=clicked)
button.pack(pady=10)
entrywin.mainloop()


# vertrektijden("gouda")
