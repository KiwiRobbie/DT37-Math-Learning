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


# Class for managing the main screen of the game
class Screen:
    def __init__(self, root, directory):
        # Load the index and save json files
        with open('Courses/%s/index.json' % directory, 'r') as f:
            self.json_index = json.loads(f.read())

        with open('data/save.json', 'r') as f:
            self.json_save = json.loads(f.read())

        # Find the first uncompleted section in the course been loaded
        self.section = ""
        for section in self.json_index["Sections"].keys():
            if self.json_save[self.json_index["Course"]][section]["Progress"] < 1:
                self.section = section
                break

        # Save a reference to the root window and update its title
        self.window = root
        self.course_title = self.json_index["Course"]
        self.window.set_title("MLG - %s (%s)" % (self.course_title, self.section))

        # Create new Queue object for the screen
        self.main_queue = Queue(root.root)

        # Save the directory of the course index.json
        self.directory = directory

        # Load the section json by looking up its location in the index file
        with open('Courses/%s/%s' % (self.directory, self.json_index["Sections"][self.section]["File"]), 'r') as f:
            self.json_section = json.loads(f.read())

        # For each question type in the section check if its progress is in the save file
        for question in self.json_section["Queue"]:
            if question not in self.json_save[self.course_title][section]:
                # If the save doesn't contain the remaining number of questions load that number from the sections file
                self.json_save[self.course_title][section][question] = self.json_section["Queue"][question]

            # Then add all remaining cards for the question type
            for i in range(self.json_save[self.course_title][section][question]):
                new_card = Card(self.main_queue.root)
                new_card.load({question: self.json_section["Questions"][question]})
                self.main_queue.append_card(new_card)

        # Create a SaveManager object to handle saving json data and use it to update the save file
        self.save_manager = SaveManager(self.json_save, self.json_section, self.course_title, self.section)
        self.save_manager.update_save()

        # Attach the save manager object to the main queue so it can access it too
        self.main_queue.save_manager = self.save_manager

    # Screens main loop
    def main_loop(self):
        # Initialize timing data
        t = time.time()
        delta_t = 0
        last_t = t

        # TODO: Add an exit condition
        while True:
            # Update the queue and the main window of the program
            self.main_queue.update(delta_t)
            self.window.update()

            # Update the timing information
            t = time.time()
            delta_t = t - last_t
            last_t = t


# Widget class for question cards, inherits from tk.Frame
class Card(tk.Frame):
    def __init__(self, root) -> None:
        # Run __init__ method for the frame and configure self
        super().__init__(root, bg=style.bg_3)
        self.columnconfigure(0, weight=1)

        # Properties of the Card
        self.root = root            # The root widget that the  card is placed in
        self.title_text = ""        # The text in the cards title
        self.title = None           # The widget holding the cards title
        self.content = None         # The widget holding the content of the card
        self.input = None           # The widget holding the input section of the card
        self.responses = []         # List of possible responses for the card
        self.correct_response = 0   # The index of the correct response to the card
        self.body = []              # A list of all widgets inside the card
        self.buttons = []           # A list of all button widgets for answering the question
        self.answered = True        # True: User answered correctly, False: User answered incorrectly
        self.symbols = {}           # Dict mapping each symbol in the question to a letter value pair
        self.t = 0                  # Used for timing animations, time since start of animation
        self.y = 0                  # Y-Coordinate of the card and the start of animation

    # Add a banner holding the title to the top of the card
    def add_title(self, title):
        # Create a frame to hold the title text
        self.body.append(tk.Frame(self, width=320, height=24, bg=style.bg_3))
        self.body[-1].grid(row=0, column=0, sticky='NSEW', pady=2)
        self.body[-1].columnconfigure(0, weight=1)
        self.body[-1].rowconfigure(0, weight=1)
        self.body[-1].grid_propagate(False)

        # Place a label with the title text inside the frame
        self.title = tk.Label(self.body[-1], text=title, fg=style.txt_2, font='Corbel 12 bold', bd=0,
                              bg=style.bg_2)
        self.title.grid(column=0, sticky='NSEW')

    # Adds a frame for holding the content / question of a card
    def add_content(self):
        self.content = tk.Frame(self, width=320, bg=style.bg_2)
        self.content.grid(column=0, sticky='NSEW', pady=2)
        self.content.columnconfigure(0, weight=1)

    # Add a section of text to the cards content section
    def add_text(self, text, font='Corbel 11'):
        self.body.append(tk.Label(self.content, text=text, bg=style.bg_2, fg=style.txt_1, font=font))
        self.body[-1].grid(column=0, sticky='NSEW', pady=4)

    # Add a section of math to the cards content section
    def add_math(self, text, font='Corbel 11'):
        self.body.append(tk.Label(self.content, text=text, bg=style.bg_2, fg=style.txt_1, font=font))
        self.body[-1].grid(column=0, sticky='NSEW', pady=4)

    # Add a single button to accept the card
    def add_single_button(self):
        self.input = tk.Button(self, text='Ok', font='Corbel 12', relief='flat', bg=style.bg_2,
                               fg=style.txt_1)
        self.input.grid(column=0, sticky='NSEW', pady=2)

    # Add a multi-choice input with three options
    def add_tri_button(self, answers, correct):
        # Evaluates equations for each answer
        def create_response(data, data_symbols):
            eq_tree = EquationsTree()              # Create a new tree
            eq_tree.build(data)                    # Build tree from provided data
            eq_tree.insert_symbols(data_symbols)   # Insert the corresponding value for each variable in the equation
            return eq_tree.evaluate()              # Evaluate the tree and return the result

        # Generate responses from the equations for each response
        self.responses = [create_response(data, self.symbols) for data in answers]

        # Save the index of the correct response
        self.correct_response = correct

        # Create and configure a frame to hold the input to the question
        self.input = tk.Frame(self, width=320, height=32, bg=style.bg_3)
        self.input.grid(column=0, sticky='NSEW', pady=2)
        self.input.rowconfigure(0, weight=1)
        self.input.grid_propagate(False)

        # Create a list of button widgets
        self.buttons = []
        for i in range(3):
            # Configure frame holding the button
            self.input.columnconfigure(i, weight=1)

            # Append a new button to the list of buttons for the card. The buttons command is set as either
            # correct or incorrect depending on the current button number and the index of the correct button
            self.buttons.append(
                tk.Button(self.input, text=self.responses[i], relief='flat', bd=0, bg=style.bg_2, fg=style.txt_1,
                          command=(lambda: self.correct(i)) if self.correct_response == i # If this the correct button
                          else (lambda: self.incorrect(self.correct_response))))          # If the button is incorrect

            # Place the new butto with .grid()
            self.buttons[-1].grid(row=0, column=i, sticky='NESW', padx=(2 * (i != 0), 2 * (i != 2)))

    # Create a card from json data
    def load(self, data):
        # Load the cards title from the provided data
        self.title_text = list(data.keys())[0]

        # Extract only the relevant data for the card
        data = data[self.title_text]

        # Add a title and content to the card
        self.add_title(self.title_text)
        self.add_content()

        # List of possible symbols that can be substituted into the question
        letters = ['u', 'v', 'w', 'p', 'q', 'z']

        # Get the question section from the data
        question = data["Question"]

        # For each section in the question
        for txt in question:
            # If the data is text add text to the cards body
            if "<txt>" in txt[0]:
                self.add_text(txt[1])

            # If it is math add math to the cards body
            elif "<math>" in txt[0]:
                # Extract the math section and replace the symbols with their corresponding letters
                math = txt[1]
                for key, value in self.symbols.items():
                    math = math.replace("[%s]" % key, value[0])

                # Insert the center dot character
                math = math.replace("cdot", "•")

                # Add the formatted math to the cards body
                self.add_math(math)

            # If the data is for a definition
            elif "<def>" in txt[0]:
                # Extract the symbol that is been defined and the equation defining it
                symbol = txt[1].split('=')[0].split('[')[1].split(']')[0]
                equation = txt[1].split('=')[1]

                # Update the symbol dict with the new symbol and its value
                self.symbols[symbol] = (letters.pop(random.randrange(0, len(letters))), solve_equation(equation))

                # Add the letter and value as math to the cards body
                self.add_math("%s = %s" % self.symbols[symbol])

        # If the card has three possible answers
        if type(data["Answer"]) == list and len(data["Answer"]) == 3:
            # Pick a location for the correct answer and load the equations for the possible answers
            correct = random.randint(0, 2)
            ans = data["Answer"]

            # Swap the value at the chosen index and the correct answer
            get = ans[0], ans[correct]
            ans[correct], ans[0] = get

            # Add a tri button response type, give it the equation to generate answers and the correct button
            self.add_tri_button(ans, correct)

    # Method to be run if the correct button is clicked
    def correct(self, index=None):
        # Remove the card from the queue using the correct flag
        self.queue.pop_card(self.queue.cards.index(self), correct=1)

        # If the button is multichoice show that the user was right by highlight all buttons green
        if type(index) is not None:
            for i in range(3):
                self.buttons[i].config(fg=style.fg_cor, bg=style.bg_cor)

    # Method to be run if the wrong button is clicked
    def incorrect(self, index=None):
        # Remove the card from the queue using the incorrect flag
        self.queue.pop_card(self.queue.cards.index(self), correct=0)

        # Show the user the correct button by highlighting it green, make other button red
        if type(index) is not None:
            for i in range(3):
                self.buttons[i].config(fg=(style.fg_cor if i == index else style.fg_err),
                                       bg=(style.bg_cor if i == index else style.bg_err))

    # Method to animate the card moving onscreen
    def animate(self, delta_t):
        # Curve relating animation time to offset
        def curve(x):
            k = 100
            return k / (1 - x) - k

        # Place the card offsetting its initial position by the value in the curve
        self.place(y=self.y + (1 - 2 * self.answered) * curve(self.t), x=80)

        # Advance the animations timer
        self.t += delta_t

        # Method returns true once the animation is complete
        return self.t >= 1


# Basic solver for symbol definition equations only containing random numbers
def solve_equation(equation):
    equation = equation.split("$")
    for i, eq in enumerate(equation):
        if "randc" in eq:
            r = int(eq.split("{")[1].split("}")[0])
            equation[i] = (random.randint(-r, r), random.randint(-r, r))
    return Complex(*equation[1])


# Extension of the base queue class
class Queue(BaseQueue):
    # Extension of the base buffer subclass
    class Buffer(BaseQueue.Buffer):
        # Add new method to animate the size of the buffer
        def animate(self, delta_t):
            # Curve for the animation to follow
            def curve(x):
                x = max(min(x, 1), 0)
                return pow(2, 1 - 5 * x) - 1

            # Set the height of the buffer using the curve value at the current time
            # to scale the initial height of the buffer
            self.config(height=int(self.height * curve(self.t)))

            # Advance the timer used for animation
            self.t += delta_t

            # Return the state of the animation:
            return self.t >= 0.2  # False: Running   True: Complete

    # Override the default __init__ of the base queue
    def __init__(self, root) -> None:
        # Create a root widget for the queue
        self.root = tk.Frame(root, bg=style.bg_3)

        # Store a reference to the save manager
        self.save_manager = None

        self.cards = []     # List of cards and buffers in the queue
        self.animated = []  # List of widgets currently been animated

        self.target = 100   # Target position of the queue ( Used for smooth scrolling )
        self.position = 0   # Actual position of the queue ( Used for smooth scrolling )
        self.length = 0     # Length of the queue in pixels ( Limit scrolling past ends of the queue )
        self.padx = 60      # Amount of padding on the sides of the queue

        # Create top and bottom buffers, these extend off the screen in both directions
        # to ensure that the edges of the queue are always hidden, this is particularly important
        # for animated cards as they can't be drawn outside of the queue and would disappear early
        self.top_buffer = self.Buffer(self.root, height=200)
        self.top_buffer.grid(row=0, column=0)

        self.bottom_buffer = self.Buffer(self.root, height=1000)
        self.bottom_buffer.grid(row=1000, column=0)

        # Bind the scroll handler to mouse events for windows and linux
        self.root.bind_all('<MouseWheel>', self.scroll_handler)
        self.root.bind_all('<Button-5>', self.scroll_handler)
        self.root.bind_all('<Button-4>', self.scroll_handler)

        # Place the queue object
        self.root.place(x=0, y=self.position)

        # Ensure everything is drawn in the correct order
        self.root.lower()
        root.lower()

    # Removes cards from the queue
    def pop_card(self, i, correct=1):
        removed = self.cards[i]     # Reference to the card been removed
        removed.answered = correct  # Tell the card if it was answered correctly

        # If the card was correctly answered decrement the number of remaining cards of that format and save progress
        self.save_manager.update_key(removed.title_text, offset=-correct)
        self.save_manager.update_save()

        # Create a buffer in the cards spot, and place it using grid
        self.cards[i] = self.Buffer(self.root, 30 + removed.winfo_height())

        # Save the cards queue relative coordinate after it was removed
        removed.y = removed.winfo_rooty() - self.root.winfo_rooty()

        # Place the buffer using .grid()
        self.cards[i].grid(row=i + 1, column=0, padx=80)

        # Lift the freed card above the other cards in the queue
        removed.lift()

        # Add both the buffer and removed cards to the list of animated widgets
        self.animated.append(self.cards[i])
        self.animated.append(removed)

    # Update method called every frame
    def update(self, delta_t):
        # Call the update method of the base queue class
        super().update(delta_t)

        # Call the animate method
        self.animate(delta_t)

    # Apply animations
    def animate(self, delta_t):
        # Apply to all widgets in the animated list
        for i, widget in enumerate(self.animated):
            # Apply the animation method, if the animation has compleated remove the widget
            if widget.animate(delta_t):
                # If the widget is in the cards list and thus in the queue
                if widget in self.cards:
                    # Remove it from the  list of animated widgets
                    removed = self.animated.pop(i)

                    # Find its index in the cards list
                    index = self.cards.index(removed)

                    # Remove it from the cards list
                    self.cards.remove(removed)

                    # Move the cards after the removed cards down
                    for k in range(index, len(self.cards)):
                        self.cards[k].grid_forget()
                        self.cards[k].grid(row=k + 1, column=0, pady=15, padx=80)

                    # Destroy the removed card
                    removed.destroy()
                else:
                    # If the card isn't part of the queue remove it from the list of animated widgets and destroy it
                    self.animated.pop(i).destroy()

                # Update the queue object so that changes take effect
                self.root.update()

                # Recalculate the length of the queue
                self.length = max(700, self.root.winfo_height() - 1100)

# Class for updating save file and holding various data
class SaveManager:
    # Load json data and course / section keys
    def __init__(self, json_save, json_section, course, section):
        self.json_save, self.json_section, self.course, self.section = \
            json_save, json_section, course, section

    # Update a key for the current section by writing a new value or offsetting an existing one
    def update_key(self, key, value=None, offset=None):
        if type(value) is int:
            self.json_save[self.course][self.section][key] = value
        else:
            self.json_save[self.course][self.section][key] += offset

    # Use the current save data to update the progress key for the current section
    def update_progress(self):
        total = sum(list(self.json_section["Queue"].values()))
        progress = sum([self.json_save[self.course][self.section][key] for key in self.json_section["Queue"].keys()])
        self.json_save[self.course][self.section]["Progress"] = (total-progress)/total

    # Write the save data to a save.json file
    def update_save(self):
        self.update_progress()
        with open("data/save.json", "w") as f:
            f.seek(0)
            json.dump(self.json_save, f, indent=4)
            f.truncate()



