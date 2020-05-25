import speech_recognition as sr
from enum import Enum
from speech_recognition import Microphone
from threading import Thread

class Recognizers(Enum):
    Sphinx=1
    Google=2
    Google_Cloud=3
    Bing=4
    Ibm=5

class Features(Enum):
    Brighter=1
    Dimmer=2
    Off=3
    On=4
    Hue=5
    Tint=6
    Saturation=7
    Shade=8
    Primary=9
    Secondary=10
    Tertiary=11
    Temperature=12
    Contrast=13
    Tones=14

class SpeechControl:

    # A speech control takes a minimum of a light control object, coded libary of words, a 
    # library of colors, and the name of your installed recognizer. By default this 
    # class uses the google recognizer and your default microphone. 
    def __init__(self, light_control, codedWords, codedColors, recognizer_name, display=None, threshold=300, dynamic_threshold=False, mic_name=None):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = threshold
        self.recognizer.dynamic_energy_threshold = dynamic_threshold
        self.display = display

        if recognizer_name == "sphinx":
            self.recognizer_name = Recognizers.Sphinx
        elif recognizer_name == "bing":
            self.recognizer_name = Recognizers.Bing
        elif recognizer_name == "ibm":
            self.recognizer_name = Recognizers.Ibm
        elif recognizer_name == "google_cloud":
            self.recognizer_name = Recognizers.Google_Cloud
        elif recognizer_name == "google":
            self.recognizer_name = Recognizers.Google
        

        if not mic_name == None:
            for i, microphone_name in enumerate(Microphone.list_microphone_names()):
                if microphone_name == mic_name:
                    self.mic = Microphone(device_index=i, sample_rate=44100, chunk_size=4096)
        else:
            self.mic = Microphone(sample_rate=44100, chunk_size=4096)

        self.lights = light_control
        self.codedLibrary = codedWords
        self.colorLibrary = codedColors
    
    def __str__(self):
        return "Microphone: {}\nSpeech Library: {}\nEnergy Threshold: {}\nDynamic Threshold: {}\n Word Library Length: {}\n{}\n".format(self.mic.microphone_name, self.recognizer_name, self.recognizer.threshold, self.recognizer.dynamic_threshold, len(self.codedLibrary), self.lights)

    # This method begins a continous audio stream using the Speech Recognition package and the speech recgonizer of your choice.
    def createContinuousStream(self):
        while True:
            try:
                with self.mic as source:
                    #self.recognizer.adjust_for_ambient_noise(source)
                    self.recognizer.adjust_for_ambient_noise(source)
                    self.display.hideProcessing()
                    audio = self.recognizer.record(source, 3)
                    self.display.showProcessing()
                if self.recognizer_name == Recognizers.Sphinx:
                    cur_str = self.recognizer.recognize_sphinx(audio)
                elif self.recognizer_name == Recognizers.Bing:
                    cur_str = self.recognizer.recognize_bing(audio)
                elif self.recognizer_name == Recognizers.Ibm:
                    cur_str = self.recognizer.recognize_ibm(audio)
                elif self.recognizer_name == Recognizers.Google_Cloud:
                    cur_str = self.recognizer.recognize_google_cloud(audio)
                elif self.recognizer_name == Recognizers.Google:
                    cur_str = self.recognizer.recognize_google(audio)
                print(cur_str)
                if (self.display != None):
                    self.display.updateSpeechDetected(cur_str)
                    #Thread(target = self.display.updateSpeechDetected, args=(cur_str,)).start()
                self.word_classify_check(cur_str)
            except KeyboardInterrupt:
                self.lights.endLights()
                break  
            except sr.UnknownValueError: 
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e: 
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    # This method takes a string version of the audio detected from the speech recognition 
    # package, and then calls the appropriate methods from the light control based on the audio transcript.
    def word_classify_check(self, translated_audio):
        word_array = translated_audio.split()
        # word check holder
        col = None
        coded_col = None
        mixed_col = []
        is_negative_sentence = False
        change_value = 0
        randomize = False
        feat = None

        
        col = self.colorCheck(translated_audio.lower())
        for j in range(len(word_array)):
            cur_word = word_array[j].lower()
            if (randomize == False):
                randomize = self.randomCheck(cur_word)
            if (is_negative_sentence == False):
                is_negative_sentence = self.negativeCheck(cur_word)
            if (change_value == 0):
                change_value = self.changeCheck(cur_word)
            if (feat == None):
                feat = self.featureCheck(cur_word)
            if (coded_col == None):
                coded_col = self.codedWordCheck(cur_word)
            if (self.codedWordCheck(cur_word) != None):
                mixed_col.append(self.codedWordCheck(cur_word))
        if (is_negative_sentence == False):
            if (feat == Features.Brighter):
                self.lights.manipulateBrightness(randomize, change_value)
            elif (feat == Features.Dimmer):
                self.lights.manipulateDimness(randomize, change_value)
            elif (feat == Features.Off):
                self.lights.lightsSwitch(False)
            elif (feat == Features.On):
                self.lights.lightsSwitch(True)
            elif (feat == Features.Hue):
                self.lights.manipulateHue(randomize, change_value)
            elif (feat == Features.Tint):
                self.lights.applyTint()
            elif (feat == Features.Shade):
                self.lights.applyShade()
            elif (feat == Features.Tones):
                self.lights.applyTone()
            elif (feat == Features.Saturation):
                self.lights.manipulateSaturation(randomize, change_value)
            elif (feat == Features.Contrast):
                self.lights.setContrast()
            elif (feat == Features.Primary):
                self.lights.primaryPattern()
            elif (feat == Features.Secondary):
                self.lights.secondaryPattern()
            elif (feat == Features.Tertiary):
                self.lights.tertiaryPattern()
            elif (col != None):
                self.lights.setColor(col.colorRGB)
            #elif (coded_col != None):
            #    self.lights.setColor(coded_col)
            elif (len(mixed_col) != 0):
                self.lights.setColorMix(mixed_col)

        self.lights.strip.show()

    # This method takes a word and determines if its considered a "random" key word,
    # if so return true otherwise return false.
    def randomCheck(self, word):
        if (word == "random"):
            return True
        elif (word == "randomize"):
            return True
        elif (word == "surprise"):
            return True
        elif (word == "unexpected"):
            return True
    
    # This method takes a word and determines if its considered a "negative" key word,
    # if so return true otherwise return false.
    def negativeCheck(self, word):
        if (word == "don't"):
            return True
        elif (word == "not"):
            return True
        elif (word == "no"):
            return True
        return False
    
    # This method takes a word and determines if its considered a "change value" key word. 
    # If consider a "postive change value" return 1, if considered a "negative change value" 
    # return -1, and if neither return 0
    def changeCheck(self, word):
        if (word == "up"):
            return 1
        elif (word == "raise"):
            return 1
        elif (word == "plus"):
            return 1
        elif (word == "more"):
            return 1
        elif (word == "incline"):
            return 1
        elif (word == "upgrade"):
            return 1
        elif (word == "increase"):
            return 1
        elif (word == "high"):
            return 1
        elif (word == "warm"):
            return 1
        if (word == "down"):
            return -1
        elif (word == "lower"):
            return -1
        elif (word == "minus"):
            return -1
        elif (word == "less"):
            return -1
        elif (word == "decline"):
            return -1
        elif (word == "downgrade"):
            return -1
        elif (word == "decrease"):
            return -1
        elif (word == "low"):
            return -1
        elif (word == "diminished"):
            return -1
        elif (word == "lessen"):
            return -1
        elif (word == "lessened"):
            return -1
        elif (word == "lesser"):
            return -1
        elif (word == "reduce"):
            return -1
        elif (word == "reduced"):
            return -1
        elif (word == "cold"):
            return -1
        return 0
    
    # This method takes a word and determines if its considered a "feature" key word,
    # if so return the proper Enum value.
    def featureCheck(self, word):
        if (word == "brighter" or word == "brightness" or word == "bright"):
            return Features.Brighter
        elif (word == "dimmer" or word == "dimness" or word == "dim"):
            return Features.Dimmer
        elif (word == "off"):
            return Features.Off
        elif (word == "on"):
            return Features.On
        elif (word == "hue"):
            return Features.Hue
        elif (word == "tint"):
            return Features.Tint
        elif (word == "saturation"):
            return Features.Saturation
        elif (word == "shade"):
            return Features.Shade
        elif (word == "primary"):
            return Features.Primary
        elif (word == "secondary"):
            return Features.Secondary
        elif (word == "tertiary"):
            return Features.Tertiary
        elif (word == "temperature"):
            return Features.Temperature
        elif (word == "contrast" or word == "contrasting"):
            return Features.Contrast
        elif (word == "tones" or word == "tone"):
            return Features.Tones
        return None
    
    # This method takes a word and determines if its within the coded library,
    # if so the rgb values, otherwise return none.
    def codedWordCheck(self, cur_word):
        for word in self.codedLibrary.wordLib:
            if word.word == cur_word:
                return word.color
        return None
    
    # This method takes a word and determines if its considered a color,
    # if so the rgb values, otherwise return none.
    def colorCheck(self, s):
        cur_color = None
        for color in self.colorLibrary.colorLib:
            if color.colorName in s:
                if cur_color == None:
                    cur_color = color
                else:
                    if (len(color.colorName.split(" ")) > len(cur_color.colorName.split(" "))):
                        cur_color = color
        return cur_color

        