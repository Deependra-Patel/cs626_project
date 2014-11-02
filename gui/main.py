import subprocess
from Tkinter import *
import ttk


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set("something")
    except ValueError:
        pass
    
root = Tk()
root.title("Natural Language to SQL Converter")

# Get config.py info here
#md = MyDialog(Tk())
#md.body(root)
#username, password, database = md.apply()
#print md.apply()
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=60, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Natural Language query:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Converted SQL").grid(column=1, row=2, sticky=E)
# ttk.Label(mainframe, text="").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()
