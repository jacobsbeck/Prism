# Prism
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Speech Recognition](#speech-recognition)

## General info
Hello! This is the project Prism, created for the Interactive Media Design 2020 Capstone at the University of Washington Bothell. This project uses a Raspberry Pi 4 and a Blue Snowball microphone to manipulate lights. This project utilizes speech recognition to create a light expereince using LED lights. This project also has the capability to use hue lights as well as a smart mirror display.
	
## Technologies
Hardware:
* Raspberry Pi 4
* LED Strip
* Hue Bridge and Lights (optional)
* Smart Mirror Display (optional)

Software:
* Python 3.6
* scipy
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
$ pip install pyaudio
$ pip install wave
$ pip install keyboard
$ pip install rpi-ws281x
$ pip install speechrecognition
$ pip install google-cloud-speech
$ pip install phue
$ pip install colorsys
$ pip install rgbxy
$ pip install colour
```

## Run Project
The system is broken up into four different controllers, main, speech, light, and file. The MainController is the base example of the system and stores the other controllers. To run the latest version of the program, run the line of code below. Also, all the arguments listed below can be added to the base command line:
* -ip: IP Address of your hue bridge, string
* -id: Unique username to access hue bridge, string
* -wf: Filename of coded words you want to use, string
* -cf: Filename of color names you want to use, string
* -l: Number of LEDs used in system, int
* -d: If you are using a display, boolean
* -sr: The speech library you are using, string
```
$ sudo bash ./mainStart.sh
```


To run the pervious version of the program, run the following code:
```
$ sudo bash ./speechStart.sh
```

