# Screen for selecting a course and viewing current progress
import json
import os
import time
import tkinter as tk

from Queue import Queue
from UI_Styles import DarkTheme

# Use the DarkTheme
style = DarkTheme()


# Class for handling module screen
class Screen:
    def __init__(self, root):
        # Boolean contains state of the program for exiting main loop
        self.running = True

        # Store a reference to the programs main window
        self.window = root
        self.window .set_title("MLG - Course Menu")

        # Create a root frame to hold all elements in the screen
        self.root = tk.Frame(root, bg=style.bg_3, width=480, height=700)
        self.root.grid_propagate(False)
        self.root.columnconfigure(0, weight=1)

        # Place root below the title bar of the window and lift it to the top of the stack
        self.root.place(x=0, y=20)
        self.root.lift()

        # Create a new queue scrollable queue to hold the courses
        self.main_queue = Queue(self.root)

        # List of widgets containing available courses
        self.courses = []

        # The name of the selected course
        self.course = ''

        # Open the save file in write mode creating a new file or leaving an exiting one unmodified
        if not os.path.isfile("data/save.json"):
            with open("data/save.json", 'w') as f:
                pass

        # Open the save file in read/write mode
        with open("data/save.json", 'r+') as f:
            # Read the json data in the file loading using json module, if no data load empty json instead
            data = f.read()
            data = "{\n}" if not data else data
            self.save_json = json.loads(data)

            # For each item in the course directory if item is a directory
            for folder in os.listdir("Courses"):
                if os.path.isdir("Courses/%s" % folder):
                    # Create a new course widget and add it to the main queue, pass references to the save json file
                    self.courses.append(
                        CourseWidget(self.main_queue.root, folder, self.save_json, self.return_course))
                    self.main_queue.append_card(self.courses[-1])

            # After course have loaded write the new save file to disk
            f.seek(0)
            json.dump(self.save_json, f, indent=4)
            f.truncate()

    # Main loop for the screen
    def main_loop(self):
        # Timing data for loop, used ensure animations play at the same speed even with different frame rates
        delta_t = 0
        last_t = time.time()

        while self.running:
            # Call the update method for the screen and then update the window
            self.update(delta_t)
            self.window.update()

            # Update timing information
            t = time.time()
            delta_t = t - last_t
            last_t = t

        # Once loop exits return the users selected course
        return self.course

    # Update method for screen: Update the queue containing the courses
    def update(self, delta_t):
        self.main_queue.update(delta_t)

    # Method to exit menu screen
    def return_course(self, course):
        # Set selected course
        self.course = course

        # Tell main loop to stop running and destroy the screens widgets
        self.running = False
        self.root.destroy()


# Class for creating a progress bar widget from a 0-1 float value, based on tk.Frame
class ProgressBar(tk.Frame):
    def __init__(self, root, progress):
        super().__init__(root)

        self.columnconfigure(0, weight=int(progress * 360))
        self.columnconfigure(1, weight=int((1 - progress) * 360))
        self.grid_propagate(False)

        if progress > 0:
            self.compleated = tk.Frame(self, bg=style.bg_cor, height=2)
            self.compleated.grid(row=0, column=0, sticky="NSEW")
        if progress < 1:
            self.remaining = tk.Frame(self, bg=style.bg_err, height=2)
            self.remaining.grid(row=0, column=1, sticky="NSEW")


# Extension of the tk.Frame class
# Widget class to be placed in course queue and display information about course
class CourseWidget(tk.Frame):
    # Class for displaying information about a subsection of a course, extension of tk.Frame
    class Section(tk.Frame):
        # Override the default __init__ method of the tk.Frame class
        def __init__(self, root, title="", description="", save_json=[], blank=False):
            # Run the old __init__ method and then configure the frame
            super().__init__(root, bg=style.bg_2)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            # If the section has not been created as a blank placeholder
            if not blank:

                # Create title and description labels inside the frame
                self.title = tk.Label(self, text=title, bg=style.bg_2, font=style.font_text, fg=style.txt_1,
                                      justify="center", wraplength=160)
                self.description = tk.Label(self, text=description, bg=style.bg_2, font=style.font_text, fg=style.txt_2,
                                            justify="center", wraplength=160)

                # Place the title and description labels using grid method
                self.title.grid(row=0, column=0, sticky="N")
                self.description.grid(row=1, column=0, sticky="N")

                # If save data for the section isn't in the save file create a new key to store progress
                # The save json has been passed by reference so changes made here will affect Screen.save_json
                if title not in save_json or type(save_json[title]) != type({}):
                    save_json[title] = {"Progress": 0}

                # Create a progress bar using the progress in the save data and place it in the frame with grid()
                self.progress = save_json[title]["Progress"]
                self.progress_bar = ProgressBar(self, self.progress)
                self.progress_bar.grid(row=2, column=0, sticky="NSEW")

    # Override the default __init__  method for tk.Frame
    def __init__(self, root, index_directory, save_json, return_course):
        # Call the default __init__ to make self a tk.Frame and configure the frame
        super().__init__(root, bg=style.bg_3, width=360)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Save the directory of the json index
        self.directory = index_directory

        # Load the index json file
        with open("Courses/%s/index.json" % index_directory, 'r') as f:
            # Read data from index.json about the course
            self.json = json.loads(f.read())
            self.title = self.json["Course"]
            self.section_titles = []
            self.section_descriptions = []

            # Read data about the sections in the course
            for section in self.json["Sections"]:
                self.section_titles.append(section)
                self.section_descriptions.append(self.json["Sections"][self.section_titles[-1]]["Description"])

        # Create and configure a frame to hold the title label
        self.title_frame = tk.Frame(self, bg=style.bg_2, width=360, height=40)
        self.title_frame.grid(row=0, column=0, sticky='NEW', pady=2, columnspan=2)
        self.title_frame.grid_propagate(False)
        self.title_frame.rowconfigure(0, weight=1)
        self.title_frame.columnconfigure(0, weight=1)

        # Create and place a title label inside its frame
        self.title_label = tk.Label(self.title_frame, text=self.title, bg=style.bg_2, fg=style.txt_1,
                                    font=style.font_title)
        self.title_label.grid(row=0, column=0, sticky="NSEW", pady=4)

        # Load the save json specific to the course if it exists
        if self.title in save_json:
            course_save_json = save_json[self.title]
        else:
            course_save_json = {}

        # Create a list to hold the sections in the course
        self.sections = []

        # Users overall progress through the course
        self.overall_progress = 0

        # Loop over each title and description in the index file
        for i, section in enumerate(zip(self.section_titles, self.section_descriptions)):
            # Append a new section widget to the course
            self.sections.append(self.Section(self, section[0], section[1], course_save_json))

            # Place the new widget using .grid() creating a 2 column list
            self.sections[-1].grid(row=(i // 2) + 1, column=i % 2, sticky='NSEW', pady=2,
                                   padx=(2 * (i % 2), 2 * (1 - i % 2)))

            # Update overall progress for the course using the progress in the new section
            self.overall_progress += self.sections[-1].progress/len(self.section_titles)

        # If an odd number of sections were added to the section list
        if len(self.sections)%2:
            # Find the index of the new section to be added
            i=len(self.section_titles)

            # Using the index place the section in the 2 column list to remove the gap in the right column
            self.sections.append(self.Section(self, blank = True))
            self.sections[-1].grid(row=(i // 2) + 1, column=i % 2, sticky='NSEW', pady=2,
                                   padx=(2 * (i % 2), 2 * (1 - i % 2)))

        # Create a frame for holding the resume / begin button
        self.button_frame = tk.Frame(self, bg=style.bg_2, height=30)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.grid_propagate(False)
        self.button_frame.grid(column=0, sticky="NSEW", columnspan=2, pady=2)

        # Add a button to the button frame, use begin or resume based on progress and a method to end the screen
        # and return the course of the course widget that the button was added to
        self.button = tk.Button(self.button_frame,
                                text="Resume Section" if self.overall_progress > 0 else "Begin Section", bg=style.bg_2,
                                fg=style.txt_1, font=style.font_button, bd=0,
                                command=lambda: return_course(self.directory))
        self.button.grid(row=0, column=0, sticky="NSEW")

        # Update the save_json for the course
        save_json[self.title] = course_save_json
