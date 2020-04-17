from phue import Bridge
from rgbxy import Converter

rgbxy = Converter()
#import logging

#logging.basicConfig()

BRIDGE_IP = '10.0.0.149'
#BRIDGE_IP = '172.20.10.5'
USERS_ID = 'vS4w2KQu1fNDEwj-mpp2r8dujuJgr-dASUiGVb9t'
b = Bridge(BRIDGE_IP, USERS_ID)

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
#b.connect()

hue_lights = b.lights
for l in hue_lights:
    l.off = True

b.set_light(3,'alert', 'lselect')
#b.set_light(3,'on', True)
#temp = rgbxy.rgb_to_xy(128, 128, 0)
#b.set_light(3,'xy', temp)

#light_ls = b.lights

#for l in light_ls:
#    l.on = True
