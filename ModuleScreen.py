import os, json, tkinter as tk
from UI_Styles import DarkTheme
from Queue import  Queue

style = DarkTheme()

class Screen:
    def __init__(self, root):
        root.set_title("MLG - Course Menu")
        self.running = True
        self.root = tk.Frame(root, bg=style.bg_3, width=480,height=700)
        self.root.grid_propagate(False)
        self.root.columnconfigure(0, weight=1)


        self.root.place(x=0,y=20)
        self.root.lift()

        self.courses = []
        self.main_queue = Queue(self.root)

        for folder in os.listdir("Courses"):
            if os.path.isdir("Courses/%s"%folder):
                self.root.rowconfigure(len(self.courses), weight=1)
                self.courses.append( CourseWidget(self.main_queue.root,"Courses/%s/index.json"%folder) )
                self.main_queue.append_card(self.courses[-1])

    def update(self, delta_t):
        self.main_queue.update(delta_t)

    def destroy(self):
        self.root.destroy()

class ProgressBar(tk.Frame):
    def __init__(self,root, progress):
        super().__init__(root)

        self.columnconfigure(0,weight=int(progress*360))
        self.columnconfigure(1,weight=int((1-progress)*360))
        self.grid_propagate(False)


        if progress > 0:
            self.compleated = tk.Frame(self,bg=style.bg_cor, height=2)
            self.compleated.grid(row=0, column=0, sticky="NSEW")
        if progress < 1:
            self.remaining  = tk.Frame(self,bg=style.bg_err, height=2)
            self.remaining.grid(row=0, column=1, sticky="NSEW")




class CourseWidget(tk.Frame):
    class Section(tk.Frame):
        def __init__(self, root, title, description):
            super().__init__(root, bg=style.bg_2)
            self.columnconfigure(0, weight=1)

            self.title = tk.Label(self,text=title, bg=style.bg_2, font=style.font_text, fg=style.txt_1, justify  = "center",wraplength= 160 )
            self.description = tk.Label(self,text=description, bg=style.bg_2, font=style.font_text, fg=style.txt_2, justify  = "center",wraplength=160 )
            self.title.grid(row=0,column=0)
            self.description.grid(row=1,column=0)

            self.progress = ProgressBar(self,0.0)
            self.progress.grid(row=2,column=0,sticky="NSEW")

    def __init__(self, root, index_file):
        super().__init__(root, bg=style.bg_3, width=360)

        with open(index_file, 'r') as f:
            self.json = json.loads(f.read())
            self.title = self.json["Course"]
            self.section_titles = []
            self.section_descriptions = []

            for section in self.json["Sections"]:
                self.section_titles.append(section["Title"])
                self.section_descriptions.append(section["Description"])

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)


        self.title_frame = tk.Frame(self, bg=style.bg_2, width=360, height=40)
        self.title_frame.grid(row=0,column=0, sticky='NEW', pady=2, columnspan=2)
        self.title_frame.grid_propagate(False)



        self.title_frame.rowconfigure(0,weight=1)
        self.title_frame.columnconfigure(0,weight=1)

        self.title_label = tk.Label(self.title_frame, text=self.title, bg=style.bg_2, fg=style.txt_1, font=style.font_title)
        self.title_label.grid(row=0,column=0,sticky="NSEW", pady=4)

        self.sections = []
        for i, section in enumerate(zip(self.section_titles,self.section_descriptions)):
            self.sections.append(self.Section(self,section[0],section[1]))
            self.sections[-1].grid(row=(i//2)+1, column=i%2, sticky='NSEW', pady=2, padx=( 2*(i%2) ,2*(1-i%2) ) )
