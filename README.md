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
```

## Plot Live Microphone
To test the live microphone, you can run the command line below. I have to use 'sudo' to allow access to my microphone:

if you have both python and python3 downloaded
```
$ sudo python3 streamingAudio.py
```

if you have only python3 downloaded
```
$ sudo python streamingAudio.py
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
