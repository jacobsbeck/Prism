import speech_recognition as sr
from neopixel import *

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

r = sr.Recognizer()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def word_classify_check(translated_audio):
    word_array = translated_audio.split()
    for j in range(len(word_array)):
        cur_word = word_array[j].lower()
        if (cur_word == "red"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 255, 0))
            strip.show()
        elif (cur_word == "green"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(255, 0, 0))
            strip.show()
        elif (cur_word == "blue"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 0, 255))
            strip.show()
        elif (cur_word == "yellow"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(255, 255, 0))
            strip.show()
        elif (cur_word == "orange"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(128, 255, 0))
            strip.show()
        elif (cur_word == "purple"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 128, 128))
            strip.show()
        elif (cur_word == "white"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(255, 255, 255))
            strip.show()
        elif (cur_word == "black"):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

while True:
    mic = sr.Microphone()
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        cur_str = r.recognize_google(audio)
        print(cur_str)
        word_classify_check(cur_str)
    except KeyboardInterrupt:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        break;
        
    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand audio") 
      
    except sr.RequestError as e: 
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    