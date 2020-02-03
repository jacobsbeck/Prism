# Prism
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Plot Live Microphone](#plot-live-microphone)
* [Classify Clap](#classify-clap)

## General info
This is the project Prism, created for the Interactive Media Design Capstone at University of Washington Bothell.
	
## Technologies
Project is created with:
* Python 3.6
* numpy
* librosa
* pysoundfile
* sounddevice
* matplotlib
* scikit-learn
* tensorflow
* keras
* pyaudio
* wave
* keyboard
	
## Setup
To run this project, install the appropriate packages:
```
$ pip3 install numpy
$ pip3 install librosa
$ pip3 install pysoundfile
$ pip3 install sounddevice
$ pip3 install matplotlib
$ pip3 install scikit-learn
$ pip3 install tensorflow
$ pip3 install keras
$ pip3 install pyaudiio
$ pip3 install wave
$ pip3 install keyboard
```

## Plot Live Microphone
To test the live microphone, you can run the command line below. I have to use 'sudo' to allow access to my microphone:
```
$ sudo python3 streamingAudio.py
```

## Classify Clap
Before you can start classifying a live microphone or wave file, we need to train it:
```
$ python3 audioClassification/cnn.py -t
```
Predict files by either:
* Putting target files under the audioClassification/predict/ directory
```
$ python3 audioClassification/cnn.py -p
```
* Recording on the fly
```
$ python3 audioClassification/cnn.py -P
```
