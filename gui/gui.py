#GUI Program for managing I/O of the translator

# Import the required GUI elements
from Tkinter import *
import tkSimpleDialog
import tkMessageBox

# Set up the GUI
root = Tk()
w = Label(root, text="")
w.pack()

# Show the welcome message
tkMessageBox.showinfo("Welcome","Hi, we welcome you to our English to SQL query translator program !!")

# Get the user info
