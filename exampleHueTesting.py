from phue import Bridge
from rgbxy import Converter

rgbxy = Converter()
#import logging

#logging.basicConfig()

b = Bridge('10.0.0.149', "vS4w2KQu1fNDEwj-mpp2r8dujuJgr-dASUiGVb9t")

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()


b.set_light(3,'on', True)
temp = rgbxy.rgb_to_xy(0, 0, 255)
b.set_light(3,'xy', temp)
#light_ls = b.lights

#for l in light_ls:
#    l.on = True
