import PySimpleGUI as sg
from tkinter import Tk
from tkinter import Label
import time
import sys

master = Tk()
master.title("_")
test_var = 1
def get_time():
    timeVar = time.strftime("%I:%M:%S %p")
    clock.config(text=timeVar)
    clock.after(1000,get_time)
    sg.theme("DefaultNoMoreNagging")
    layout = [[sg.Text(time.strftime("%I")), sg.Text(time.strftime("%M")), sg.Text(time.strftime("%S")), sg.Text(time.strftime("%p"))]]
    window = sg.Window("Timer", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            test_var = 2

clock = Label(master, font=("Calibri",1),bg="white",fg="white")
clock.pack(),

if test_var == 1:
    get_time()

master.mainloop()