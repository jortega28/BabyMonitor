__author__ = 'Justin'
#Uses the AudioProcessing py program
#Will create a graph at the end of running the program
#The graphs can be pushed to the web application at some point
#If threshold passed the parent should be emailed or notified in some way

import AudioProcessing as audio
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime
import PIL
from PIL import Image
import os

def sendNotification():
    print "Sending parent a notification..."
    #Insert email code here
    #Possibly send text message

def captureAudioGraph(timeStamp):
    if os.path.isfile('file.csv') is False:
        return "No previous recording found"
    if os.stat("file.csv").st_size == 0:
        return "No data exist in file"
    data1=np.genfromtxt('file.csv', skip_header=1)
    if not len(data1) >= 14400:
        return "Not enough data to create a graph"
    else:
        counter = 0
        willBePlotted = []
        temp = []
        while len(data1) > counter:
            temp.append(data1[counter])
            if len(temp) != 0:
                if (len(temp) % 3600) == 0:
                    tempAvg = sum(temp)/len(temp)
                    willBePlotted.append(tempAvg)
                    temp = []
            counter = counter+1

        plt.figure(figsize=(10,5))
        plt.plot(np.arange(0,len(willBePlotted),1), willBePlotted)
        plt.xlabel("Hours")
        plt.ylabel("Audio Activity")
        plt.title(datetime.datetime.fromtimestamp(timeStamp).strftime('%m-%d-%Y at %H:%M'))
        plt.xticks(np.arange(0,len(willBePlotted),1))
        plt.savefig("graphs/%s.png" % timeStamp)

        w = 600
        h = 375
        img = Image.open("graphs/%s.png" % timeStamp)
        img = img.resize((w,h), PIL.Image.ANTIALIAS)
        img.save("graphs/600x375%s.png" % timeStamp)

        w = 278
        h = 147
        img = Image.open("graphs/%s.png" % timeStamp)
        img = img.resize((w,h), PIL.Image.ANTIALIAS)
        img.save("graphs/278x147%s.png" % timeStamp)

        os.remove("graphs/%s.png" % timeStamp)

        #delete csv file

        return "Graphs successfully created"

if __name__ == "__main__":
    #The while true statement while keep the program running forever
    #At least until CTRL + Z is pressed on keyboard
    #Settings will be declared out here
    BASE_NOISE = 1000
    MAX_NOISE = 0
    sensitivity = "high"
    threshold = 0
    nt = audio.NoiseTester()
    audioData = []
    movementData = []
    lastTime = "None"
    status = "on"
    graphCreated = True
    configured = False
    notifyLevel = 20
    audioNotifyLevel = 0
    motionNotifyLevel = 0
    while True:
        lastTime = time.time()
        while status is "on":
            #Set threshold for audio
            threshold = BASE_NOISE
            if sensitivity is "low":
                threshold = BASE_NOISE * 2.25
            if sensitivity is "medium":
                threshold = BASE_NOISE * 2.0
            else:
                threshold = BASE_NOISE * 1.75
            #Create a timestamp
            #Now take an audio and movement sample
            audioSample, average = nt.listen(threshold)
            if average > 0:
                if average > threshold:
                    print "Average %s " % average + "broke the threshold %s" % threshold
                    if sensitivity is "low":
                        audioNotifyLevel = audioNotifyLevel + 1
                    if sensitivity is "medium":
                        audioNotifyLevel = audioNotifyLevel + 2
                    if sensitivity is "high":
                        audioNotifyLevel = audioNotifyLevel + 3
                    totalNL = audioNotifyLevel + motionNotifyLevel
                    print "The total notify level is now %s" % totalNL
                    if totalNL >= notifyLevel:
                        sendNotification()
                        audioNotifyLevel = 0
                        motionNotifyLevel = 0
            if audioSample < BASE_NOISE:
                BASE_NOISE = audioSample
            if audioSample > MAX_NOISE:
                MAX_NOISE = audioSample
            #print "%s" % audioSample
            audioData.append(audioSample)
            #Now check if we have reached 10 values in our audio data
            #print "%s" % BASE_NOISE
            #print "%s" % MAX_NOISE
            #Here we will say that a graph for this data has not been created
            graphCreated = False
            #Check the status and see if it is still on
            #status = "off"

        if graphCreated is False:
            #Once the status is off try and produce a graph of the file
            #This will also delete the data recorded from the pi
            #Use the last recording time as a variable
            print captureAudioGraph(lastTime)
            #Now that we have created the graph set it to true
            graphCreated = True

        #Check all settings and set them to a value
