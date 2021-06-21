import tkinter as tk
from tkinter import ttk
root = tk.Tk()
style = ttk.Style()

#Step 0: Load the gifs
borderImage = tk.PhotoImage("borderImage", file='Testing/Button.gif')
focusBorderImage = tk.PhotoImage("focusBorderImage", file='Testing/Focus.gif')

#Step 1: Create a ttk style 
style.element_create("RoundedFrame",
                     "image", borderImage,
                     ("focus", focusBorderImage),
                     border=32, sticky="NSEW")
style.layout("RoundedFrame",
             [("RoundedFrame", {"sticky": "NSEW"})])

#Step 2: Create frames using the style 
frame1 = ttk.Frame(style="RoundedFrame", padding=16)
frame2 = ttk.Frame(style="RoundedFrame", padding=16)

root.configure(background="#D8D8D8")
frame1.pack(side="top", fill="both", expand=True, padx=20, pady=20)
frame2.pack(side="top", fill="both", expand=True, padx=20, pady=20)

def enter(event):
    event.widget.focus_set()

def exit(event):
    root.focus_set()

frame1.bind("<ButtonPress-1>", enter)
frame1.bind("<ButtonRelease-1>", exit)

frame2.bind("<ButtonPress-1>", enter)
frame2.bind("<ButtonRelease-1>", exit)

#Step 3: Profit
root.mainloop()