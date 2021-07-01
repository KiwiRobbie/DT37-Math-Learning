import tkinter as tk
from UI_Styles import DarkTheme

colour = DarkTheme()

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

    # Add a banner holding the title to the top of the card
    def add_title(self,title):
        self.title_frame = tk.Frame(self, width=360, height=24, bg=colour.bg_3)
        self.title_frame.grid(row=0, column=0, sticky='NSEW', pady=2)
        self.title_frame.columnconfigure(0, weight=1)
        self.title_frame.rowconfigure(0, weight=1)
        self.title_frame.grid_propagate(False)

        self.title = tk.Label(self.title_frame, text=title, fg=colour.txt_2, font='Corbel 12 bold', bd=0,
                              bg=colour.bg_2)
        self.title.grid(column=0, sticky='NSEW')

    def add_content(self):
        self.content = tk.Frame(self, width=320, bg=colour.bg_2)
        self.content.grid(column=0, sticky='NSEW', pady=2)
        self.content.columnconfigure(0,weight=1)

    # Add a section of text to the card
    def add_text(self,text,font='Corbel 11'):
        self.body.append(tk.Label(self.content,text=text,bg=colour.bg_2,fg=colour.txt_1, font=font))
        self.body[-1].grid(column=0, sticky='NSEW',pady=4)

    # Add a single button to accept the card
    def add_single_button(self):
        self.input = tk.Button(self, text='Ok', font='Corbel 12', relief='flat', bg=colour.bg_2, fg=colour.txt_1)
        self.input.grid(column=0, sticky='NSEW', pady=2)

    # Add a multichoice input
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
        self.root.lower()
        root.lower()

    def scroll_handler(self, event):
        self.target += event.delta / 2

    def update(self, delta_t):
        self.target += max((660 - self.target - self.length) * delta_t * 10, 0)
        self.target += min((60 - self.target) * delta_t * 10, 0)

        self.position += (self.target - self.position) * min(delta_t * 5.0, 1.0)
        self.root.place(x=60, y=self.position)

    def append_card(self,card):
        self.cards.append(card)
        self.cards[-1].grid(row=len(self.cards) - 1, column=0, pady=15)
        self.root.update()
        self.length = max(600, self.root.winfo_height())

    def remove_card(self):
        pass


if __name__ == "__main__":
    import main
