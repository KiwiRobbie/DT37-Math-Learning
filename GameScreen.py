import tkinter as tk
from UI_Styles import DarkTheme
import json
import random
from EquationsTrees import EquationsTree
from Complex import  Complex
import re
import math
import copy


colour = DarkTheme()

def solve_equation(equation, symbols={}):
    equation = equation.split("$")
    for i, eq in enumerate(equation):
        if "randc" in eq:
            r = int(eq.split("{")[1].split("}")[0])
            equation[i] = (random.randint(-r, r), random.randint(-r, r))
    return Complex( *equation[1] )


class Card(tk.Frame):
    def __init__(self, root) -> None:
        super().__init__(root, bg=colour.bg_3)
        self.columnconfigure(0, weight=1)

        self.root = root
        self.title = 0
        self.body = []
        self.input = 0
        self.responses = []
        self.correct_response = []
        self.content = 0
        self.buttons = []
        self.answered = True

        self.colour = copy.copy(colour)

        self.t = 0
        self.y = 0

    # Add a banner holding the title to the top of the card
    def add_title(self, title):
        self.body.append(tk.Frame(self, width=320, height=24, bg=self.colour.bg_3))
        self.body[-1].grid(row=0, column=0, sticky='NSEW', pady=2)
        self.body[-1].columnconfigure(0, weight=1)
        self.body[-1].rowconfigure(0, weight=1)
        self.body[-1].grid_propagate(False)

        self.title = tk.Label(self.body[-1], text=title, fg=self.colour.txt_2, font='Corbel 12 bold', bd=0,
                              bg=self.colour.bg_2)
        self.title.grid(column=0, sticky='NSEW')

    def add_content(self):
        self.content = tk.Frame(self, width=320, bg=self.colour.bg_2)
        self.content.grid(column=0, sticky='NSEW', pady=2)
        self.content.columnconfigure(0, weight=1)

    # Add a section of text to the card
    def add_text(self, text, font='Corbel 11'):
        self.body.append(tk.Label(self.content, text=text, bg=self.colour.bg_2, fg=self.colour.txt_1, font=font))
        self.body[-1].grid(column=0, sticky='NSEW', pady=4)

    # Add a section of math to the card
    def add_math(self, text, font='Corbel 11'):
        self.body.append(tk.Label(self.content, text=text, bg=self.colour.bg_2, fg=self.colour.txt_1, font=font))
        self.body[-1].grid(column=0, sticky='NSEW', pady=4)

    # Add a single button to accept the card
    def add_single_button(self):
        self.input = tk.Button(self, text='Ok', font='Corbel 12', relief='flat', bg=self.colour.bg_2, fg=self.colour.txt_1)
        self.input.grid(column=0, sticky='NSEW', pady=2)

    # Add a multi-choice input
    def add_tri_button(self, answers, symbols, correct):
        def create_response(data, symbols):
            eq_tree =  EquationsTree()
            eq_tree.build(data)
            eq_tree.insert_symbols(symbols)
            return eq_tree.evaluate()

        self.responses = [ create_response(data, symbols) for data in answers]



        self.correct_response = correct

        self.input = tk.Frame(self, width=320, height=32, bg=self.colour.bg_3)
        self.input.grid(column=0, sticky='NSEW', pady=2)
        self.input.rowconfigure(0, weight=1)
        self.input.grid_propagate(False)

        self.buttons = []
        for i in range(3):
            self.input.columnconfigure(i, weight=1)
            self.buttons.append(
                tk.Button(self.input, text=self.responses[i], relief='flat', bd=0, bg=self.colour.bg_2,
                          fg=self.colour.txt_1, command=(lambda: self.correct(i)) if self.correct_response == i else (lambda: self.incorrect(i))))
            self.buttons[-1].grid(row=0, column=i, sticky='NESW', padx=(2 * (i != 0), 2 * (i != 2)))

    def load_file(self, file):
        with open(file, 'r') as f:
            data = json.loads(f.read())
            self.add_title(data["Title"])
            self.add_content()

            letters = ['u', 'v', 'w', 'p', 'q', 'z']
            symbols = {}

            question = random.choice(list(data["Questions"].values()))
            for txt in question["Question"]:
                if "<txt>" in txt[0]:
                    self.add_text(txt[1])
                elif "<math>" in txt[0]:
                    math = txt[1]

                    for key, value in symbols.items():
                        math = math.replace("[%s]" % key, value[0])

                    math = math.replace("cdot", "•")

                    self.add_math(math)

                elif "<def>" in txt[0]:
                    symbol = txt[1].split('=')[0].split('[')[1].split(']')[0]
                    equation = txt[1].split('=')[1]
                    symbols[symbol] = (letters.pop(random.randrange(0, len(letters))), solve_equation(equation))
                    self.add_math("%s = %s" % symbols[symbol])

            if type(question["Answer"]) == list and len(question["Answer"]) == 3:
                correct = random.randint(0, 2)
                ans = question["Answer"]

                get = ans[0], ans[correct]
                ans[correct], ans[0] = get

                self.add_tri_button(ans, symbols, correct)

    def correct(self, index=None):
        self.queue.pop_card( self.queue.cards.index(self),correct=1  )
        if type(index) is not None:
            for i in range(3):
                self.buttons[i].config(fg=colour.fg_cor, bg=colour.bg_cor)


    def incorrect(self, index=None):
        self.queue.pop_card( self.queue.cards.index(self),correct=0 )
        if type(index) is not None:
            for i in range(3):
                self.buttons[i].config(fg=(colour.fg_cor if i==index else colour.fg_err ),bg=(colour.bg_cor if i==index else colour.bg_err ))

    def animate(self, delta_t):
        def curve(x):
            k=100
            return k/(1-x)-k

        self.place(y=self.y + (1-2*self.answered)*curve(self.t),x=80)
        self.t+=delta_t
        return self.t >= 1

class Queue:
    class Buffer(tk.Frame):
        def __init__(self, root, height):
            super().__init__(root, width=320, height=height, bg=colour.bg_3)
            self.height=height
            self.t = -0.5

        def animate(self,delta_t):
            def curve(x):
                x = max(min(x,1),0)
                return pow(2,1-5*x)-1

            self.config(height=int(self.height * curve(self.t)))
            self.t+=delta_t

            return self.t >= 0.2

    def __init__(self, root) -> None:
        self.root = tk.Frame(root, bg=colour.bg_3)
        self.cards = []
        self.animated = []

        self.target = 100
        self.position = 100
        self.length = 0

        self.root.place(x=80, y=self.position)
        self.top_buffer = self.Buffer(self.root,height=200)
        self.top_buffer.grid(row=0,column=0)

        self.bottom_buffer = self.Buffer(self.root,height=1000)
        self.bottom_buffer.grid(row=1000,column=0)

        self.root.bind_all('<MouseWheel>', self.scroll_handler)
        self.root.bind_all('<Button-5>', self.scroll_handler)
        self.root.bind_all('<Button-4>', self.scroll_handler)

        self.root.lower()
        root.lower()

    def scroll_handler(self, event):
        if event.num == 5:
            self.target -= 45
        elif event.num == 4:
            self.target += 45

        self.target += event.delta / 2

    def append_card(self, card):
        card.queue = self
        self.cards.append(card)
        self.cards[-1].grid(row=len(self.cards), column=0, pady=15, padx=80)
        self.root.update()
        self.length = max(600, self.root.winfo_height()-1060)

    def pop_card(self, i, correct=1):
        removed = self.cards[i]
        removed.answered = correct
        self.cards[i] = self.Buffer(self.root,30+removed.winfo_height())
        removed.y=removed.winfo_rooty()-self.root.winfo_rooty()
        self.cards[i].grid(row=i+1,column=0,padx=80)
        removed.lift()
        self.animated.append(self.cards[i])
        self.animated.append(removed)

    def update(self, delta_t):
        self.target += max((700 - self.target - self.length) * delta_t * 10, 0)
        self.target += min((- self.target) * delta_t * 10, 0)

        self.position += (self.target - self.position) * min(delta_t * 5.0, 1.0)
        self.root.place(x=0, y=self.position-140)

        for i, card in enumerate(self.animated):
            if card.animate(delta_t):
                if card in self.cards:
                    removed = self.animated.pop(i)
                    index = self.cards.index(removed)
                    self.cards.remove(removed)
                    for k in range(index,len(self.cards)):
                        print(index, k)
                        self.cards[k].grid_forget()
                        self.cards[k].grid(row=k+1, column=0, pady=15, padx=80)

                    removed.destroy()
                else:
                    self.animated.pop(i).destroy()
                self.root.update()
                self.length = max(700, self.root.winfo_height() - 1200)

if __name__ == "__main__":
    import main
