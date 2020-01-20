try:
    import pyaudio
except:
    print("Something didn't import")

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 0 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test.wav' # name of .wav file
microphone_name = 'Logitech USB Microphone'

def main():
    initializeMicrophone()

def initializeMicrophone():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        if (microphone_name == p.get_device_info_by_index(i).get('name')):
            dev_index = i
main()