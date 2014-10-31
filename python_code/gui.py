#!/usr/bin/python
import subprocess
from Tkinter import *
import ttk
from main import *
import os

def calculate(*args):
    try:
        value = feet.get()
        sql = process_query(value)
        meters.set(sql)
        f = os.popen('./../stat_moses/convert.sh \''+value+'\'')
        meters_stat.set(f.read())
    except ValueError:
        print 'passing'
        pass
    
root = Tk()
root.title("Natural Language to SQL")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()
meters_stat = StringVar()

feet_entry = ttk.Entry(mainframe, width=60, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=meters_stat).grid(column=2, row=3, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=1, sticky=W)

ttk.Label(mainframe, text="Natural Language query").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Rule Based Output").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Statistical Output").grid(column=1, row=3, sticky=E)
# ttk.Label(mainframe, text="").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()
