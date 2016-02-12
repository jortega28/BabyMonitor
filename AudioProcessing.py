__author__ = 'Justin'

import pyaudio
import struct
import math
import time
import random

# open a microphone in pyAudio and listen for sounds

FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.10
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
#278 x 147
#600 x 375

def get_rms( block ):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class NoiseTester(object):
    values = []
    amplitude = 0.001
    noise_threshold = 1000
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.quietcount = 0
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    device_index = i
                    return device_index

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def noiseDetected(self, avg):
        #print "Noise detected!"
        #print(avg)
        #print(self.noise_threshold)
        with open("file.csv","a+") as f:
            f.writelines("%s" % avg+"\n")
            self.values = []
            self.values.append(avg)
            f.close()

    def listen(self,threshold):
        self.noise_threshold = threshold

        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            #Use the statement below for troubleshooting
            print( "(%d) Error recording: %s"%(self.errorcount,e) )

        self.amplitude = get_rms(block)
        self.amplitude = round(self.amplitude, 3)

        if self.amplitude > threshold*2:
            self.amplitude = self.noise_threshold + (self.noise_threshold/4)

        if len(self.values) == 10:
            avg = sum(self.values)/10
            if avg < self.noise_threshold:
                with open("file.csv","a+") as f:
                    avg = sum(self.values)/10
                    f.writelines("%s" % avg+"\n")
                    self.values = []
                    self.values.append(self.amplitude)
                    f.close()
            if avg >= self.noise_threshold:
                self.noiseDetected(avg)
            print "The current noise level is " + "%s" % avg
            return self.amplitude, avg
        else:
            self.values.append(self.amplitude)

        return self.amplitude, 0

if __name__ == "__main__":
    nt = NoiseTester()
    status = "on"
    timer = 0

    while status is "on":
        nt.listen()