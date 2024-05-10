import serial
import time
from time import sleep
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import *
from tkcalendar import DateEntry
import datetime

WIDTH = 1920
HEIGHT = 1200
keyonhook = 0
sendsignal = 0
setreminders = []

class MainGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="#0C0F19")
        self.foreground = "#111524"
        self.list_1 = []
        self.list_2 = []
        self.list_3 = []
        self.list_4 = []
        self.list_5 = []
        self.list_6 = []
        self.checkboxes = []
        self.setupGUI()
        self.grid(sticky=N+S+E+W)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=7)
        self.columnconfigure(4, weight=7)
        self.columnconfigure(5, weight=10)
        self.rowconfigure(2, weight=1)

    def setupGUI(self):
        l1 = tk.Label(self, text="Reminders:", font=("Consolas", 14), bg=f'{self.foreground}', fg="#8ADFE0")
        l1.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)

        l2 = tk.Label(self, text="Set Date:", font=("Consolas", 14), bg=f'{self.foreground}', fg="#8ADFE0")
        l2.grid(row=0, column=1, padx=10, pady=10, sticky=N+S+E+W)

        l3 = tk.Label(self, text="Due Date:", font=("Consolas", 14), bg=f'{self.foreground}', fg="#8ADFE0")
        l3.grid(row=0, column=2, padx=10, pady=10, sticky=N+S+E+W)

        l5 = tk.Label(self, text="Hours", font=("Consolas", 14), bg=f'{self.foreground}', fg="#8ADFE0")
        l5.grid(row=0, column=3, padx=10, pady=10, sticky=N+S+E+W)

        l6 = tk.Label(self, text="Minutes", font=("Consolas", 14), bg=f'{self.foreground}', fg="#8ADFE0")
        l6.grid(row=0, column=4, padx=10, pady=10, sticky=N+S+E+W)

        l7 = tk.Label(self, text="AM/PM", font=("Consolas", 14), bg=f'{self.foreground}', fg="#8ADFE0")
        l7.grid(row=0, column=5, padx=10, pady=10, sticky=N+S+E+W)

        self.e1 = tk.Entry(self, font=("Consolas", 12))
        self.e1.grid(row=1, column=0, padx=10, pady=10, sticky=N+S+E+W)

        self.e2 = tk.Entry(self, state='readonly',font=("Consolas", 12), bg="#9E9E9E")
        self.e2.grid(row=1, column=1, padx=10, pady=10, sticky=N+S+E+W)

        self.hour_entry = tk.ttk.Combobox(self, state='readonly', values=[i for i in range(1,13)])
        self.hour_entry.grid(row=1, column=3, padx=10, pady=10, sticky=N+S+E+W)

        self.minute_entry = tk.ttk.Combobox(self, state='readonly', values=[i for i in range(0,60) if i == 0 or i % 5 == 0])
        self.minute_entry.grid(row=1, column=4, padx=10, pady=10, sticky=N+S+E+W)

        self.e3_var = tk.StringVar()
        self.e3 = DateEntry(self, font=("Consolas", 12), state='readonly', textvariable=self.e3_var, mindate=datetime.datetime.now())
        self.e3.grid(row=1, column=2, padx=10, pady=10, sticky=N+S+E+W)

        self.AM_PM = tk.ttk.Combobox(self, state="readonly", values=["AM", "PM"])
        self.AM_PM.grid(row=1, column=5, padx=10, pady=10, sticky=N+S+E+W)

        self.b1 = tk.Button(self, text="Enter", font=("Consolas", 12), command=lambda: self.process("Enter"))
        self.b1.grid(row=1, column=6, padx=10, pady=10, sticky=N+S+E+W)

        self.listbox_1 = tk.Listbox(self, font=("Consolas", 14), bg=f'{self.foreground}', fg="#ECA47D")
        self.listbox_1.grid(row=2, column=0, padx=10, pady=10, sticky=N+S+E+W)

        self.listbox_2 = tk.Listbox(self, font=("Consolas", 14), bg=f'{self.foreground}', fg="#ECA47D")
        self.listbox_2.grid(row=2, column=1, padx=10, pady=10, sticky=N+S+E+W)

        self.listbox_3 = tk.Listbox(self, font=("Consolas", 14), bg=f'{self.foreground}', fg="#ECA47D")
        self.listbox_3.grid(row=2, column=2, padx=10, pady=10, sticky=N+S+E+W)

        self.listbox_4 = tk.Listbox(self, font=("Consolas", 14), bg=f'{self.foreground}', fg="#ECA47D")
        self.listbox_4.grid(row=2, column=3, padx=10, pady=10, sticky=N+S+E+W)

        self.listbox_6 = tk.Listbox(self, font=("Consolas", 14), bg=f'{self.foreground}', fg="#ECA47D")
        self.listbox_6.grid(row=2, column=4, padx=10, pady=10, sticky=N+S+E+W)

        self.listbox_5 = tk.Listbox(self, font=("Consolas", 14), bg=f'{self.foreground}', fg="#ECA47D")
        self.listbox_5.grid(row=2, column=5, padx=10, pady=10, sticky=N+S+E+W)

        self.frame_4 = tk.Frame(self, bg=f'{self.foreground}')
        self.frame_4.grid(row=2, column=6, padx=10, pady=10, sticky=N+S+E+W)

        l5 = tk.Label(self, text="Completed Reminders:", font=("Consolas", 12), bg=f'{self.foreground}', fg="#8ADFE0")
        l5.grid(row=3, column=1, columnspan=4, padx=10, pady=10, sticky=N+S+E+W)

        self.finished_tasks = tk.Listbox(self, font=("Consolas", 14), height=5, bg=f'{self.foreground}', fg="#F05370")
        self.finished_tasks.grid(row=4, column=1, columnspan=4, padx=10, pady=10, sticky=N+S+E+W)

    def move_to_finished(self, index):
        print("Index:", index)
        print("Length of checkboxes:", len(self.checkboxes))
        if self.checkboxes[index][1].get():  # Check if the checkbox is actually checked
            del setreminders[index]
            task = f"{self.list_1[index]}"
            self.finished_tasks.insert(tk.END, task)
            self.listbox_1.delete(index)
            self.listbox_2.delete(index)
            self.listbox_3.delete(index)
            self.listbox_4.delete(index)
            self.listbox_5.delete(index)
            self.listbox_6.delete(index)
            self.checkboxes[index][0].destroy()
            del self.list_1[index]
            del self.list_2[index]
            del self.list_3[index]
            del self.list_4[index]
            del self.list_5[index]
            del self.list_6[index]
            del self.checkboxes[index]

            # Update grid positions of remaining checkboxes
            for i, (cb, var) in enumerate(self.checkboxes):
                cb.grid(row=i, column=0, sticky=tk.W)

    def process(self, button):
        if button == "Enter":
            new_entry = (self.e1.get(), self.e2.get(), self.e3.get(), self.hour_entry.get(), self.minute_entry.get(), self.AM_PM.get())
            if new_entry[0] == '' or new_entry[1] != '' or new_entry[2] == '' or new_entry[3] == '':
                return
            self.e2.config(state='normal')
            self.e2.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            set_date_entry = self.e2.get()
            setreminders.append(f"{self.e1.get()}+{self.e2.get()}+{self.e3.get()}+{self.hour_entry.get()}+{self.minute_entry.get()}+{self.AM_PM.get()}")
            print(setreminders)
            self.list_1.append(new_entry[0])
            self.list_2.append(set_date_entry)
            self.list_3.append(new_entry[2])
            self.list_4.append(new_entry[3])
            self.list_5.append(new_entry[5])
            self.list_6.append(new_entry[4])
            
            self.listbox_1.insert(tk.END, new_entry[0])
            self.listbox_2.insert(tk.END, set_date_entry)
            self.listbox_3.insert(tk.END, new_entry[2])
            self.listbox_4.insert(tk.END, new_entry[3])
            self.listbox_5.insert(tk.END, new_entry[5])
            self.listbox_6.insert(tk.END, new_entry[4])
            self.e2.delete(0, END)
            self.e2.config(state='readonly')
            
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.frame_4, text="Done", variable=var, command=lambda index=len(self.checkboxes): self.move_to_finished(index))
            cb.grid(row=len(self.checkboxes), column=0, sticky=tk.W)
            self.checkboxes.append((cb, var))

            print("Number of checkboxes:", len(self.checkboxes))
            
            self.e1.delete(0, tk.END)
            self.e3.set_date(datetime.datetime.now())

def TimeAsLED(startdate, enddate):
    print(startdate)
    print(enddate)
    date_current = datetime.datetime.now()
    print(date_current)
    currenttime = date_current - startdate
    endtime = enddate - startdate
    currentminutes = (currenttime).total_seconds() / 60.0
    endminutes = (endtime).total_seconds() / 60.0
    if endminutes <= 0:
        return 255
    LEDValue = int((currentminutes - 0)*(255-0)/(endminutes-0)+0)
    print(LEDValue)
    return LEDValue
ser = serial.Serial('COM4', 9600)  
ser.timeout = 1  
window = tk.Tk()
window.attributes('-fullscreen', True)
window.title("Keyminder App")
window.geometry(f"{WIDTH}x{HEIGHT}")
p = MainGUI(window)

try:
    while True:
        window.update_idletasks()
        window.update()
        # Important Comment Line
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data.startswith("Ultrasonic:"):
                ultrasonic_value = int(data.split(":")[1])
                print("Ultrasonic value:", ultrasonic_value)
                if keyonhook == 0:
                    if 1 <= ultrasonic_value <= 6:
                        sendsignal = 1
                        keyonhook = 1
                elif keyonhook == 1:
                    if 300 > ultrasonic_value > 6:
                        sendsignal = 1
                        keyonhook = 0
                if sendsignal == 1:
                    LEDLIST = []
                    for reminder in setreminders:
                        date_current = datetime.datetime.now()
                        reminder_components = reminder.split('+')
                        reminder_name = reminder_components[0]
                        reminder_setdate = reminder_components[1]
                        reminder_enddate = reminder_components[2]
                        reminder_hours = reminder_components[3]
                        reminder_minutes = reminder_components[4]
                        reminder_AMPMstatus = reminder_components[5]
                        fixed_reminder_hours = int(reminder_hours)
                        fixed_reminder_minutes = int(reminder_minutes)
                        if reminder_AMPMstatus == "PM":
                            fixed_reminder_hours = int(reminder_hours) + 12
                        date_start = datetime_object = datetime.datetime.strptime(reminder_setdate, "%Y-%m-%d %H:%M")
                        date_end_without_hours = datetime.datetime.strptime(reminder_enddate, "%m/%d/%y")
                        date_end = date_end_without_hours + timedelta(hours=(fixed_reminder_hours)) + timedelta(minutes=(fixed_reminder_minutes))
                        LEDValue = TimeAsLED(date_start, date_end)
                        if LEDValue <= 0:
                            LEDValue = 0
                        elif LEDValue >= 255:
                            LEDValue = 255
                        LEDLIST.append(LEDValue)
                    sendstring = str(LEDLIST)
                    ser.write(sendstring.encode() + b'\n')
                    print("Sent string to Arduino")
                    sendsignal = 0
            else:
                try:
                    received_value = int(data)
                except ValueError:
                    print("Received invalid value:", data)
        time.sleep(0.1)  
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed")