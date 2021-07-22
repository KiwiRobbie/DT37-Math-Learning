import json
import os
import time
import tkinter as tk

from Queue import Queue
from UI_Styles import DarkTheme

style = DarkTheme()


class Screen:
    def __init__(self, root):
        root.set_title("MLG - Course Menu")
        self.running = True
        self.root = tk.Frame(root, bg=style.bg_3, width=480, height=700)
        self.root.grid_propagate(False)
        self.root.columnconfigure(0, weight=1)
        self.window = root

        self.root.place(x=0, y=20)
        self.root.lift()

        self.courses = []
        self.main_queue = Queue(self.root)
        self.course = ''

        if not os.path.isfile("data/save.json"):
            with open("data/save.json", 'w') as f:
                pass

        with open("data/save.json", 'r+') as f:
            data = f.read()
            data = "{\n}" if not data else data
            self.save_json = json.loads(data)

            for folder in os.listdir("Courses"):
                if os.path.isdir("Courses/%s" % folder):
                    self.root.rowconfigure(len(self.courses), weight=1)
                    self.courses.append(
                        CourseWidget(self.main_queue.root, folder, self.save_json, self.return_course))
                    self.main_queue.append_card(self.courses[-1])

            f.seek(0)
            json.dump(self.save_json, f, indent=4)
            f.truncate()

    def main_loop(self):
        delta_t = 0
        last_t = time.time()

        while self.running:
            self.update(delta_t)
            self.window.update()

            t = time.time()
            delta_t = t - last_t
            last_t = t

        return self.course

    def update(self, delta_t):
        self.main_queue.update(delta_t)

    def return_course(self, course):
        self.running = False
        self.course = course
        self.root.destroy()


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


class CourseWidget(tk.Frame):
    class Section(tk.Frame):
        def __init__(self, root, title="", description="", save_json=[], blank=False):
            super().__init__(root, bg=style.bg_2)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            if blank:
                pass
            else:
                self.title = tk.Label(self, text=title, bg=style.bg_2, font=style.font_text, fg=style.txt_1,
                                      justify="center", wraplength=160)
                self.description = tk.Label(self, text=description, bg=style.bg_2, font=style.font_text, fg=style.txt_2,
                                            justify="center", wraplength=160)
                self.title.grid(row=0, column=0, sticky="N")
                self.description.grid(row=1, column=0, sticky="N")

                if title not in save_json or type(save_json[title]) != type({}):
                    save_json[title] = {"Progress": 0}

                self.progress = save_json[title]["Progress"]
                self.progress_bar = ProgressBar(self, self.progress)
                self.progress_bar.grid(row=2, column=0, sticky="NSEW")

    def __init__(self, root, index_directory, save_json, return_course):
        super().__init__(root, bg=style.bg_3, width=360)

        self.directory = index_directory
        with open("Courses/%s/index.json" % index_directory, 'r') as f:

            self.json = json.loads(f.read())
            self.title = self.json["Course"]
            self.section_titles = []
            self.section_descriptions = []

            for section in self.json["Sections"]:
                self.section_titles.append(section)
                self.section_descriptions.append(self.json["Sections"][self.section_titles[-1]]["Description"])

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.title_frame = tk.Frame(self, bg=style.bg_2, width=360, height=40)
        self.title_frame.grid(row=0, column=0, sticky='NEW', pady=2, columnspan=2)
        self.title_frame.grid_propagate(False)

        self.title_frame.rowconfigure(0, weight=1)
        self.title_frame.columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.title_frame, text=self.title, bg=style.bg_2, fg=style.txt_1,
                                    font=style.font_title)
        self.title_label.grid(row=0, column=0, sticky="NSEW", pady=4)

        if self.title in save_json:
            course_save_json = save_json[self.title]
        else:
            course_save_json = {}

        self.sections = []
        self.overall_progress = 0
        for i, section in enumerate(zip(self.section_titles, self.section_descriptions)):
            self.sections.append(self.Section(self, section[0], section[1], course_save_json))
            self.sections[-1].grid(row=(i // 2) + 1, column=i % 2, sticky='NSEW', pady=2,
                                   padx=(2 * (i % 2), 2 * (1 - i % 2)))
            self.overall_progress += self.sections[-1].progress

        if len(self.sections)%2:
            i=len(self.section_titles)
            self.sections.append(self.Section(self, blank = True))
            self.sections[-1].grid(row=(i // 2) + 1, column=i % 2, sticky='NSEW', pady=2,
                                   padx=(2 * (i % 2), 2 * (1 - i % 2)))

        self.button_frame = tk.Frame(self, bg=style.bg_2, height=30)
        self.button_frame.grid(column=0, sticky="NSEW", columnspan=2, pady=2)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.grid_propagate(False)

        self.button = tk.Button(self.button_frame,
                                text="Resume Section" if self.overall_progress > 0 else "Begin Section", bg=style.bg_2,
                                fg=style.txt_1, font=style.font_button, bd=0,
                                command=lambda: return_course(self.directory))
        self.button.grid(row=0, column=0, sticky="NSEW")
        save_json[self.title] = course_save_json
