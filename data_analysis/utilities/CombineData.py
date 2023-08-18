import os
os.chdir("../")
os.chdir("../")
cwd = os.getcwd()
print(cwd)

import sys
sys.path.append(cwd)

import sys
sys.path.append("/Users/zacharystarr/Desktop/TrafficMonitoring-usingYOLO/")
import os
os.chdir("/Users/zacharystarr/Desktop/TrafficMonitoring-usingYOLO/")

from datetime import datetime, timedelta
import params
from natsort import os_sorted

folder = params.RawData_Folder
collections = os.listdir("{}/".format(folder))
collections = os_sorted(collections)

def CloneFile(source_filename, dest_filename):
    with open(source_filename, "r") as sourceFile:
        fileContent = sourceFile.read()
    with open(dest_filename, "w") as destinationFile:
        destinationFile.write(fileContent)

def ReadRawTime(rawTime):
    if len(rawTime) < 6:
        x = "0"
        rawTime = x + rawTime
    Time = datetime.strptime(f"{rawTime[:2]}:{rawTime[2:4]}:{rawTime[4:]}", "%H:%M:%S")
    return Time

def ReadItemTime(textItem):
    rawTime = textItem.split(',')[1]
    Time = datetime.strptime(f"{rawTime[:2]}:{rawTime[2:4]}:{rawTime[4:]}", "%H:%M:%S")
    return Time

msg = "Select File: \n"
count = 0
for item in collections:
    msg = msg + "{}: {}".format(count, str(item)) + "\n"
    count += 1
print(msg)

file1 = input("Choose First File: ")
file1 = collections[int(file1)]
file1path = f"{os.getcwd()}/data/raw_data/{file1}"

file1data = file1.split(',')
adjusterTime = ReadRawTime(file1data[2].replace(":",""))
adjusterTime = timedelta(0, adjusterTime.second, 0, 0, adjusterTime.minute, adjusterTime.hour)
startTime = file1data[3]

with open(file1path, "r") as f:
    lines1 = f.readlines()
startCount = len(lines1)

file2 = input ("Choose Second File: ")
file2 = collections[int(file2)]
file2path = f"{os.getcwd()}/data/raw_data/{file2}"

file2data = file2.split(',')
file2CloneData = file2data
file2CloneData[0] = file1data[0]
file2CloneData[1] = str(int(file2data[1]) + startCount)
file2CloneData[2] = str((ReadRawTime(file2CloneData[2].replace(":", "")) + adjusterTime).time())
file2CloneData[3] = startTime
file2cloneName = ','.join(file2CloneData)

combinedFile = f"{os.getcwd()}/data/raw_data/{file2cloneName}"

CloneFile(file2path, f"{os.getcwd()}/data/raw_data/{file2cloneName}")

with open(file1path, "r") as f:
    lines1 = f.readlines()
with open(combinedFile, "r") as g:
    lines2 = g.readlines()
with open(combinedFile, "w") as file:
    pass
with open(combinedFile, "a") as file:
    for item in lines1:
        file.write(item)
    for item in lines2:
        itemdata = item.split(',')
        itemNum = itemdata[0]
        itemNum = itemdata[0] = str(int(itemNum) + startCount)
        itemTime = ReadRawTime(itemdata[1])
        itemTime = str((itemTime + adjusterTime).time()).replace(":", "")
        itemdata[1] = itemTime
        item = ','.join(itemdata)
        file.write(item)
    print("done!")