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
        self.background_container = Picture(self.window, image="background.gif", height=1280, width=720)
        self.prompt_text = Text(self.window, text=self.prompt_list[self.prompt_index], size= 40, color="white")
        self.speech_text = Text(self.window, text="Speech", size= 40, color="white")
        self.recording_symbol = Picture(self.window, image="processing.gif", height=50, width=50)
    
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
