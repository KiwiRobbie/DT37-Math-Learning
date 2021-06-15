import tkinter as tk
from ProgramColours import DarkTheme
from operator import attrgetter

colour=DarkTheme()

# 3 Section button
class TriButton():
    def __init__(self,root):
        self.root=tk.Frame(root,width=360,height=80,bg=colour.fg_1)

# Class for creating question and infomation cards
class Card():
    def __init__(self,root,offset,card_file=0):
        self.root=tk.Frame(root,bg=colour.bg_2,width=360,height=320)
        self.buttons=TriButton(self.root)
        self.buttons.root.place(y=280,x=0)
        self.offset=offset

    def update(self,queue_scroll):
        self.root.place(x=0,y=queue_scroll+self.offset)

class Queue():
    def __init__(self) -> None:
        self.spacing=20
        self.cards=[]

    def append_card(self,card):
        self.cards.append(card)
        offset=len(self.cards-1)*self.spacing+sum( [ c.offset for c in self.cards[:-1] ] )

    def remove_card(self):
        pass

#Run the main script if we try to run the this file instead
if(__name__=='__main__'):
    import main 