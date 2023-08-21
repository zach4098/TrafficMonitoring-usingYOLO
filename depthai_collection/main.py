import sys
sys.path.append("/home/fyp2022/Desktop/TrafficMonitoring-usingYOLO")
import os
os.chdir("/home/fyp2022/Desktop/TrafficMonitoring-usingYOLO")

import cv2
import depthai as dai
import numpy as np
import time as time1
from time import time, ctime
import blobconverter
from pynput import mouse
import params
import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

labelMap = [
    "pedestrian",     "bicycle",    "car",           "motorbike",     "aeroplane",   "bus",           "train",
    "truck",          "boat",       "traffic light", "fire hydrant",  "stop sign",   "parking meter", "bench",
    "bird",           "cat",        "dog",           "horse",         "sheep",       "cow",           "elephant",
    "bear",           "zebra",      "giraffe",       "backpack",      "umbrella",    "handbag",       "tie",
    "suitcase",       "frisbee",    "skis",          "snowboard",     "sports ball", "kite",          "baseball bat",
    "baseball glove", "skateboard", "surfboard",     "tennis racket", "bottle",      "wine glass",    "cup",
    "fork",           "knife",      "spoon",         "bowl",          "banana",      "apple",         "sandwich",
    "orange",         "broccoli",   "carrot",        "hot dog",       "pizza",       "donut",         "cake",
    "chair",          "sofa",       "pottedplant",   "bed",           "diningtable", "toilet",        "tvmonitor",
    "laptop",         "mouse",      "remote",        "keyboard",      "cell phone",  "microwave",     "oven",
    "toaster",        "sink",       "refrigerator",  "book",          "clock",       "vase",          "scissors",
    "teddy bear",     "hair drier", "toothbrush"
]

allowedLabels = params.allowedLabels

def getAllowedItems(items):
    whiteList = []
    for i in items:
        if i in labelMap:
            whiteList.append(labelMap.index(i))
        if i not in labelMap:
            print("could not find {} in the label map!".format(i))
    return whiteList

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    deltaTime = datetime.time(hours, mins, sec)
    deltaTime = str(deltaTime).replace(':', '')
    return deltaTime

# Create pipeline
pipeline = dai.Pipeline()

nnPath = blobconverter.from_openvino(params.nnPathXml, params.nnPathBin, shaves=6)

t = time()
timeOfCreation = str(ctime(t))
timeInit = t

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
detectionNetwork = pipeline.create(dai.node.YoloDetectionNetwork)
objectTracker = pipeline.create(dai.node.ObjectTracker)

xlinkOut = pipeline.create(dai.node.XLinkOut)
trackerOut = pipeline.create(dai.node.XLinkOut)

xlinkOut.setStreamName("preview")
trackerOut.setStreamName("tracklets")

# Properties
camRgb.setPreviewSize(416, 416)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
camRgb.setFps(30)

detectionNetwork.setConfidenceThreshold(0.5)
detectionNetwork.setNumClasses(80)
detectionNetwork.setCoordinateSize(4)
detectionNetwork.setAnchors([10, 14, 23, 27, 37, 58, 81, 82, 135, 169, 344, 319])
detectionNetwork.setAnchorMasks({"side26": [1, 2, 3], "side13": [3, 4, 5]})
detectionNetwork.setIouThreshold(0.5)
detectionNetwork.setBlobPath(nnPath)
detectionNetwork.setNumInferenceThreads(2)
detectionNetwork.input.setBlocking(False)

objectTracker.setDetectionLabelsToTrack(getAllowedItems(allowedLabels))  # track only person
# possible tracking types: ZERO_TERM_COLOR_HISTOGRAM, ZERO_TERM_IMAGELESS, SHORT_TERM_IMAGELESS, SHORT_TERM_KCF
objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
# take the smallest ID when new object is tracked, possible options: SMALLEST_ID, UNIQUE_ID
objectTracker.setTrackerIdAssignmentPolicy(dai.TrackerIdAssignmentPolicy.SMALLEST_ID)

# Linking
camRgb.preview.link(detectionNetwork.input)
objectTracker.passthroughTrackerFrame.link(xlinkOut.input)


#camRgb.preview.link(objectTracker.inputTrackerFrame)
detectionNetwork.passthrough.link(objectTracker.inputTrackerFrame)

detectionNetwork.passthrough.link(objectTracker.inputDetectionFrame)
detectionNetwork.out.link(objectTracker.inputDetections)
objectTracker.out.link(trackerOut.input)


GPIO.output(14, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)
leftRight = params.leftRight
def click(x, y, button, pressed):
    global leftRight
    if str(button) == "Button.left" and leftRight is not True:
        leftRight = True
        GPIO.output(23, GPIO.HIGH)
        time1.sleep(0.1)
        GPIO.output(23, GPIO.LOW)
    elif str(button) == "Button.right" and leftRight is not False:
        leftRight = False
        GPIO.output(23, GPIO.HIGH)
        time1.sleep(0.1)
        GPIO.output(23, GPIO.LOW)
        time1.sleep(0.1)
        GPIO.output(23, GPIO.HIGH)
        time1.sleep(0.1)
        GPIO.output(23, GPIO.LOW)

listener = mouse.Listener(on_click=click)
listener.start()

showOutput = params.showOutput

if params.calibrate:
    time1.sleep(45)

GPIO.output(14, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)
time1.sleep(0.2)
GPIO.output(14, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
time1.sleep(0.2)
GPIO.output(14, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)
time1.sleep(0.2)
GPIO.output(14, GPIO.LOW)
GPIO.output(23, GPIO.LOW)

count = 1
for item in os.listdir(f"{params.directory}/data/raw_data"):
    count += 1
data_name = f"Data Sample {count}"

dataCollected = False

# Connect to device and start pipeline
try:
    with dai.Device(pipeline) as device:

        GPIO.output(14, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)

        preview = device.getOutputQueue("preview", maxSize=4, blocking=False)
        tracklets = device.getOutputQueue("tracklets", maxSize=4, blocking=False)

        startTime = time1.monotonic()
        counter = 0
        fps = 0
        frame = None

        sensorBox = params.SensorBox
        sensorBoxY = params.SensorBoxY

        leftBox = params.leftBox
        rightBox = params.rightBox

        bottomBox = params.bottomBox
        upperBox = params.upperBox

        vehicles = []
        totalVehicles = 0

        vehicleDir = None

        while(True):
            timer = round(time1.monotonic())
            try:
                imgFrame = preview.get()
                track = tracklets.get()
            except:
                imgFrame = preview.tryGet()
                track = tracklets.tryGet()

            counter+=1
            current_time = time1.monotonic()
            if (current_time - startTime) > 1 :
                fps = counter / (current_time - startTime)
                counter = 0
                startTime = current_time

            color = (255, 0, 0)
            yellow = (255, 255, 0)
            frame = imgFrame.getCvFrame()
            trackletsData = track.tracklets
            for t in trackletsData:
                roi = t.roi.denormalize(frame.shape[1], frame.shape[0])
                x1 = int(roi.topLeft().x)
                y1 = int(roi.topLeft().y)
                x2 = int(roi.bottomRight().x)
                y2 = int(roi.bottomRight().y)

                bbox = [x1, y1, x2, y2]

                global midpoint
                midpoint = (x1+x2)/2
                midpoint = int(round(midpoint))

                global midpointY
                midpointY = (bbox[1] + bbox[3])/2
                midpointY = int(round(midpointY))

                vehicleID = t.id
                vehicleStatus = str(t.status.name)

                labelID = t.label

                try:
                    label = labelMap[t.label]
                except:
                    label = t.label

                if leftRight:
                    if vehicleStatus == "NEW" and bbox[2] <= leftBox[1]:
                        vehicleDir = 0
                    elif vehicleStatus == "NEW" and bbox[0] >= rightBox[0]:
                        vehicleDir = 1
                    if vehicleID not in vehicles and sensorBox[0] <= midpoint <= sensorBox[1]:
                        if vehicleStatus == "TRACKED":
                            t = time()
                            currentTime = datetime.datetime.now()
                            stopwatchTime = round(t - timeInit)
                            vehicles.append(vehicleID)
                            totalVehicles += 1
                    if vehicleStatus == "REMOVED" or sensorBox[0] > midpoint or sensorBox[1] < midpoint:
                        if vehicleID in vehicles:
                            endTime = datetime.datetime.now()
                            speedTime = endTime - currentTime
                            secondDelta = speedTime.total_seconds()
                            speedRating = (params.SensorBoxWidth/secondDelta)
                            speedRating = round(speedRating*3.6)
                            #speedRating = round(((1/secondDelta) * 0.2)*params.SensorBoxWidth)
                            with open(f"./data/raw_data/{data_name}.txt", "a") as fp:
                                fp.write("{},{},{},{},{}\n".format(totalVehicles, time_convert(stopwatchTime), vehicleDir, labelID, speedRating))
                            dataCollected = True
                            vehicles.remove(vehicleID)
                elif not leftRight:
                    if vehicleStatus == "NEW" and bbox[1] <= upperBox[1]:
                        vehicleDir = 0
                    elif vehicleStatus == "NEW" and bbox[3] >= bottomBox[0]:
                        vehicleDir = 1

                    if vehicleID not in vehicles and sensorBoxY[0] <= midpointY <= sensorBoxY[1]:
                        if vehicleStatus == "TRACKED":
                            t = time()
                            currentTime = datetime.datetime.now()
                            stopwatchTime = round(t - timeInit)
                            vehicles.append(vehicleID)
                            totalVehicles += 1
                    if vehicleStatus == "REMOVED" or sensorBoxY[0] > midpointY or sensorBoxY[1] < midpointY:
                        if vehicleID in vehicles:
                            endTime = datetime.datetime.now()
                            speedTime = endTime - currentTime
                            secondDelta = speedTime.total_seconds()
                            speedRating = (params.SensorBoxWidth/secondDelta)
                            speedRating = round(speedRating*3.6)
                            #speedRating = round((0.5/(secondDelta/2) * 0.2)*params.SensorBoxYHeight)
                            with open(f"./data/raw_data/{data_name}.txt", "a") as fp:
                                fp.write("{},{},{},{},{}\n".format(totalVehicles, time_convert(stopwatchTime), vehicleDir, labelID, speedRating))
                            dataCollected = True
                            vehicles.remove(vehicleID)

                if len(vehicles) != 0:
                        GPIO.output(23, GPIO.HIGH)
                elif len(vehicles) == 0:
                    GPIO.output(23, GPIO.LOW)
                if showOutput:
                    cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    #cv2.putText(frame, f"{vehicleDir}", (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    #cv2.putText(frame, vehicleStatus, (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)
            if showOutput:
                if leftRight:
                    cv2.rectangle(frame, (sensorBox[0], 0), (sensorBox[1], 416), (0, 0, 255), 1)
                    cv2.rectangle(frame, (leftBox[0], 0), (leftBox[1], 416), yellow, 1)
                    cv2.rectangle(frame, (rightBox[0], 0), (rightBox[1], 416), yellow, 1)
                elif not leftRight:
                    cv2.rectangle(frame, (0, sensorBoxY[0]), (416, sensorBoxY[1]), (0, 0, 255), 1)
                    cv2.rectangle(frame, (0, bottomBox[0]), (416, bottomBox[1]), yellow, 1)
                    cv2.rectangle(frame, (0, upperBox[0]), (416, upperBox[1]), yellow, 1)

                cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.7, color)

                cv2.imshow("tracker", cv2.resize(frame, (1000, 1000)))  
            if (timer % 2) == 0:
                    GPIO.output(14, GPIO.HIGH)
            elif (timer % 2) != 0:
                GPIO.output(14, GPIO.LOW)

            cv2.waitKey(1)
except:
    if dataCollected:
        GPIO.output(14, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        time1.sleep(1)
        try:
            if os.path.isfile(f"{params.directory}/data/raw_data/{data_name}.txt"):
                total = 0
                time = None
                with open(f"{params.directory}/data/raw_data/{data_name}.txt", "r") as f:
                    lines = f.readlines()
                    total = len(lines)
                    time = lines[len(lines) - 1].split(',')[1]
                    time = f"{time[:2]}:{time[2:4]}:{time[4:]}"
                new_name = data_name + ",{},{}".format(total, time)
                os.rename(f"{params.directory}/data/raw_data/{data_name}.txt", f"{params.directory}/data/raw_data/{new_name}.txt")
            else:
                print("failed to rename!")
                for i in range (3):
                    GPIO.output(23, GPIO.HIGH)
                    time1.sleep(0.5)
                    GPIO.output(23, GPIO.LOW)
                    time1.sleep(0.5)
        except:
            print("failed to rename!")
            for i in range (3):
                GPIO.output(23, GPIO.HIGH)
                time1.sleep(0.5)
                GPIO.output(23, GPIO.LOW)
                time1.sleep(0.5)
        for i in range (5):
            GPIO.output(14, GPIO.HIGH)
            time1.sleep(0.1)
            GPIO.output(14, GPIO.LOW)
            time1.sleep(0.1)
    elif not dataCollected:
        print("error! check if camera is plugged in!")
        for i in range (5):
            GPIO.output(23, GPIO.LOW)
            time1.sleep(0.1)
            GPIO.output(23, GPIO.HIGH)
            time1.sleep(0.1)
        GPIO.output(23, GPIO.LOW)
    print("done!")