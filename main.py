from WindowDark import WindowDark
import time
import UI
import tkinter as tk

root=WindowDark(480,700,0,0)

main_queue=UI.Queue(root.root)

last_t=time.time()
delta_t=0

for i in range(10):
    main_queue.append_card(tk.Label(text='Test'))

while True:
    main_queue.update(delta_t)

    root.update()

    t=time.time()
    delta_t=t-last_t
    last_t=t
