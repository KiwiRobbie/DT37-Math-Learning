"""
====================================================================
  __          ___           _               _____             _
  \ \        / (_)         | |             |  __ \           | |
   \ \  /\  / / _ _ __   __| | _____      _| |  | | __ _ _ __| | __
    \ \/  \/ / | | '_ \ / _` |/ _ \ \ /\ / / |  | |/ _` | '__| |/ /
     \  /\  /  | | | | | (_| | (_) \ V  V /| |__| | (_| | |  |   <
      \/  \/   |_|_| |_|\__,_|\___/ \_/\_/ |_____/ \__,_|_|  |_|\_\ 
====================================================================
Class for creating windows that use a custom title bar and darktheme
"""

from UI_Styles import DarkTheme

colour=DarkTheme()

#WindowDark is an extension of the tkinter.Tk class
import tkinter as tk
class WindowDark():

    #Override the defualt init for Tk window class
    def __init__(self, w, h, x=710,y=100):
        #Create a new window using overide dirrect
        self.window=tk.Tk()
        self.window.geometry('{}x{}+{}+{}'.format(w,h+20,int((1920-w)/2),int((1080-h-20)/2)))
        self.window.overrideredirect(True)
        self.window.config(bg=colour.bg_1)
        self.last_x=0
        self.last_y=0

        #Create a title bar
        window_bar = tk.Frame(self.window,bg=colour.bg_1,width=500,height=20)
        window_bar.place(x=0,y=0)
        window_bar.lift()

        #Add an exit button
        exit_frame = tk.Frame(window_bar,bg=colour.bg_1,width=20,height=20)
        exit_frame.place(x=w-20,y=0)

        exit_frame.columnconfigure(0,weight=1)
        exit_frame.rowconfigure(0,weight=1)
        exit_frame.grid_propagate(False)
        tk.Button(exit_frame,text='X',bg=colour.bg_1,bd=0,fg=colour.txt_1,font='arial 8 bold',command=quit).grid(sticky='nesw')

        #Bind events for dragging the window arround
        window_bar.bind('<B1-Motion>', self.move_window)
        window_bar.bind('<ButtonPress-1>', self.mouse_down)

        self.root=tk.Frame(self.window,width=w,height=h,bg=colour.bg_3)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.root.grid_propagate(False)
        self.root.place(x=0,y=20)

    #Fuction to update the window when the mouse is moved
    def move_window(self,event):
        delta_x=event.x_root-self.last_x 
        delta_y=event.y_root-self.last_y 
        self.window.geometry('+{0}+{1}'.format(self.window.winfo_x() + delta_x ,self.window.winfo_y()+delta_y))
        self.last_x=event.x_root
        self.last_y=event.y_root

    #Function to update the last coordinates of the mouse when the mouse button is pressed
    def mouse_down(self,event):
        self.last_x=event.x_root
        self.last_y=event.y_root

    #Function to quit the program
    def quit(self):
        self.window.destroy()

#Run the main script if we try to run the this file instead
if(__name__=='__main__'):
    import main 