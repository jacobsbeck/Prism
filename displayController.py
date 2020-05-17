from tkinter import *
from PIL import Image, ImageTk
from itertools import count, cycle

class DisplayControl(Frame):
    def __init__(self, promptList):
        self.master = Tk()
        super().__init__(self.master)
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg='black')

        self.gif_container = ImageLabel(self.master)
        self.gif_container.pack()
        self.gif_container.load('gif.gif')
        self.prompt_list = promptList
        self.prompt_index = 0
        self.prompt = Label(self.master, text="Prompts", bg="white")
        self.prompt.place(x=20, y=20)
        self.speech = Label(self.master, text="Speech", bg="white")
        self.speech.place(x=20, y=100)
        self.pack()
        self.master.mainloop()
    
    def updatePrompt(self):
        self.prompt["text"] = self.prompt_list[self.prompt_index]
    
    def updateSpeechDetected(self, detected):
        self.speech["text"] = detected
        self.updatePrompt()
        

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
