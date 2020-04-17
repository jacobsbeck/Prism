# Prism
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Sound Classification](#sound-classification)
* [Speech Recognition](#speech-recognition)

## General info
Hello! This is the project Prism, created for the Interactive Media Design 2020 Capstone at the University of Washington Bothell. This project uses a Raspberry Pi 4 and a Blue Snowball microphone to manipulate lights. This project utilizes audio classification, noise cancellation, and machine learning to create a unique audio to light expereince. The audio calssification model I used for this project is based off of [this](https://github.com/mtobeiyf/audio-classification) project I found during my research.
	
## Technologies
Hardware:
* Raspberry Pi 4
* LED Strip
* Hue Bridge and Lights (optional)

Software:
* Python 3.6
* scipy
* librosa
* tensorflow
* pysoundfile
* sounddevice
* matplotlib
* scikit-learn
* tensorflow
* keras
* pyaudio
* wave
* keyboard
* rpi-ws281x
* speechrecognition
* google-cloud-speech
* pHue
* colorsys
* colour
* rgbxy
	
## Setup
To run this project, install the appropriate packages:
```
$ pip install scipy==1.2.3
$ pip install librosa==0.6.0
$ pip install matplotlib
$ pip install pyaudio
$ pip install wave
$ pip install keyboard
$ pip install tensorflow
$ pip install pysoundfile
$ pip install sounddevice
$ pip install keras
$ pip install numpy
$ pip install rpi-ws281x
$ pip install scikit-learn
$ pip install speechrecognition
$ pip install google-cloud-speech
$ pip install phue
$ pip install colorsys
$ pip install rgbxy
$ pip install colour
```

## Speech Recognition
To run the latest version of the program, run the following code:
```
$ sudo bash ./mainStart.sh
```
Some different variables that can be passed into the execution command line:
* -ip: IP Address of your hue bridge
* -id: Unique username to access hue bridge
* -wf: Filename of coded words you want to use
* -cf: Filename of color names you want to use
* -l: Number of LEDs used in system
* -d: If you are using a display
* -sr: The speech library you are using

To run the pervious version of the program, run the following code:
```
$ sudo bash ./speechStart.sh
```

