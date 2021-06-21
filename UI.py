import tkinter as tk
from UI_Styles import DarkTheme
colour=DarkTheme()





class Queue():
    def __init__(self,root):
        #Step 0: Load the gifs
        self.borderImage = tk.PhotoImage("borderImage", file='Testing/Button.gif')
        self.focusBorderImage = tk.PhotoImage("focusBorderImage", file='Testing/Focus.gif')

        self.root=tk.Label(root,image=self.borderImage,width=360,height=1000)
        self.target=100
        self.position=100
        self.length=1000

        self.root.place(x=60,y=self.position)
        self.root.bind_all('<MouseWheel>',self.scroll_handler)
        self.root.lower()
        root.lower()

    def scroll_handler(self,event):
        self.target+=event.delta/10

    def update(self,delta_t):
        self.target+=max((660-self.target-self.length)*delta_t*10,0)
        self.position+=(self.target-self.position)*min(delta_t*5.0,1.0)
        self.root.place(x=60,y=self.position)

    def append_card(self,card):
        pass

    def remove_card(self):
        pass

if __name__=="__main__":
    import main