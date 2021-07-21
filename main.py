import random
from WindowDark import WindowDark
import time
import UI
import tkinter as tk

root = WindowDark(480, 700, 0, 0)

main_queue = UI.Queue(root.root)

last_t = time.time()
delta_t = 0

for i in range(5):
    new_card = UI.Card(main_queue.root)
    new_card.load_file('Courses/Complex-Numbers/Basic-Arithmetic.json')
    main_queue.append_card(new_card)


while True:
    main_queue.update(delta_t)

    root.update()

    t = time.time()
    delta_t = t - last_t
    last_t = t
