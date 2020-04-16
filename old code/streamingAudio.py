try:
    from sys import byteorder
    from array import array
    from struct import pack

    import pyaudio
    import wave
    import numpy as np
    import matplotlib.pyplot as plt
except:
    print("Something didn't import")

# Variables ---------------------------------------
threshold = 500
audio = pyaudio.PyAudio()
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 48000 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
dev_index = 0 # device index found by p.get_device_info_by_index(i)
wav_output_filename = 'demo.wav' # name of .wav file
#microphone_name = 'Logitech USB Microphone' # name of the microphone being used
microphone_name = 'Blue Snowball' # name of the microphone being used

for i in range(audio.get_device_count()):
    if (microphone_name == audio.get_device_info_by_index(i).get('name')):
        dev_index = i

# Initalize Plots ---------------------------------
f,ax = plt.subplots(2)
# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)
# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,5000)
ax[1].set_ylim(-100,100)
ax[1].set_title("Fast Fourier Transform")
# Show the plot, but without blocking updates
plt.tight_layout()
plt.subplots_adjust(hspace=0.3)
plt.pause(0.01)

# Functions ------------------------------------------
def callback(in_data, frame_count, time_info, status):
    # get and convert the data to float
    audio_data = np.fromstring(in_data, np.int16)
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))
    
    # Force the new data into the plot, but without redrawing axes.
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)
    
    # Show the updated plot, but without blocking
    plt.pause(0.01)
    return (in_data, pyaudio.paContinue)

def main():
    listAudioSources()

    still_streaming = True
    i = 0
    print("please make a noise in the microphone")
    while (still_streaming):
        try: 
            record_to_file("detectedsounds/demo" + i.__str__() + ".wav")
            print("demo" + i.__str__() + " .wav created")
            i += 1
        except KeyboardInterrupt:
            break
    print("done - results written to the folder detectedsounds")
     
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
    #stream = p.open(format = form_1,rate = samp_rate,channels = chans, \
    #                input_device_index = dev_index,input = True, output=True, \
    #                frames_per_buffer=chunk)
    stream = p.open(format=form_1,
                channels=chans,
                rate=samp_rate,
                frames_per_buffer=chunk,
                input=True)


    num_silent = 0
    snd_started = False

    r = array('h')
    while 1:
        # little endian, signed short
        #plot_data(stream.read(chunk))
        data = stream.read(chunk, exception_on_overflow = False)
        snd_data = array('h', data)
        #plot_data(data)
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
        # get and convert the data to float
        audio_data = np.fromstring(data, np.int16)
        # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
        # and make sure it's not imaginary
        dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))
        
        # Force the new data into the plot, but without redrawing axes.
        li.set_xdata(np.arange(len(audio_data)))
        li.set_ydata(audio_data)
        li2.set_xdata(np.arange(len(dfft))*10.)
        li2.set_ydata(dfft)
        
        # Show the updated plot, but without blocking
        plt.pause(0.01)

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

# This method lists the possible audio sources to help determine the specific name of a microphone being used
def listAudioSources():
    for ii in range(audio.get_device_count()):
        print(audio.get_device_info_by_index(ii).get('name'))
        print("Channels = "+str(audio.get_device_info_by_index(ii).get('channels')))

def plot_data(in_data):
    # get and convert the data to float
    audio_data = np.fromstring(in_data, np.int16)
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))
    
    # Force the new data into the plot, but without redrawing axes.
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)
    
    # Show the updated plot, but without blocking
    plt.pause(0.01)

main()