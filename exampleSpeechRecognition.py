import speech_recognition as sr
from neopixel import *
from enum import Enum
import random
import colour
from phue import Bridge

class Features(Enum):
    Brighter=1
    Dimmer=2
    Color=3
    Off=4
    On=5
    Hue=6
    Tint=7
    Saturation=8
    Shade=9
    Monochromatic=10
    Primary=11
    Secondary=12
    Tertiary=13
    Temperature=14
    Chroma=15
    Contrast=16
    Tones=17
    Light=18

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

b = Bridge('10.0.0.149')
b.connect()
hue_lights = b.get_light_objects()

def main():
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
            break
            
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio")
        
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def word_classify_check(translated_audio):
    word_array = translated_audio.split()
    col = None
    is_negative_sentence = False
    change_value = 0
    randomize = False
    feat = None
    for j in range(len(word_array)):
        cur_word = word_array[j].lower()
        if (randomize == False):
            randomize = randomCheck(cur_word)
        if (is_negative_sentence == False):
            is_negative_sentence = negativeCheck(cur_word)
        if (change_value == 0):
            change_value = downCheck(cur_word)
        if (change_value == 0):
            change_value = upCheck(cur_word)
        if (col == None):
            color = colorCheck(cur_word)
        if (feat == None):
            feat = featureCheck(cur_word)

    if (is_negative_sentence == False):
        if (feat == Features.Brighter):
            manipulateBrightness(randomize, change_value)
        elif (feat == Features.Dimmer):
             manipulateDimness(randomize, change_value)
        elif (feat == Features.Off):
            strip.setBrightness(0)
            for l in hue_lights:
                l.brightness = 0
        elif (feat == Features.On):
            strip.setBrightness(255)
            for l in hue_lights:
                l.brightness = 255
        elif (feat == Features.Hue):
            manipulateHue(randomize, change_value)
        elif (feat == Features.Tint):
            applyTint()
        elif (feat == Features.Shade):
            applyShade()
        elif (feat == Features.Tones):
            applyTone()
        elif (feat == Features.Saturation):
            manipulateSaturation(randomize, change_value)
        elif (feat == Features.Contrast):
            setContrast()
        
    elif (feat == Features.Primary):
        primaryPattern()
    elif (feat == Features.Secondary):
        secondaryPattern()
    elif (feat == Features.Tertiary):
        tertiaryPattern()
    elif (col != None):
        for i in range(LED_COUNT):
            strip.setPixelColor(i, col)
        for l in range(hue_lights):
            l.xy = colour.rgb_to_xy(col.red, col.green, col.blue))
    strip.show()

def setContrast():
    for i in range(LED_COUNT):
        cur_HLS = colour.rgb_to_hls(strip.getPixelColor(i).r, strip.getPixelColor(i).g, strip.getPixelColor(i).b)
        cur_RGB = colour.hsv_to_rgb((360 - cur_HLS.index(0) * 360) / 360, cur_HLS.index(1), cur_HLS.index(2))
        strip.setPixelColor(i, Color(cur_RGB.index(0) * 255, cur_RGB.index(1) * 255, cur_RGB.index(2) * 255))
    for l in range(hue_lights):
        rgb_value = colour.xy_to_rgb(l.xy)
        cur_HSV = colour.rgb_to_hsv(rgb_value.index(0), rgb_value.index(1), rgb_value.index(2))
        new_rgb_value = colour.hsv_to_rgb((360 - cur_HSV.index(0) * 360) / 360, cur_HLS.index(1), cur_HLS.index(2))
        l.xy = colour.rgb_to_xy(new_rgb_value.index(0), new_rgb_value.index(1), new_rgb_value.index(2))

def manipulateBrightness(rand_check, change):
    if (change >= 0):
        if (strip.getBrightness() >= 215):
            strip.setBrightness(255)
        else:
            strip.setBrightness(strip.getBrightness() + 40)
    else:
        if (strip.getBrightness() <= 40):
            strip.setBrightness(0)
        else:
            strip.setBrightness(strip.getBrightness() - 40)
    if (rand_check == True):
        strip.setBrightness(random.randrange(0, 255))
    for l in range(hue_lights):
        if (change >= 0):
            if (l.brightness >= 214):
                l.brightness = 254
            else:
                l.brightness = l.brightness + 40
        else:
            if (l.brightness <= 40):
                l.brightness = 0
            else:
                l.brightness = l.brightness - 40
        if (rand_check == True):
            l.brightness = random.randrange(0, 254)


def manipulateDimness(rand_check, change):
    if (change >= 0):
        if (strip.getBrightness() <= 40):
            strip.setBrightness(0)
        else:
            strip.setBrightness(strip.getBrightness() - 40)
    else:
        if (strip.getBrightness() >= 215):
            strip.setBrightness(255)
        else:
            strip.setBrightness(strip.getBrightness() + 40)
    if (rand_check == True):
        strip.setBrightness(random.randrange(0, 255))
    for l in range(hue_lights):
        if (change >= 0):
            if (l.brightness <= 40):
                l.brightness = 0
            else:
                l.brightness = l.brightness - 40
        else:
            if (l.brightness >= 254):
                l.brightness = 0
            else:
                l.brightness = l.brightness + 40
        if (rand_check == True):
            l.brightness = random.randrange(0, 254)

def manipulateSaturation(rand_check, change):
    for i in range(LED_COUNT):
        cur_HSV = colour.rgb_to_hsv(strip.getPixelColor(i).r, strip.getPixelColor(i).g, strip.getPixelColor(i).b)
        if rand_check:
            cur_RGB = colour.hsv_to_rgb(cur_HSV.index(0), random.randrange(0, 100) / 100, cur_HSV.index(2))
        elif change >= 0:
            cur_RGB = colour.hsv_to_rgb(cur_HSV.index(0), random.randrange(cur_HSV.index(1) * 100, 100) / 100, cur_HSV.index(2))
        else:
            cur_RGB = colour.hsv_to_rgb(cur_HSV.index(0), random.randrange(0, cur_HSV.index(1) * 100) / 100, cur_HSV.index(2))
        strip.setPixelColor(i, Color(cur_RGB.index(0) * 255, cur_RGB.index(1) * 255, cur_RGB.index(2) * 255))
    for l in range(hue_lights):
        rgb_value = colour.xy_to_rgb(l.xy)
        cur_HSV = colour.rgb_to_hsv(rgb_value.index(0),rgb_value.index(1), rgb_value.index(2))
        if rand_check:
            cur_RGB = colour.hsv_to_rgb(cur_HSV.index(0), random.randrange(0, 100) / 100, cur_HSV.index(2))
        elif change >= 0:
            cur_RGB = colour.hsv_to_rgb(cur_HSV.index(0), random.randrange(cur_HSV.index(1) * 100, 100) / 100, cur_HSV.index(2))
        else:
            cur_RGB = colour.hsv_to_rgb(cur_HSV.index(0), random.randrange(0, cur_HSV.index(1) * 100) / 100, cur_HSV.index(2))
        l.xy = colour.rgb_to_xy(cur_RGB.index(0) * 255, cur_RGB.index(1) * 255, cur_RGB.index(2) * 255)
        
def manipulateHue(rand_check, change):
    for i in range(LED_COUNT):
        cur_HSV = colour.rgb_to_hsv(strip.getPixelColor(i).r, strip.getPixelColor(i).g, strip.getPixelColor(i).b)
        if rand_check:
            cur_RGB = colour.hsv_to_rgb(random.randrange(0, 360) / 360, cur_HSV.index(1), cur_HSV.index(2))
        elif change >= 0:
            cur_RGB = colour.hsv_to_rgb(random.randrange(cur_HSV.index(0) * 360, 360) / 360, cur_HSV.index(1), cur_HSV.index(2))
        else:
            cur_RGB = colour.hsv_to_rgb(random.randrange(0, cur_HSV.index(0) * 360) / 360, cur_HSV.index(1), cur_HSV.index(2))
        strip.setPixelColor(i, Color(cur_RGB.index(0) * 255, cur_RGB.index(1) * 255, cur_RGB.index(2) * 255))
    for l in range(hue_lights):
        rgb_value = colour.xy_to_rgb(l.xy)
        cur_HSV = colour.rgb_to_hsv(rgb_value.index(0), rgb_value.index(1), rgb_value.index(2))
        if rand_check:
            cur_RGB = colour.hsv_to_rgb(random.randrange(0, 360) / 360, cur_HSV.index(1), cur_HSV.index(2))
        elif change >= 0:
            cur_RGB = colour.hsv_to_rgb(random.randrange(cur_HSV.index(0) * 360, 360) / 360, cur_HSV.index(1), cur_HSV.index(2))
        else:
            cur_RGB = colour.hsv_to_rgb(random.randrange(0, cur_HSV.index(0) * 360) / 360, cur_HSV.index(1), cur_HSV.index(2))
        l.xy = colour.rgb_to_xy(cur_RGB.index(0) * 255, cur_RGB.index(1) * 255, cur_RGB.index(2) * 255)
        
def applyTint():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color((255 - strip.getPixelColor(i).red) / 2, (255 - strip.getPixelColor(i).green) / 2, (255 - strip.getPixelColor(i).blue) / 2))
    for l in range(hue_lights):
        cur_RGB = colour.xy_to_rgb(l.xy)
        l.xy = colour.rgb_to_xy((255 - cur_RGB.red) / 2, (255 - cur_RGB.green) / 2, (255 - cur_RGB.blue) / 2)

def applyShade():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(strip.getPixelColor(i).red / 2, strip.getPixelColor(i).green / 2, strip.getPixelColor(i).blue / 2))
    for l in range(hue_lights):
        cur_RGB = colour.xy_to_rgb(l.xy)
        l.xy = colour.rgb_to_xy(cur_RGB.red / 2, cur_RGB.green / 2, cur_RGB.blue / 2)

def applyTone():
    grayTone = 211
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color((strip.getPixelColor(i).red + grayTone) / 2, (strip.getPixelColor(i).green + grayTone) / 2, (strip.getPixelColor(i).blue + grayTone) / 2))

def manipulateTemperature(rand_check, change):
    low_temp = 1700
    high_temp = 6500
    for i in range(LED_COUNT):
        cur_RGB = strip.getPixelColor(i)
        cur_XY = colour.rgb_to_xy(cur_RGB.red, cur_RGB.green, cur_RGB.blue)
        cur_CCT = colour.xy_to_CCT(cur_XY.index(0), cur_XY.index(1))
        if rand_check:
            new_XY = colour.CCT_to_xy(random.randrange(low_temp, high_temp))
        elif change >= 0:
            new_XY = colour.CCT_to_xy(random.randrange(cur_CCT, high_temp))
        else:
            new_XY = colour.CCT_to_xy(random.randrange(low_temp, cur_CCT))
        new_RGB = colour.xy_to_rgb(new_XY.index(0), new_XY.index(1))
        strip.setPixelColor(i, Color(new_RGB.index(0), new_RGB.index(1), new_RGB.index(2)))
    for l in range(hue_lights):
        cur_CCT = colour.xy_to_CCT(l.xy)
        if rand_check:
            new_XY = colour.CCT_to_xy(random.randrange(low_temp, high_temp))
        elif change >= 0:
            new_XY = colour.CCT_to_xy(random.randrange(cur_CCT, high_temp))
        else:
            new_XY = colour.CCT_to_xy(random.randrange(low_temp, cur_CCT))
        l.xy = new_XY

def primaryPattern():
    for i in range(LED_COUNT):
        if (i / 25 == 0):
            strip.setPixelColor(i, Color(255, 255, 0))
        elif (i / 25 == 4):
            strip.setPixelColor(i, Color(0, 0, 255))
        elif (i / 25 == 8):
            strip.setPixelColor(i, Color(0, 255, 0))
        
def secondaryPattern():
    for i in range(LED_COUNT):
        if (i / 25 == 2):
            strip.setPixelColor(i, Color(255, 0, 0))
        elif (i / 25 == 6):
            strip.setPixelColor(i, Color(238,130,238))
        elif (i / 25 == 10):
            strip.setPixelColor(i, Color(128, 255, 0))

def tertiaryPattern():
    for i in range(LED_COUNT):
        if (i / 25 == 1):
            strip.setPixelColor(i, Color(154,205,50))
        elif (i / 25 == 3):
            strip.setPixelColor(i, Color(0, 221, 221))
        elif (i / 25 == 5):
            strip.setPixelColor(i, Color(138, 43, 226)) 
        elif (i / 25 == 7):
            strip.setPixelColor(i, Color(199, 21, 133))
        elif (i / 25 == 9):
            strip.setPixelColor(i, Color(255, 69, 0))
        elif (i / 25 == 11):
            strip.setPixelColor(i, Color(255, 174, 66))        


def downCheck(word):
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
    return 0

def upCheck(word):
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
    return 0

def featureCheck(word):
    if (word == "brighter" or word == "brightness"):
        return Features.Brighter
    elif (word == "dimmer" or word == "dimness"):
        return Features.Dimmer
    elif (word == "color"):
        return Features.Color
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
    elif (word == "monochromatic"):
        return Features.Monochromatic
    elif (word == "primary"):
        return Features.Primary
    elif (word == "secondary"):
        return Features.Secondary
    elif (word == "tertiary"):
        return Features.Tertiary
    elif (word == "temperature"):
        return Features.Temperature
    elif (word == "chroma"):
        return Features.Chroma
    elif (word == "contrast" or word == "contrasting"):
        return Features.Contrast
    elif (word == "tones"):
        return Features.Tones
    elif (word == "light"):
        return Features.Light
    return None

def negativeCheck(word):
    if (word == "don't"):
        return True
    elif (word == "not"):
        return True
    elif (word == "no"):
        return True
    return False

def colorCheck(word):
    if (word == "red"):
        return Color(0, 255, 0)
    elif (word == "green"):
        return Color(255, 0, 0)
    elif (word == "blue"):
        return Color(0, 0, 255)
    elif (word == "yellow"):
        return Color(255, 255, 0)
    elif (word == "orange"):
        return Color(128, 255, 0)
    elif (word == "purple"):
        return Color(0, 128, 128)
    elif (word == "white"):
        return Color(255, 255, 255)
    elif (word == "black"):
        return Color(0, 0, 0)
    return None

def randomCheck(word):
    if (word == "random"):
        return True
    elif (word == "randomize"):
        return True
    elif (word == "surprise"):
        return True
    elif (word == "unexpected"):
        return True

main()