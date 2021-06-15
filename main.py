from tkinter.constants import RIDGE
from WindowDark import WindowDark
import UI
import time
from math import sin

root=WindowDark(480,700,0,0)
button=UI.Card(root.root,0)
main_queue=UI.Queue(root.root)

while True:
    button.update(100)
    root.window.update()

