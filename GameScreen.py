import copy
import json
import random
import time
import tkinter as tk

from Complex import Complex
from EquationsTrees import EquationsTree
from Queue import Queue as BaseQueue
from UI_Styles import DarkTheme

style = DarkTheme()


def solve_equation(equation, symbols={}):
    equation = equation.split("$")
    for i, eq in enumerate(equation):
        if "randc" in eq:
            r = int(eq.split("{")[1].split("}")[0])
            equation[i] = (random.randint(-r, r), random.randint(-r, r))
    return Complex(*equation[1])


class Screen:
    def __init__(self, root, directory):
        with open('Courses/%s/index.json' % directory, 'r') as f:
            self.json_index = json.loads(f.read())

        with open('data/save.json', 'r') as f:
            self.json_save = json.loads(f.read())

        self.section = ""
        for section in self.json_index["Sections"].keys():
            if self.json_save[self.json_index["Course"]][section]["Progress"] < 1:
                self.section = section
                break

        self.window = root
        self.course_title = self.json_index["Course"]
        self.window.set_title("MLG - %s (%s)" % (self.course_title, self.section))
        self.main_queue = Queue(root.root)
        self.directory = directory

        with open('Courses/%s/%s' % (directory, self.json_index["Sections"][self.section]["File"]), 'r') as f:
            self.json_section = json.loads(f.read())

        for question in self.json_section["Queue"]:
            if question not in self.json_save[self.course_title][section]:
                self.json_save[self.course_title][section][question] = self.json_section["Queue"][question]
            for i in range(self.json_save[self.course_title][section][question]):
                new_card = Card(self.main_queue.root)
                new_card.load({question: self.json_section["Questions"][question]})
                self.main_queue.append_card(new_card)

        self.save_manager = SaveManager(self.json_save, self.json_section, self.course_title, self.section)
        self.save_manager.update_save()
        self.main_queue.save_manager = self.save_manager

    def main_loop(self):
        t = time.time()
        delta_t = 0
        last_t = t

        while True:
            self.main_queue.update(delta_t)
            self.window.update()

            t = time.time()
            delta_t = t - last_t
            last_t = t


class Card(tk.Frame):
    def __init__(self, root) -> None:
        super().__init__(root, bg=style.bg_3)
        self.columnconfigure(0, weight=1)

        self.root = root
        self.title = 0
        self.title_text = ""

        self.body = []
        self.input = 0
        self.responses = []
        self.correct_response = []
        self.content = 0
        self.buttons = []
        self.answered = True

        self.colour = copy.copy(style)

        self.t = 0
        self.y = 0

    # Add a banner holding the title to the top of the card
    def add_title(self, title):
        self.title_text = title
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
        self.input = tk.Button(self, text='Ok', font='Corbel 12', relief='flat', bg=self.colour.bg_2,
                               fg=self.colour.txt_1)
        self.input.grid(column=0, sticky='NSEW', pady=2)

    # Add a multi-choice input
    def add_tri_button(self, answers, symbols, correct):
        def create_response(data, symbols):
            eq_tree = EquationsTree()
            eq_tree.build(data)
            eq_tree.insert_symbols(symbols)
            return eq_tree.evaluate()

        self.responses = [create_response(data, symbols) for data in answers]

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
                          fg=self.colour.txt_1, command=(lambda: self.correct(i)) if self.correct_response == i else (
                        lambda: self.incorrect(self.correct_response))))
            self.buttons[-1].grid(row=0, column=i, sticky='NESW', padx=(2 * (i != 0), 2 * (i != 2)))

    def load(self, data):
        self.title = list(data.keys())[0]
        data = data[self.title]

        self.add_title(self.title)
        self.add_content()

        letters = ['u', 'v', 'w', 'p', 'q', 'z']
        symbols = {}

        question = data["Question"]
        for txt in question:
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

        if type(data["Answer"]) == list and len(data["Answer"]) == 3:
            correct = random.randint(0, 2)
            ans = data["Answer"]

            get = ans[0], ans[correct]
            ans[correct], ans[0] = get

            self.add_tri_button(ans, symbols, correct)

    def correct(self, index=None):
        self.queue.pop_card(self.queue.cards.index(self), correct=1)
        if type(index) is not None:
            for i in range(3):
                self.buttons[i].config(fg=style.fg_cor, bg=style.bg_cor)

    def incorrect(self, index=None):
        print(index)
        self.queue.pop_card(self.queue.cards.index(self), correct=0)
        if type(index) is not None:
            for i in range(3):
                self.buttons[i].config(fg=(style.fg_cor if i == index else style.fg_err),
                                       bg=(style.bg_cor if i == index else style.bg_err))

    def animate(self, delta_t):
        def curve(x):
            k = 100
            return k / (1 - x) - k

        self.place(y=self.y + (1 - 2 * self.answered) * curve(self.t), x=80)
        self.t += delta_t
        return self.t >= 1


class Queue(BaseQueue):
    class Buffer(BaseQueue.Buffer):
        def animate(self, delta_t):
            def curve(x):
                x = max(min(x, 1), 0)
                return pow(2, 1 - 5 * x) - 1

            self.config(height=int(self.height * curve(self.t)))
            self.t += delta_t

            return self.t >= 0.2

    def __init__(self, root) -> None:
        self.root = tk.Frame(root, bg=style.bg_3)
        self.save_manager = None

        self.cards = []
        self.animated = []

        self.target = 100
        self.position = 100
        self.length = 0
        self.padx = 80

        self.root.place(x=80, y=self.position)
        self.top_buffer = self.Buffer(self.root, height=200)
        self.top_buffer.grid(row=0, column=0)

        self.bottom_buffer = self.Buffer(self.root, height=1000)
        self.bottom_buffer.grid(row=1000, column=0)

        self.root.bind_all('<MouseWheel>', self.scroll_handler)
        self.root.bind_all('<Button-5>', self.scroll_handler)
        self.root.bind_all('<Button-4>', self.scroll_handler)

        self.root.lower()
        root.lower()

    def pop_card(self, i, correct=1):
        removed = self.cards[i]
        removed.answered = correct

        self.save_manager.update_question(removed.title_text, offset=-correct )
        self.save_manager.update_save()

        self.cards[i] = self.Buffer(self.root, 30 + removed.winfo_height())
        removed.y = removed.winfo_rooty() - self.root.winfo_rooty()
        self.cards[i].grid(row=i + 1, column=0, padx=80)
        removed.lift()
        self.animated.append(self.cards[i])
        self.animated.append(removed)

    def update(self, delta_t):
        super().update(delta_t)
        self.animate(delta_t)

    def animate(self, delta_t):
        for i, card in enumerate(self.animated):
            if card.animate(delta_t):
                if card in self.cards:
                    removed = self.animated.pop(i)
                    index = self.cards.index(removed)
                    self.cards.remove(removed)
                    for k in range(index, len(self.cards)):
                        self.cards[k].grid_forget()
                        self.cards[k].grid(row=k + 1, column=0, pady=15, padx=80)

                    removed.destroy()
                else:
                    self.animated.pop(i).destroy()
                self.root.update()
                self.length = max(700, self.root.winfo_height() - 1100)


class SaveManager:
    def __init__(self, json_save, json_section, course, section):
        self.json_save, self.json_section, self.course, self.section = \
            json_save, json_section, course, section

    def update_question(self, key, value=None, offset=None):
        if type(value) is int:
            self.json_save[self.course][self.section][key] = value
        else:
            self.json_save[self.course][self.section][key] += offset

    def update_save(self):
        self.update_progress()
        with open("data/save.json", "w") as f:
            f.seek(0)
            json.dump(self.json_save, f, indent=4)
            f.truncate()

    def update_progress(self):
        total = sum(list(self.json_section["Queue"].values()))
        progress = sum([self.json_save[self.course][self.section][key] for key in self.json_section["Queue"].keys()])
        self.json_save[self.course][self.section]["Progress"] = (total-progress)/total

if __name__ == "__main__":
    pass
