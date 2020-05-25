from tkinter import *
from pyglet import font
from PIL import Image, ImageTk
from itertools import count, cycle
#from guizero import *
from fileController import Prompts

import time
from threading import Thread

class DisplayControl(Frame):
    def __init__(self, promptList):
        #font.add_file('ProductSans.ttf')
        customFont = ('Helvetica', 27)
        self.window = Tk()
        super().__init__(self.window)
        self.window.attributes('-fullscreen', True)
        self.window.configure(bg='black')

        self.prompt_list = promptList.prompts
        self.prompt_index = 0
        self.frame = Frame(self.window, relief='raised', bg='black')
        self.frame.pack(fill=BOTH, expand=YES)
        self.frame.pack_propagate(False)

        self.label = ImageLabel(self.frame)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.pack()
        self.label.load('background.gif')

        #image = Image.open('background1.png')
        #photo = ImageTk.PhotoImage(image)

        #self.label = Label(self.frame, image=photo)

        center_frame = Frame(self.frame, relief='raised', bg='black')
        center_frame.place(relx=0.5, rely=0.5, width=600, anchor=S)
        self.processing = ImageLabel(center_frame, bg='black')
        self.processing.pack()
        self.processing.load('processing.gif')
        self.label = Label(center_frame, text=self.prompt_list[self.prompt_index], width=500, bg='black', fg='white', font=customFont, wraplength=500)
        #Label(center_frame, text='Education', width=8).pack()
        #self.container = Label(self.window, text=self.prompt_list[self.prompt_index], image=tk_image, compound='center', fg="white", font=("Product Sans Regular", 27))
        self.label.pack()
        #Thread(target = self.playBackgroundAnimation).start()
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

    def updatePrompt(self):
        self.prompt_index = self.prompt_index + 1
        if (self.prompt_index >= len(self.prompt_list)):
            self.prompt_index = 0
        self.label['text'] = self.prompt_list[self.prompt_index]
    
    def updateSpeechDetected(self, detected):
        self.label['text'] = detected
        self.window.update()
        time.sleep(3)
        self.updatePrompt()
        self.window.update()
    
    def hideProcessing(self):
        self.processing.pack_forget()
        self.window.update()
    
    def showProcessing(self):
        self.label.pack_forget()
        self.processing.pack()
        self.label.pack()
        self.window.update()
        
    def showDisplay(self):
        self.window.mainloop()

class ImageLabel(Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)