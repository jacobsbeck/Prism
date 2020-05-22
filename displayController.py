from tkinter import *
from PIL import Image, ImageTk
from itertools import count, cycle
#from guizero import *
from fileController import Prompts

import time
from threading import Thread

class DisplayControl(Frame):
    def __init__(self, promptList):
        self.window = Tk()
        super().__init__(self.window)
        self.window.attributes('-fullscreen', True)
        self.window.configure(bg='black')

        self.prompt_list = promptList.prompts
        self.prompt_index = 0

        Thread(target = self.playBackgroundAnimation).start()
        """
        self.window = App(title="Prism", bg=(0,0,0))
        self.window.full_screen = True
        
        self.prompt_list = promptList.prompts
        self.prompt_index = 0
        self.container = Drawing(self.window, height="fill", width="fill")
        Thread(target = self.playBackgroundAnimation).start()
        self.container.text(x=0, y=0, text=self.prompt_list[self.prompt_index], color="white")
        #self.prompt_text = Text(self.window, text=self.prompt_list[self.prompt_index], size= 40, color="white")
        #self.speech_text = Text(self.window, text="Speech", size= 40, color="white")
        #self.recording_symbol = Picture(self.window, image="processing.gif", height=50, width=50)
        """

    def playBackgroundAnimation(self):
        curBackground = 0
        while True:
            
            if (curBackground == 3):
                curBackground = 0
            if (curBackground == 0):
                image = Image.open('background1.png')
            elif (curBackground == 1):
                image = Image.open('background2.png')
            else:
                image = Image.open('background3.png')

            tk_image = ImageTk.PhotoImage(image)
            self.container = Label(self.window, text=self.prompt_list[self.prompt_index], image=tk_image, compound='center', fg="white", font=("Product Sans Regular", 27))
            self.container.pack()
            self.window.update()
            curBackground = curBackground + 1
            time.sleep(0.5)

    def updatePrompt(self):
        self.prompt_index = self.prompt_index + 1
        if (self.prompt_index >= len(self.prompt_list)):
            self.prompt_index = 0
        self.prompt_text.value = self.prompt_list[self.prompt_index]
    
    def updateSpeechDetected(self, detected):
        self.speech_text.value = detected
        self.updatePrompt()
        self.window.update()
    
    def showRecording(self):
        self.recording_symbol.image = "recording.png"
        self.window.update()
    
    def showProcessing(self):
        self.recording_symbol.image = "processing.gif"
        self.window.update()
        
    def showDisplay(self):
        self.window.display()

prompts = Prompts("prompts.txt")
app = DisplayControl(prompts)
app.window.mainloop()