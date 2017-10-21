import pyaudio
import struct
import math
import numpy as np
import scipy.io.wavfile
import scipy.fftpack

INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)


def fft_array(Fs, Data):
    y = Data / 32767.0
    avg = np.abs(np.average(y))
    dB = 160 + (20 * np.log10(avg))
    # print (dB)
    if dB < 73.0:
        print("Halk")
    else:
        print("Hangos")

    RATE = Fs
    chunk = len(Data)
    fftData = abs(np.fft.rfft(Data)) ** 2
    which = fftData[1:].argmax() + 1
    thefreq = 0.0
    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        thefreq = (which + x1) * RATE / chunk
    else:
        thefreq = which * RATE / chunk
    print
    thefreq * 2
    if thefreq < 400:  # Hzben
        print
        "Mely"
    elif thefreq > 450:
        print
        "Magas"
    return None


def get_rms(block):
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)
    fft_array(RATE, np.array(shorts))
    return None


pa = pyaudio.PyAudio()

stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

while True:
    try:
        block = stream.read(INPUT_FRAMES_PER_BLOCK)
    except IOError, e:
        pass
    get_rms(block)
