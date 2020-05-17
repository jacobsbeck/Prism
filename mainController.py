import argparse
import time

from speechController import SpeechControl
from lightController import LightControl
from fileController import WordLibrary
from fileController import ColorLibrary
from fileController import Prompts

#BRIDGE_IP = '10.0.0.149'
#BRIDGE_IP = '172.20.10.5'
#USERS_ID = 'vS4w2KQu1fNDEwj-mpp2r8dujuJgr-dASUiGVb9t'

def main(args):
    
    hue_ip = args.hueIP
    hue_id = args.hueID
    wordFileName = args.wordFile
    colorFileName = args.colorFile
    numLEDs = args.leds
    rec = args.recognizer
<<<<<<< HEAD
    wordLib = ColorLibrary(fileName)
    colorLib = ColorLibrary("colorFile.txt")
    prompts = Prompts("prompts.txt")
=======
    
    wordLib = WordLibrary(wordFileName)
    colorLib = ColorLibrary(colorFileName)
>>>>>>> 067a6042130dcd651b2eeb9a1dca891a8128c77f
    lights = LightControl(numLEDs, hue_ip, hue_id)
<<<<<<< HEAD
    #lights.setColor([0,1,0])
    #lights.strip.show()
    #time.sleep(2)
    #lights.manipulateHue(False, 0)
    #lights.strip.show()
    speech = SpeechControl(lights, wordLib, colorLib, rec)
=======
    display = DisplayControl(prompts)
    speech = SpeechControl(lights, wordLib, colorLib, rec, display)
>>>>>>> 4415dee6f368fb083f752d95d4c54f06ff9a0a2d

    speech.createContinuousStream()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
<<<<<<< HEAD
    parser.add_argument('-ip', '--hueIP',          metavar='ip_address',     default=10.0.0.149,              help='uses this is you have hue lights and bridge you would like to connect')
    parser.add_argument('-id', '--hueID',          metavar='user_id',     default='vS4w2KQu1fNDEwj-mpp2r8dujuJgr-dASUiGVb9t',                 help='uses this is you have hue lights and bridge you would like to connect')
    parser.add_argument('-f', '--file',            metavar='name',     default='allCodedWords.txt',     help='use this if you have your own file of data')
    parser.add_argument('-l', '--leds',            metavar='size',     default=300,                     help='the number of LED ligths', type=int)
    parser.add_argument('-d', '--display',         action='store_true',                                 help='if you are using a smart mirror display')
    parser.add_argument('-sr', '--recognizer',     metavar='speech_recognition',   default='google',    help='if you are using a smart mirror display')
=======
    parser.add_argument('-ip', '--hueIP',          metavar='ip_address',     default='10.0.0.149',                            help='uses this is you have hue lights and bridge you would like to connect')
    parser.add_argument('-id', '--hueID',          metavar='user_id',     default='vS4w2KQu1fNDEwj-mpp2r8dujuJgr-dASUiGVb9t', help='uses this is you have hue lights and bridge you would like to connect')
    parser.add_argument('-wf', '--wordFile',       metavar='filename',     default='allCodedWords.txt',                       help='use this if you have your own file of data')
    parser.add_argument('-cf', '--colorFile',      metavar='filename',     default='colorFile.txt',                           help='use this if you have your own file of data')
    parser.add_argument('-l', '--leds',            metavar='size',     default=64,                                           help='the number of LED ligths', type=int)
    parser.add_argument('-d', '--display',         action='store_true',                                                       help='if you are using a smart mirror display')
    parser.add_argument('-sr', '--recognizer',     metavar='speech_recognition',   default='google',                          help='specify which recognition package you\'re using')
>>>>>>> 067a6042130dcd651b2eeb9a1dca891a8128c77f
    args = parser.parse_args()
    main(args)