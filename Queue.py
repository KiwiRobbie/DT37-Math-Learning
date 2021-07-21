# Modular Queue System for holding card lists
import tkinter as tk
from UI_Styles import DarkTheme
import random
from EquationsTrees import EquationsTree
from Complex import  Complex
import math
import copy

style = DarkTheme()

class Queue:
    class Buffer(tk.Frame):
        def __init__(self, root, height):
            super().__init__(root, width=320, height=height, bg=style.bg_3)
            self.height=height
            self.t = -0.5

    def __init__(self, root) -> None:
        self.root = tk.Frame(root, bg=style.bg_3)
        self.cards = []
        self.animated = []

        self.target = 100
        self.position = 100
        self.length = 0
        self.padx = 60

        self.root.place(x=80, y=self.position)
        self.top_buffer = self.Buffer(self.root,height=200)
        self.top_buffer.grid(row=0,column=0)

        self.bottom_buffer = self.Buffer(self.root,height=1000)
        self.bottom_buffer.grid(row=1000,column=0)

        self.root.bind_all('<MouseWheel>', self.scroll_handler)
        self.root.bind_all('<Button-5>', self.scroll_handler)
        self.root.bind_all('<Button-4>', self.scroll_handler)
        #
        # self.root.lower()
        # root.lower()

    def scroll_handler(self, event):
        if event.num == 5:
            self.target -= 45
        elif event.num == 4:
            self.target += 45

        self.target += event.delta / 2

    def append_card(self, card):
        card.queue = self
        self.cards.append(card)
        self.cards[-1].grid(row=len(self.cards), column=0, pady=15, padx=self.padx)
        self.root.update()
        self.length = max(700, self.root.winfo_height()-1200)

    def update(self, delta_t):
        self.target += max((700 - self.target - self.length) * delta_t * 10, 0)
        self.target += min((- self.target) * delta_t * 10, 0)

        self.position += (self.target - self.position) * min(delta_t * 5.0, 1.0)
        self.root.place(x=0, y=self.position-140)

