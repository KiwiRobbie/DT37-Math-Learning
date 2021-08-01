# Modular Queue System for holding card lists
import tkinter as tk

from UI_Styles import DarkTheme

style = DarkTheme()


class Queue:
    # Invisible buffer card that can be used to extend the queue
    class Buffer(tk.Frame):
        # Override the default __init__ method of the tk.Frame
        def __init__(self, root, height):
            # Call the __init__ method of tk.Frame setting custom parameters
            super().__init__(root, width=320, height=height, bg=style.bg_3)

            # Properties of the class used when the class is extended
            self.height = height
            self.t = -0.5

    # Creates a new queue in the specified root widget
    def __init__(self, root) -> None:
        # Root widget to contain all elements of the queue
        self.root = tk.Frame(root, bg=style.bg_3)

        # List of cards in the queue
        self.cards = []

        # Properties of the queue
        self.target = 0    # Target position of the queue ( Used for smooth scrolling )
        self.position = 0  # Actual position of the queue ( Used for smooth scrolling )
        self.length = 0      # Length of the queue in pixels ( Limit scrolling past ends of the queue )
        self.padx = 60       # Amount of padding on the sides of the queue
        self.offset = 0

        # Create top and bottom buffers, these extend off the screen in both directions
        # These ensure that the edges of the queue are always hidden
        self.top_buffer = self.Buffer(self.root, height=200)
        self.top_buffer.grid(row=0, column=0)

        self.bottom_buffer = self.Buffer(self.root, height=1000)
        self.bottom_buffer.grid(row=1000, column=0)

        # Add bindings to handle scrolling for windows:
        self.root.bind_all('<MouseWheel>', self.scroll_handler)

        # Add bindings to handle scrolling for linux:
        self.root.bind_all('<Button-5>', self.scroll_handler)
        self.root.bind_all('<Button-4>', self.scroll_handler)

    # Function to handle scroll events for both windows and linux
    def scroll_handler(self, event):
        # For both OS the target position of the queue is moved by the amount scrolled

        # Linux sends and event every time the scroll wheel moves
        # Different events are different directions
        # ( Windows won't send these events )
        if event.num == 5:
            self.target -= 45
        elif event.num == 4:
            self.target += 45

        # Windows sends multiple scroll events at the same time, the distance scrolled is event.delta
        # event.delta is zero in when using linux
        self.target += event.delta / 2

    # Append a new card widget to the queue
    def append_card(self, card):
        # Add a reference to the queue in the card
        card.queue = self

        # Append the card to the list of cards in the queue
        self.cards.append(card)

        # Place the card in the queue root
        self.cards[-1].grid(row=len(self.cards), column=0, pady=15, padx=self.padx)

    def regrid(self):
        self.top_buffer.grid(row=0,column=0)
        self.bottom_buffer.grid(row=1000, column=0)
        for i, card in enumerate(self.cards):
            card.grid(row=i+1, column=0, pady=15, padx=self.padx)

    # Update the queue, all animations are scaled by the amount of time frames are taking
    def update(self, delta_t):
        # Find the length of the cards in the queue ( Ignoring buffers )
        # Clamp the length so that it is not less that the screen length
        self.length = max(700, self.root.winfo_height() + self.offset - self.bottom_buffer.winfo_height() - self.top_buffer.winfo_height())

        # Smoothly clamp the target position by moving it back if it is above or below the screen
        self.target += max((700 - self.target - self.length) * delta_t * 10, 0)
        self.target += min((- self.target) * delta_t * 10, 0)

        # Offset the current position of the queue so that it move toward the target position
        self.position += (self.target - self.position) * min(delta_t * 5.0, 1.0)

        # Update the position of the widget
        self.root.place(x=0, y=self.position + self.offset - self.top_buffer.winfo_height())
