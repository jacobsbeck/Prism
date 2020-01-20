try:
    from sys import byteorder
    from array import array
    from struct import pack

    import pyaudio
    import wave
    import keyboard
except:
    print("Something didn't import")

threshold = 500
audio = pyaudio.PyAudio()
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 1024 # 2^12 samples for buffer
record_secs = 1 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'demo.wav' # name of .wav file
microphone_name = 'Logitech USB Microphone' # name of the microphone being used

def main():
    #listAudioSources()
    #initializeMicrophone()

    still_streaming = True
    i = 0
    print("please make a noise in the microphone")
    print("press q to quit")
    while (still_streaming):
        if keyboard.is_pressed('q'):
            still_streaming = False
            break
        else:
            record_to_file("detectedsounds/demo" + i.__str__() + ".wav")
            print("demo" + i.__str__() + " .wav created in detectedsounds folder")
            i += 1
    print("done - result written to demo.wav")

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < threshold

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>threshold:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*samp_rate))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*samp_rate))])
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, output=True, \
                    frames_per_buffer=chunk)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(chunk))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(form_1)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(samp_rate)
    wf.writeframes(data)
    wf.close()

# This method initalizes the audio streaming, specifically determining the index for the microphone
def initializeMicrophone():
    for i in range(audio.get_device_count()):
        if (microphone_name == audio.get_device_info_by_index(i).get('name')):
            dev_index = i

# This method lists the possible audio sources to help determine the specific name of a microphone being used
def listAudioSources():
    for ii in range(audio.get_device_count()):
        print(audio.get_device_info_by_index(ii).get('name'))
        print("Channels = "+str(audio.get_device_info_by_index(ii).get('channels')))

main()