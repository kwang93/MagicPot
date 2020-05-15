from sys import platform as sys_pf

if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import serial
import time
import os

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
time.sleep(2)


def getReading():

    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)

    temperature = []
    data = []                       # empty list to store the data
    for i in range(1):
        b = ser.readline()          # read a byte string
        string_n = b.decode()       # decode byte string into Unicode
        string = string_n.rstrip()  # remove \n and \r
        readings = string.split('z')
        print(readings)
        temperature.append(readings[1])
        humidity = readings[2]
        flt = float(readings[0])         # convert string to float
        data.append(flt)            # add to the end of data list
        data.append(100.0 - flt)  # add to the end of data list
        time.sleep(0.1)             # wait (sleep) 0.1 seconds

    ser.close()
    return data, temperature, humidity

def draw_plot(data):
    labels = 'Moisuture Percentage', 'Dry Percentage'
    plt.pie(data, labels=labels, colors=['blue', 'brown'], autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.show(block=False)


data, temperature, humidity = getReading()
moisture = data[0]
layout = [[sg.Button('Show Visual'), sg.Cancel()],
          [sg.Text('Soil Moisture Percentage: ' + str(data[0]) + '%')],
          [sg.Text('Temperature: ' + str(temperature[0]) + '\u00b0 C')],
          [sg.Text('Humidity: ' + str(humidity) + '%')]]

window = sg.Window('MagicPot Dashboard', layout)

while True:
    data, temperature, humidity = getReading()
    if data[0] < 50:
        message = "Time to water your plant!"
        name = "Lukas Griffin"
        preparedM = 'osascript -e \'tell application \"Messages\" to send \"' + message + '\" to buddy \"' + name + '\"\''
        os.system(preparedM)
    if float(temperature[0]) < 10:
        message = "Your plant is to cold!"
        name = "Lukas Griffin"
        preparedM = 'osascript -e \'tell application \"Messages\" to send \"' + message + '\" to buddy \"' + name + '\"\''
        os.system(preparedM)
    event, values = window.read()

    if event in (None, 'Cancel'):
        break
    elif event == 'Show Visual':
        plt.close()
        data, temperature, humidity = getReading()

        if data[0] < 50:
            message = "Time to water your plant!"
            name = "Lukas Griffin"
            preparedM = 'osascript -e \'tell application \"Messages\" to send \"' +message + '\" to buddy \"' + name + '\"\''
            os.system(preparedM)
        if float(temperature[0]) < 10:
            message = "Your plant is to cold!"
            name = "Lukas Griffin"
            preparedM = 'osascript -e \'tell application \"Messages\" to send \"' +message + '\" to buddy \"' + name + '\"\''
            os.system(preparedM)

        draw_plot(data)
        window.close()
        layout = [[sg.Button('Show Visual'), sg.Cancel()],
                  [sg.Text('Soil Moisture Percentage: ' + str(data[0]) + '%')],
                  [sg.Text('Temperature: ' + str(temperature[0]) + '\u00b0 C')],
                  [sg.Text('Humidity: ' + str(humidity) + '%')]]

        window = sg.Window('MagicPot Dashboard', layout)

window.close()
