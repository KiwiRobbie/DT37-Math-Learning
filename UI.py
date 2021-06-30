import tkinter as tk
from UI_Styles import DarkTheme

colour = DarkTheme()


class ConfigureCard:
    def __init__(self) -> None:
        pass


class Card(tk.Frame):
    def __init__(self, root, card_config) -> None:
        super().__init__(root, bg=colour.bg_3)
        self.config = card_config
        self.columnconfigure(0, weight=1)

        # Card title
        self.title_frame = tk.Frame(self, width=320, height=16, bg=colour.bg_3)
        self.title_frame.grid(row=0, column=0, sticky='NSEW', pady=2)
        self.title_frame.columnconfigure(0, weight=1)
        self.title_frame.rowconfigure(0, weight=1)
        self.title_frame.grid_propagate(False)
 
        self.title = tk.Label(self.title_frame, text='Complex Numbers', fg=colour.txt_2, font='Corbel 12 bold', bd=0,
                              bg=colour.bg_2)
        self.title.grid(row=0, column=0, sticky='NSEW')

        # Question
        self.body = tk.Frame(self, width=320, height=100, bg=colour.bg_2)
        self.body.grid(row=1, column=0, sticky='NSEW', pady=2)

        # Button
        if self.config.button == 'single':
            self.single_button()
        elif self.config.button == 'tri':
            self.tri_button()

    def enter(self, event):
        pass

    def exit(self, event):
        pass

    def single_button(self):
        self.button = tk.Button(self, text='Ok', font='Corbel 12', relief='flat', bg=colour.bg_2, fg=colour.txt_1)
        self.button.grid(row=2, column=0, sticky='NSEW', pady=2)

    def tri_button(self):
        self.button_frame = tk.Frame(self, width=320, height=32, bg=colour.bg_3)
        self.button_frame.grid(row=2, column=0, sticky='NSEW', pady=2)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.grid_propagate(False)

        self.buttons = []
        for i in range(3):
            self.button_frame.columnconfigure(i, weight=1)
            self.buttons.append(
                tk.Button(self.button_frame, text=self.config.answer[i], relief='flat', bd=0, bg=colour.bg_2,
                          fg=colour.txt_1,command=self.correct if self.config.correct==i else self.incorrect))
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

    def append_card(self, card_config):
        self.cards.append(Card(self.root, card_config))
        self.cards[-1].grid(row=len(self.cards) - 1, column=0, pady=15)
        self.root.update()
        self.length = max(600, self.root.winfo_height())

    def remove_card(self):
        pass


if __name__ == "__main__":
    import main
