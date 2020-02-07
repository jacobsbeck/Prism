# Prism
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Classify Clap](#classify-clap)
* [Speech Recognition](#speech-recognition)
* [Light Pattern Testing](#light-pattern-testing)

## General info
Hello! This is the project Prism, created for the Interactive Media Design 2020 Capstone at the University of Washington Bothell. This project uses a Raspberry Pi 4 and a Blue Snowball microphone to manipulate lights. This project utilizes audio classification, noise cancellation, and machine learning to create a unique audio to light expereince. The audio calssification model I used for this project is based off of [this](https://github.com/mtobeiyf/audio-classification) project I found during my research.
	
## Technologies
Project is created with:
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
```

## Classify Clap
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

## Light Pattern Testing
```
$ sudo ./testpatternStart.sh
```

