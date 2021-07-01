import random

from WindowDark import WindowDark
import time
import UI
import tkinter as tk

root = WindowDark(480, 700, 0, 0)

main_queue = UI.Queue(root.root)

last_t = time.time()
delta_t = 0

for i in range(10):
    new_card=UI.Card(main_queue.root)
    new_card.add_title('Complex Numbers')
    new_card.add_content()
    new_card.add_text('The answer is probably not B\n( Statistically speaking )')
    new_card.add_text('I am not responsible for any issues caused if the answer is actually B',font='Corbel 7 italic')


    new_card.add_tri_button(['A', 'B', 'C'], random.randint(0, 2))
    main_queue.append_card(new_card)


print('Test')

while True:
    main_queue.update(delta_t)

    root.update()

    t = time.time()
    delta_t = t - last_t
    last_t = t
