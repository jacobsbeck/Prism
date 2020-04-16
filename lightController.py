from phue import Bridge
from neopixel import *
from colour import Color
from rgbxy import Converter
import colorsys
import random

rgbxy = Converter()

class LightControl:
  
  def __init__(self, led_count, hue_IP=None, hue_ID=None):
    # LED strip configuration:
    self.LED_COUNT = led_count      # Number of LED pixels.
    self.LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #self.LED_PIN = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    self.LED_DMA = 10      # DMA channel to use for generating signal (try 10)
    self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    self.LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
    self.LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    if (hue_IP != None):
      self.hue_available = True
      try:
        if (hue_ID == None):
          self.bridge = Bridge(hue_IP)
        else:
          self.bridge = Bridge(hue_IP, hue_ID)
        self.bridge.connect()
        self.hue_lights = self.bridge.lights
      except ValueError: 
        print("Could not connect/find hue bridge connected to ip address: {0}".format(hue_IP))
    else:
      self.hue_available = False

    self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
    self.strip.begin()
    self.startLights()

  def __str__(self):
    s = "LED Count: {}\n".format(self.LED_COUNT)
    if (self.hue_available):
      s = s + "Hue IP: {}\nHue ID: {}\nNum Hue Lights: {}\n".format(self.bridge.ip, self.bridge.username, len(self.hue_lights))
    else:
      s = s + "Hue lights unavailable"
    return s

  def startLights(self):
    for i in range(self.LED_COUNT):
      self.strip.setPixelColor(i, Color(255, 255, 255))
    for l in self.hue_lights:
      l.xy = [0.33, 0.33]
      l.brightness = 255
    self.strip.setBrightness(255)
    self.strip.show()

  def endLights(self):
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, Color(0, 0, 0))
    self.strip.show()
    if self.hue_available:
      for l in self.hue_lights:
        l.xy = [0.33, 0.33]
        l.brightness = 0
  
  def manipulateBrightness(self, rand_check, change):
    manipulation_value = 100
    if (change >= 0):
      if (self.strip.getBrightness() >= 255 - manipulation_value):
        self.strip.setBrightness(255)
      else:
        self.strip.setBrightness(self.strip.getBrightness() + manipulation_value)
    else:
      if (self.strip.getBrightness() <= manipulation_value):
        self.strip.setBrightness(0)
      else:
        self.strip.setBrightness(self.strip.getBrightness() - manipulation_value)
    if (rand_check == True):
      self.strip.setBrightness(random.randrange(0, 255))
    for l in self.hue_lights:
      if (change >= 0):
        if (l.brightness >= 254 - manipulation_value):
          l.brightness = 254
        else:
          l.brightness = l.brightness + manipulation_value
      else:
        if (l.brightness <= manipulation_value):
          l.brightness = 0
        else:
          l.brightness = l.brightness - manipulation_value
      if (rand_check == True):
        l.brightness = random.randrange(0, 254)

  def manipulateDimness(self, rand_check, change):
    manipulation_value = 100
    if (change >= 0):
      if (self.strip.getBrightness() <= manipulation_value):
        self.strip.setBrightness(0)
      else:
        self.strip.setBrightness(self.strip.getBrightness() - manipulation_value)
    else:
      if (self.strip.getBrightness() >= 255 - manipulation_value):
        self.strip.setBrightness(255)
      else:
        self.strip.setBrightness(self.strip.getBrightness() + manipulation_value)
    if (rand_check == True):
      self.strip.setBrightness(random.randrange(0, 255))
    for l in self.hue_lights:
      if (change >= 0):
        if (l.brightness <= manipulation_value):
          l.brightness = 0
        else:
          l.brightness = l.brightness - manipulation_value
      else:
        if (l.brightness >= 254 - manipulation_value):
          l.brightness = 0
        else:
          l.brightness = l.brightness + manipulation_value
      if (rand_check == True):
        l.brightness = random.randrange(0, 254)

  def setContrast(self):
    for i in range(self.LED_COUNT):
      cur_RGB = rgbint_to_rgb(self.strip.getPixelColor(i))
      cur_HLS = colorsys.rgb_to_hls(cur_RGB[0], cur_RGB[1], cur_RGB[2])
      cur_RGB = colorsys.hsv_to_rgb((360 - cur_HLS[0] * 360) / 360, cur_HLS[1], cur_HLS[2])
      self.strip.setPixelColor(i, Color(int(cur_RGB[1] * 255), int(cur_RGB[0] * 255), int(cur_RGB[2] * 255)))
    for l in self.hue_lights:
      rgb_value = rgbxy.xy_to_rgb(l.xy)
      cur_HSV = colorsys.rgb_to_hsv(rgb_value[0], rgb_value[1], rgb_value[2])
      new_rgb_value = colorsys.hsv_to_rgb((360 - cur_HSV[0] * 360) / 360, cur_HLS[1], cur_HLS[2])
      l.xy = rgbxy.rgb_to_xy(new_rgb_value[0], new_rgb_value[1], new_rgb_value[2])

  def manipulateSaturation(self, rand_check, change):
    for i in range(self.LED_COUNT):
      cur_RGB = rgbint_to_rgb(self.strip.getPixelColor(i))
      cur_HSV = colorsys.rgb_to_hsv(cur_RGB[0], cur_RGB[1], cur_RGB[2])
      if rand_check:
        cur_RGB = colorsys.hsv_to_rgb(cur_HSV[0], random.randrange(0, 100) / 100, cur_HSV[2])
      elif change >= 0:
        cur_RGB = colorsys.hsv_to_rgb(cur_HSV[0], random.randrange(cur_HSV[1] * 100, 100) / 100, cur_HSV[2])
      else:
        cur_RGB = colorsys.hsv_to_rgb(cur_HSV[0], random.randrange(0, cur_HSV[1] * 100) / 100, cur_HSV[2])
      self.strip.setPixelColor(i, Color(cur_RGB[1] * 255, cur_RGB[0] * 255, cur_RGB[2] * 255))
    for l in self.hue_lights:
      rgb_value = rgbxy.xy_to_rgb(l.xy)
      cur_HSV = colorsys.rgb_to_hsv(rgb_value[0], rgb_value[1], rgb_value[2])
      if rand_check:
        cur_RGB = colorsys.hsv_to_rgb(cur_HSV[0], random.randrange(0, 100) / 100, cur_HSV[2])
      elif change >= 0:
        cur_RGB = colorsys.hsv_to_rgb(cur_HSV[0], random.randrange(cur_HSV[1] * 100, 100) / 100, cur_HSV[2])
      else:
        cur_RGB = colorsys.hsv_to_rgb(cur_HSV[0], random.randrange(0, cur_HSV[1] * 100) / 100, cur_HSV[2])
      l.xy = rgbxy.rgb_to_xy(cur_RGB[0] * 255, cur_RGB[1] * 255, cur_RGB[2] * 255)

  def manipulateHue(self, rand_check, change):
    for i in range(self.LED_COUNT):
      cur_RGB = rgbint_to_rgb(self.strip.getPixelColor(i))
      cur_HSV = colorsys.rgb_to_hsv(cur_RGB[0], cur_RGB[1], cur_RGB[2])
      if rand_check:
        cur_RGB = colorsys.hsv_to_rgb(random.randrange(0, 360) / 360, cur_HSV[1], cur_HSV[2])
      elif change >= 0:
        cur_RGB = colorsys.hsv_to_rgb(random.randrange(cur_HSV[0] * 360, 360) / 360, cur_HSV[1], cur_HSV[2])
      else:
        cur_RGB = colorsys.hsv_to_rgb(random.randrange(0, cur_HSV[0] * 360) / 360, cur_HSV[1], cur_HSV[2])
      self.strip.setPixelColor(i, Color(cur_RGB[1] * 255, cur_RGB[0] * 255, cur_RGB[2] * 255))
      for l in self.hue_lights:
        rgb_value = rgbxy.xy_to_rgb(l.xy[0], l.xy[1])
        cur_HSV = colorsys.rgb_to_hsv(rgb_value[0], rgb_value[1], rgb_value[2])
        if rand_check:
          cur_RGB = colorsys.hsv_to_rgb(random.randrange(0, 360) / 360, cur_HSV[1], cur_HSV[2])
        elif change >= 0:
          cur_RGB = colorsys.hsv_to_rgb(random.randrange(cur_HSV[0] * 360, 360) / 360, cur_HSV[1], cur_HSV.index(2))
        else:
          cur_RGB = colorsys.hsv_to_rgb(random.randrange(0, cur_HSV[0] * 360) / 360, cur_HSV[1], cur_HSV[2])
        l.xy = rgbxy.rgb_to_xy(cur_RGB[0] * 255, cur_RGB[1] * 255, cur_RGB[2] * 255)

  def manipulateTemperature(self, rand_check, change):
    low_temp = 1700
    high_temp = 6500
    for i in range(self.LED_COUNT):
      cur_RGB = rgbint_to_rgb(self.strip.getPixelColor(i))
      cur_XY = rgbxy.rgb_to_xy(cur_RGB[0], cur_RGB[1], cur_RGB[2])
      cur_CCT = Color.xy_to_CCT(cur_XY, 'hernandez1999')
      if rand_check:
        new_XY = Color.CCT_to_xy(random.randrange(low_temp, high_temp))
      elif change >= 0:
        new_XY = Color.CCT_to_xy(random.randrange(cur_CCT, high_temp))
      else:
        new_XY = Color.CCT_to_xy(random.randrange(low_temp, cur_CCT))
      new_RGB = rgbxy.xy_to_rgb(new_XY[0], new_XY[1])
      self.strip.setPixelColor(i, Color(new_RGB[1], new_RGB[0], new_RGB[2]))
    for l in self.hue_lights:
      cur_CCT = Color.xy_to_CCT(l.xy)
      if rand_check:
        new_XY = Color.CCT_to_xy(random.randrange(low_temp, high_temp))
      elif change >= 0:
        new_XY = Color.CCT_to_xy(random.randrange(cur_CCT, high_temp))
      else:
        new_XY = Color.CCT_to_xy(random.randrange(low_temp, cur_CCT))
      l.xy = new_XY

  def applyTint(self):
    for i in range(self.LED_COUNT):
      cur_RGB = rgbint_to_rgb(self.strip.getPixelColor(i))
      self.strip.setPixelColor(i, Color(int((255 - cur_RGB[1]) / 2), int((255 - cur_RGB[0]) / 2), int((255 - cur_RGB[2]) / 2)))
    for l in self.hue_lights:
      cur_RGB = rgbxy.xy_to_rgb(l.xy)
      l.xy = rgbxy.rgb_to_xy(int((255 - cur_RGB[0]) / 2), int((255 - cur_RGB[1]) / 2), int((255 - cur_RGB[2]) / 2))

  def applyShade(self):
    for i in range(self.LED_COUNT):
      cur_RGB = rgbint_to_rgb(self.strip.getPixelColor(i))
      self.strip.setPixelColor(i, Color(int(cur_RGB[0] / 2), int(cur_RGB[1] / 2), int(cur_RGB[2] / 2)))
    for l in self.hue_lights:
      cur_RGB = rgbxy.xy_to_rgb(l.xy[0], l.xy[1])
      l.xy = rgbxy.rgb_to_xy(cur_RGB[0] / 2, cur_RGB[1] / 2, cur_RGB[2] / 2)

  def applyTone(self):
    grayTone = 211
    for i in range(self.LED_COUNT):
      self.strip.setPixelColor(i, Color((self.strip.getPixelColor(i).red + grayTone) / 2, (self.strip.getPixelColor(i).green + grayTone) / 2, (self.strip.getPixelColor(i).blue + grayTone) / 2))

  def primaryPattern(self):
    for i in range(self.LED_COUNT):
      if (i / 25 == 0):
        self.strip.setPixelColor(i, Color(255, 255, 0))
      elif (i / 25 == 4):
        self.strip.setPixelColor(i, Color(0, 0, 255))
      elif (i / 25 == 8):
        self.strip.setPixelColor(i, Color(0, 255, 0))
  
  def secondaryPattern(self):
    for i in range(self.LED_COUNT):
      if (i / 25 == 2):
        self.strip.setPixelColor(i, Color(255, 0, 0))
      elif (i / 25 == 6):
        self.strip.setPixelColor(i, Color(238,130,238))
      elif (i / 25 == 10):
        self.strip.setPixelColor(i, Color(128, 255, 0))

  def tertiaryPattern(self):
    for i in range(self.LED_COUNT):
      if (i / 25 == 1):
        self.strip.setPixelColor(i, Color(154,205,50))
      elif (i / 25 == 3):
        self.strip.setPixelColor(i, Color(0, 221, 221))
      elif (i / 25 == 5):
        self.strip.setPixelColor(i, Color(138, 43, 226)) 
      elif (i / 25 == 7):
        self.strip.setPixelColor(i, Color(199, 21, 133))
      elif (i / 25 == 9):
        self.strip.setPixelColor(i, Color(255, 69, 0))
      elif (i / 25 == 11):
        self.strip.setPixelColor(i, Color(255, 174, 66)) 

  def lightSwitch(self, on):
    if on:
      self.strip.setBrightness(255)
      for l in self.hue_lights:
        l.brightness = 255
    else:
      self.strip.setBrightness(0)
      for l in self.hue_lights:
        l.brightness = 0
  
  def setColor(self, col):
    for i in range(self.LED_COUNT):
      self.strip.setPixelColor(i, Color(col[1], col[0], col[2]))
    for l in self.hue_lights:
      l.xy = rgbxy.rgb_to_xy(col[0], col[1], col[2])
  
  def setColorMix(self, col):
    tempRed = 0
    tempGreen = 0
    tempBlue = 0
    for j in col:
      tempRed = j[0] + tempRed
      tempGreen = j[1] + tempGreen
      tempBlue = j[2] + tempBlue
    tempColor = Color(rgb=(round(tempRed / len(col), 3), round(tempGreen / len(col), 3), round(tempBlue / len(col), 3)))
    for i in range(self.LED_COUNT):
      self.strip.setPixelColor(i, Color(tempColor[1], tempColor[0], tempColor[2]))
    for l in self.hue_lights:
      l.xy = rgbxy.rgb_to_xy(col[0], col[1], col[2])

def rgbint_to_rgb(rgbint):
  return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)