import pyaudio
import struct
import math
import numpy as np
import scipy.io.wavfile
import scipy.fftpack

INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0 / 32768.0)
CHANNELS = 2
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)

OVERSENSITIVE = 15.0 / INPUT_BLOCK_TIME

UNDERSENSITIVE = 120.0 / INPUT_BLOCK_TIME  # if we get this many quiet blocks in a row, decrease the threshold

MAX_TAP_BLOCKS = 0.15 / INPUT_BLOCK_TIME  # if the noise was longer than this many blocks, it's not a 'tap'


def fft_array(Fs, Data):
    y = Data / 32767.0
    avg = np.abs(np.average(y))
    dB = 160 + (20 * np.log10(avg))
    # print (dB)
    # if dB < 68.0:
    #     print ("Halk")
    # else:
    #     print ("Hangos")


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
    # if thefreq < 850: #Hzben
    #     print "Mely"
    # elif thefreq > 900:
    #     print "Magas"
    return None


def get_rms(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)
    fft_array(RATE, np.array(shorts))
    return None


pa = pyaudio.PyAudio()  # ]
# |
stream = pa.open(format=FORMAT,  # |
                 channels=CHANNELS,  # |---- You always use this in pyaudio...
                 rate=RATE,  # |
                 input=True,  # |
                 frames_per_buffer=INPUT_FRAMES_PER_BLOCK)  # ]

tap_threshold = INITIAL_TAP_THRESHOLD  # ]
noisycount = MAX_TAP_BLOCKS + 1  # |---- Variables for noise detector...
quietcount = 0  # |
errorcount = 0  # ]

for i in range(1000):
    try:  # ]
        block = stream.read(INPUT_FRAMES_PER_BLOCK)  # |
    except IOError, e:  # |---- just in case there is an error!
        errorcount += 1  # |
        print("(%d) Error recording: %s" % (errorcount, e))  # |
        noisycount = 1  # ]

    get_rms(block)
