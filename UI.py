import tkinter as tk
from tkinterhtml import HtmlFrame
import urllib.request

from UI_Styles import DarkTheme
colour=DarkTheme()


class Card(tk.Frame):
    def __init__(self,root,card_config) -> None:
        super().__init__(root,bg='white',width=360,height=300)


        # self.cap=tk.PhotoImage('cap',file='Testing/Neo-Cap.gif')
        # button=tk.Label(self,image=self.cap,text='Complex Numbers', compound='center',fg='#ff7b2e',font='Corbel 12',bd=0,bg=colour.bg_3,pady=-1,padx=-1)
        # button.grid(row=0,column=0)


        # self.q_image=tk.PhotoImage('question',file='assets/download.png')
        # image=tk.Label(self,image=self.q_image,bd=0,bg=colour.bg_3)
        # image.grid(row=1,column=0)



        # self.buttons=tk.PhotoImage('singleButton',file='Testing/Neo-Wide.gif')
        # button=tk.Label(self,image=self.buttons,bd=0,bg=colour.bg_3)
        # button.grid(row=2,column=0)




    def single_button(self):
        pass

    def tri_button(self):
        pass

class Queue():
    def __init__(self,root) -> None:

        self.root=tk.Frame(root,bg=colour.bg_3)
        self.cards=[]

        self.target=100
        self.position=100
        self.length=0


        self.root.place(x=60,y=self.position)
        
        self.root.bind_all('<MouseWheel>',self.scroll_handler)
        self.root.lower()
        root.lower()
 
    def scroll_handler(self,event):
        self.target+=event.delta/2

    def update(self,delta_t):
        self.target+=max((660-self.target-self.length)*delta_t*10,0)
        self.target+=min((60-self.target)*delta_t*10,0)


        self.position+=(self.target-self.position)*min(delta_t*5.0,1.0)
        self.root.place(x=60,y=self.position)


    def append_card(self,card_config):
        self.cards.append(Card(self.root,card_config))
        self.cards[-1].grid(row=len(self.cards)-1,column=0,pady=15)
        self.root.update()
        self.length=max(600,self.root.winfo_height())


    def remove_card(self):
        pass

if __name__=="__main__":
    import main