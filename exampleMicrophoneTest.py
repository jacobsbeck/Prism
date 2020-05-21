import speech_recognition as sr
import wave

r = sr.Recognizer()

sampleRate = 44100.0 
while True:
        mic = sr.Microphone()
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                print("recording..")
                audio = r.listen(source)
                o = wave.open('demo3.wav', 'w')
                o.setnchannels(1)
                o.setsampwidth(2)
                o.setframerate(sampleRate)
                o.writeframesraw(audio.get_raw_data())
                o.close()
                break
            
        except KeyboardInterrupt:
            break