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

# WindowDark is an extension of the tkinter.Tk class
import tkinter as tk

from UI_Styles import DarkTheme

colour = DarkTheme()


class WindowDark(tk.Tk):
    # Override the default init for Tk window class
    def __init__(self, w, h, title=""):
        # Create a new window using override direct
        super().__init__()
        self.geometry('{}x{}+{}+{}'.format(w, h + 20, int((1920 - w) / 2), int((1080 - h - 20) / 2)))
        self.overrideredirect(True)
        self.config(bg=colour.bg_1)
        self.last_x = 0
        self.last_y = 0

        # Create a title bar
        window_bar = tk.Frame(self, bg=colour.bg_1, width=w, height=20)
        window_bar.grid_propagate(False)
        window_bar.columnconfigure(0, weight=1)
        window_bar.place(x=0, y=0)
        window_bar.lift()

        self.title = tk.Label(window_bar, text=title, bg=colour.bg_1, fg=colour.txt_2, font='Corbel 10 bold')
        self.title.grid(row=0, column=0, sticky='NSEW')

        # Add an exit button
        exit_frame = tk.Frame(window_bar, bg=colour.bg_1, width=20, height=20)
        exit_frame.place(x=w - 20, y=0)

        exit_frame.columnconfigure(0, weight=1)
        exit_frame.rowconfigure(0, weight=1)
        exit_frame.grid_propagate(False)
        tk.Button(exit_frame, text='X', bg=colour.bg_1, bd=0, fg=colour.txt_1, font='arial 8 bold', command=self.quit) \
            .grid(sticky='NSEW')

        # Bind events for dragging the window around
        window_bar.bind('<B1-Motion>', self.move_window)
        window_bar.bind('<ButtonPress-1>', self.mouse_down)
        self.title.bind('<B1-Motion>', self.move_window)
        self.title.bind('<ButtonPress-1>', self.mouse_down)

        self.root = tk.Frame(self, width=w, height=h, bg=colour.bg_3)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.root.grid_propagate(False)
        self.root.place(x=0, y=20)

    # Function to update the window when the mouse is moved
    def move_window(self, event):
        delta_x = event.x_root - self.last_x
        delta_y = event.y_root - self.last_y
        self.geometry('+{0}+{1}'.format(self.winfo_x() + delta_x, self.winfo_y() + delta_y))
        self.last_x = event.x_root
        self.last_y = event.y_root

    # Function to update the last coordinates of the mouse when the mouse button is pressed
    def mouse_down(self, event):
        self.last_x = event.x_root
        self.last_y = event.y_root

    def set_title(self, title):
        self.title.config(text=title)

    # Function to quit the program
    def quit(self):
        self.destroy()


# Run the main script if we try to run the this file instead
if (__name__ == '__main__'):
    pass
