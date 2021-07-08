import tkinter as tk
from UI_Styles import DarkTheme
import json
import random
from EquationsTrees import EquationsTree
import re

colour = DarkTheme()


def solve_equation(equation, symbols={}):
    equation = equation.split("$")
    for i, eq in enumerate(equation):
        if "randc" in eq:
            r = int(eq.split("{")[1].split("}")[0])
            equation[i] = ("_%d+_%di" % (random.randint(-r, r), random.randint(-r, r))) \
                .replace("+-", "-").replace("1i", "i").replace("_-","-").replace("_", " ")
            equation[i] = re.sub(".0i|0.", "", equation[i])
            equation[i] = equation[i] if equation[i] != " " else " 0"
    return ''.join(equation)


class Card(tk.Frame):
    def __init__(self, root) -> None:
        super().__init__(root, bg=colour.bg_3)
        self.columnconfigure(0, weight=1)

        self.title = 0
        self.body = []
        self.input = 0
        self.responses = []
        self.correct_response = []
        self.content = 0
        self.buttons = []

    # Add a banner holding the title to the top of the card
    def add_title(self, title):
        self.body.append(tk.Frame(self, width=360, height=24, bg=colour.bg_3))
        self.body[-1].grid(row=0, column=0, sticky='NSEW', pady=2)
        self.body[-1].columnconfigure(0, weight=1)
        self.body[-1].rowconfigure(0, weight=1)
        self.body[-1].grid_propagate(False)

        self.title = tk.Label(self.body[-1], text=title, fg=colour.txt_2, font='Corbel 12 bold', bd=0,
                              bg=colour.bg_2)
        self.title.grid(column=0, sticky='NSEW')

    def add_content(self):
        self.content = tk.Frame(self, width=320, bg=colour.bg_2)
        self.content.grid(column=0, sticky='NSEW', pady=2)
        self.content.columnconfigure(0, weight=1)

    # Add a section of text to the card
    def add_text(self, text, font='Corbel 11'):
        self.body.append(tk.Label(self.content, text=text, bg=colour.bg_2, fg=colour.txt_1, font=font))
        self.body[-1].grid(column=0, sticky='NSEW', pady=4)

    # Add a section of math to the card
    def add_math(self, text, font='Corbel 11'):
        self.body.append(tk.Label(self.content, text=text, bg=colour.bg_2, fg=colour.txt_1, font=font))
        self.body[-1].grid(column=0, sticky='NSEW', pady=4)

    # Add a single button to accept the card
    def add_single_button(self):
        self.input = tk.Button(self, text='Ok', font='Corbel 12', relief='flat', bg=colour.bg_2, fg=colour.txt_1)
        self.input.grid(column=0, sticky='NSEW', pady=2)

    # Add a multi-choice input
    def add_tri_button(self, answers, correct):
        self.responses = answers
        self.correct_response = correct

        self.input = tk.Frame(self, width=320, height=32, bg=colour.bg_3)
        self.input.grid(column=0, sticky='NSEW', pady=2)
        self.input.rowconfigure(0, weight=1)
        self.input.grid_propagate(False)

        self.buttons = []
        for i in range(3):
            self.input.columnconfigure(i, weight=1)
            self.buttons.append(
                tk.Button(self.input, text=self.responses[i], relief='flat', bd=0, bg=colour.bg_2,
                          fg=colour.txt_1, command=self.correct if self.correct_response == i else self.incorrect))
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
                if "<txt>" in txt:
                    self.add_text(txt[5:])
                elif "<math>" in txt:
                    math = txt[6:]

                    for key, value in symbols.items():
                        math = math.replace("[%s]" % key, value[0])

                    math = math.replace("cdot", "•")

                    self.add_math(math)

                elif "<def>" in txt:
                    symbol = txt.split('=')[0].split('[')[1].split(']')[0]
                    equation = txt.split('=')[1]
                    symbols[symbol] = (letters.pop(random.randrange(0, len(letters))), solve_equation(equation))
                    self.add_math("%s = %s" % symbols[symbol])

            if type(question["Answer"]) == list and len(question["Answer"]) == 3:
                correct = random.randint(0, 2)
                ans = question["Answer"]

                get = ans[0], ans[correct]
                ans[correct], ans[0] = get

                trees = [ EquationsTree() for i in range(3) ]
                trees = [ tree.build(ans[i]) for i, tree in enumerate(trees) ]
                ans = [ tree.evaluate() for tree in trees ]

                self.add_tri_button(ans, correct)

    def correct(self):
        print('Correct')

    def incorrect(self):
        print('Try Again')


class Queue:
    def __init__(self, root) -> None:
        self.root = tk.Frame(root, bg=colour.bg_3)
        self.cards = []

        self.target = 100
        self.position = 100
        self.length = 0

        self.root.place(x=60, y=self.position)

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

    def update(self, delta_t):
        self.target += max((660 - self.target - self.length) * delta_t * 10, 0)
        self.target += min((60 - self.target) * delta_t * 10, 0)

        self.position += (self.target - self.position) * min(delta_t * 5.0, 1.0)
        self.root.place(x=60, y=self.position)

    def append_card(self, card):
        self.cards.append(card)
        self.cards[-1].grid(row=len(self.cards) - 1, column=0, pady=15)
        self.root.update()
        self.length = max(600, self.root.winfo_height())

    def remove_card(self):
        pass


if __name__ == "__main__":
    import main
