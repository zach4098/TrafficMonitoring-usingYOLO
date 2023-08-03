directory = "/home/fyp2022/Desktop/TrafficMonitoring-usingYOLO"
RawData_Folder = "data/raw_data"
SpreadsheetFolder = "data/data_spreadsheet"
SpreadsheetName = "data.xlsx"

MorningPeakStart = "083000"
MorningPeakEnd = "103000"
NightPeakStart = "173000"
NightPeakEnd = "210000"

SensorBox = [188, 228]
SensorBoxY = [188 - 40, 228 - 40]

allowedLabels = ["bicycle", "car", "motorbike", "bus", "truck"]

nnPathXml = "./neural_networks/YOLOv4_tiny_COCO/yolov4_tiny_coco_416x416.xml"
nnPathBin = "./neural_networks/YOLOv4_tiny_COCO/yolov4_tiny_coco_416x416.bin"