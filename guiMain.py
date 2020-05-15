from sys import platform as sys_pf

if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
import PySimpleGUI as sg
import matplotlib.backends.tkagg as tkagg
from matplotlib.figure import Figure
import serial
import time
import tkinter as Tk

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
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Temperature axis")
    ax.set_ylabel("Time axis")
    ax.grid()

    print("data:", data)
    labels = 'Moisuture Percentage', 'Dry Percentage'
    plt.pie(data, labels=labels, colors=['blue', 'brown'], autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    #plt.show(block=False)
    fig = plt.gcf()
    return fig


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    return figure_canvas_agg


data, temperature, humidity = getReading()

layout = [[sg.Cancel(), sg.Button('Update')],
          [sg.Canvas(size=(640, 480), key='canvas')],
          [sg.Text('Temperature: ' + str(temperature[0]) + '\u00b0 C')],
          [sg.Text('Humidity: ' + str(humidity) + '%')]]
window = sg.Window('MagicPot Dashboard', layout, finalize=True)

fig = draw_plot(data)
canvas_elem = window['canvas']
graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
canvas = canvas_elem.TKCanvas

graph.draw()
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
figure_w, figure_h = int(figure_w), int(figure_h)
photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

canvas.create_image(640 / 2, 480 / 2, image=photo)

figure_canvas_agg = FigureCanvasAgg(fig)
figure_canvas_agg.draw()

tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)


while True:
    data, temperature, humidity = getReading()
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'Update':
        window.close()
        data, temperature, humidity = getReading()

        layout = [[sg.Cancel(), sg.Button('Update')],
                  [sg.Canvas(size=(640, 480), key='canvas')],
                  [sg.Text('Temperature: ' + str(temperature[0]) + '\u00b0 C')],
                  [sg.Text('Humidity: ' + str(humidity) + '%')]]
        window = sg.Window('MagicPot Dashboard', layout, finalize=True)

        fig = draw_plot(data)
        canvas_elem1 = window['canvas']
        graph1 = FigureCanvasTkAgg(fig, master=canvas_elem1.TKCanvas)
        canvas1 = canvas_elem1.TKCanvas

        graph1.draw()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo1 = Tk.PhotoImage(master=canvas1, width=figure_w, height=figure_h)

        canvas1.create_image(640 / 2, 480 / 2, image=photo1)

        figure_canvas_agg1 = FigureCanvasAgg(fig)
        figure_canvas_agg1.draw()

        tkagg.blit(photo1, figure_canvas_agg1.get_renderer()._renderer, colormode=2)


        #fig = draw_plot(data)
        #fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

window.close()
