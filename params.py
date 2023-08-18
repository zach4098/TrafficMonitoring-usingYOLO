directory = "/home/fyp2022/Desktop/TrafficMonitoring-usingYOLO"
RawData_Folder = "data/raw_data"
SpreadsheetFolder = "data/data_spreadsheet"
SpreadsheetName = "data.xlsx"

MorningPeakStart = "083000"
MorningPeakEnd = "103000"
NightPeakStart = "173000"
NightPeakEnd = "210000"

leftRight = False
showOutput = True
calibrate = not showOutput

SensorBox = [188, 228]
SensorBoxWidth = (SensorBox[1] - SensorBox[0])/20

SensorBoxY = [188 - 80, 228 - 80]
SensorBoxYHeight = (SensorBoxY[1] - SensorBoxY[0])/20

allowedLabels = ["bicycle", "car", "motorbike", "bus", "truck"]

nnPathXml = "./neural_networks/YOLOv6t_COCO/yolov6t_coco_416x416.xml"
nnPathBin = "./neural_networks/YOLOv6t_COCO/yolov6t_coco_416x416.bin"

"""nnPathXml = "./neural_networks/YOLOv4_tiny_COCO/yolov4_tiny_coco_416x416.xml"
nnPathBin = "./neural_networks/YOLOv4_tiny_COCO/yolov4_tiny_coco_416x416.bin"""

def midpoint(p1, p2):
    return int((p1+p2)/2)

leftBox = [0, midpoint(SensorBox[0], SensorBox[1])]
rightBox = [midpoint(SensorBox[0], SensorBox[1]), 416]

bottomBox = [midpoint(SensorBoxY[0], SensorBoxY[1]), 416]
upperBox = [0, midpoint(SensorBoxY[0], SensorBoxY[1])]