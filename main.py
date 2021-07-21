import random
from WindowDark import WindowDark
import time
import ModuleScreen
import GameScreen
import tkinter as tk

root = WindowDark(480, 700)


menu_screen = ModuleScreen.Screen(root)

last_t = time.time()
delta_t = 0

while menu_screen.running:
    menu_screen.update(delta_t)
    root.update()

    t = time.time()
    delta_t = t - last_t
    last_t = t

menu_screen.destroy()
game_screen = GameScreen.Queue(root.root) #menu_screen.game_screen

for i in range(2):
    new_card = GameScreen.Card(game_screen.root)
    new_card.load_file('Courses/Complex-Numbers/Basic-Arithmetic.json')
    game_screen.append_card(new_card)


while True:
    game_screen.update(delta_t)
    root.update()

    t = time.time()
    delta_t = t - last_t
    last_t = t
