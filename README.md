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
* Wifi Extendor
* LED Strip
* Hue Bridge and Lights
* Personal Hotspot

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

To setup the hardware, you must begin by configuring your personal hotspot and wifi extendor. Once your personal network is working with your extendor, connect your hue bridge with ethernet to your wifi extendor and then connect your raspberry pi with wifi to your extendor. From there you must determine the bridges ip address and change the ip address of the bridge in the code. Then run the code below and see if the lights start to flash:
```
$ python exampleHueTesting.py
```

## Sound Classification
Before you can start classifying a live microphone, we need to train it:
```
$ sudo ./train.sh
```
* After we train the classifier, you can run the program:
```
$ sudo ./start.sh
```

## Speech Recognition
```
$ sudo ./speechStart.sh
```

