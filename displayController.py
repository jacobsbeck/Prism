#from tkinter import *
import PIL
#from itertools import count, cycle
from guizero import *

class DisplayControl():
    def __init__(self, promptList):
        self.window = App(title="Prism", bg=(0,0,0))
        self.window.full_screen = True
        
        self.prompt_list = promptList.prompts
        self.prompt_index = 0
        
        self.prompt_text = Text(self.window, text=self.prompt_list[self.prompt_index], size= 40, color="white")
        self.gif_contain = Picture(self.window, image="gif.gif")
        self.speech_text = Text(self.window, text="Speech", size= 40, color="white")

        #self.prompt = Label(self.master, text="Prompts", bg="white")
        #self.prompt.place(x=20, y=20)
        #self.speech = Label(self.master, text="Speech", bg="white")
        #self.speech.place(x=20, y=100)
        #self.pack()
        #self.master.mainloop()
    
    def updatePrompt(self):
        self.prompt_text.text = self.prompt_list[self.prompt_index]
    
    def updateSpeechDetected(self, detected):
        self.speech_text.text = detected
        self.updatePrompt()
        self.showDisplay()
    
    def showDisplay(self):
        self.window.display()
