import argparse
import time
from threading import Thread

from speechController import SpeechControl
from lightController import LightControl
from displayController import DisplayControl
from fileController import WordLibrary
from fileController import ColorLibrary
from fileController import Prompts

#BRIDGE_IP = '10.0.0.149'
#BRIDGE_IP = '172.20.10.5'
#USERS_ID = 'vS4w2KQu1fNDEwj-mpp2r8dujuJgr-dASUiGVb9t'

def main(args):
    
    wordLib = WordLibrary(args.wordFile)
    colorLib = ColorLibrary(args.colorFile)
    prompts = Prompts("prompts.txt")

    lights = LightControl(args.leds, args.hueIP, args.hueID)
    
    if (args.display):
        #Thread(display = DisplayControl(prompts)).start()
        display = DisplayControl(prompts)
        speech = SpeechControl(lights, wordLib, colorLib, args.recognizer, display)
    else:
        speech = SpeechControl(lights, wordLib, colorLib, args.recognizer)
    #Thread(target = display.showDisplay).start()
    Thread(target = speech.createContinuousStream).start()
    display.showDisplay()
    lights.endLights()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-ip', '--hueIP',          metavar='ip_address',     default='10.0.0.149',                            help='uses this is you have hue lights and bridge you would like to connect')
    parser.add_argument('-id', '--hueID',          metavar='user_id',     default='vS4w2KQu1fNDEwj-mpp2r8dujuJgr-dASUiGVb9t', help='uses this is you have hue lights and bridge you would like to connect')
    parser.add_argument('-wf', '--wordFile',       metavar='filename',     default='allCodedWords.txt',                       help='use this if you have your own file of data')
    parser.add_argument('-cf', '--colorFile',      metavar='filename',     default='colorFile.txt',                           help='use this if you have your own file of data')
    parser.add_argument('-l', '--leds',            metavar='size',     default=64,                                            help='the number of LED ligths', type=int)
    parser.add_argument('-d', '--display',         action='store_true', default=True,                                         help='if you are using a smart mirror display')
    parser.add_argument('-sr', '--recognizer',     metavar='speech_recognition',   default='google',                          help='specify which recognition package you\'re using')
    args = parser.parse_args()
    main(args)