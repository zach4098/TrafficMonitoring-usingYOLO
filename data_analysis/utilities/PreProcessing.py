import os
while 'data_analysis' in os.getcwd():
    os.chdir("../")
    print("<--")
cwd = os.getcwd()

import sys
sys.path.append(cwd)

import params
from natsort import os_sorted
from datetime import datetime, timedelta

def itemType(line):
    vehicleType = line.split(',')[3]
    return int(vehicleType)
def itemTime(line):
    rawTime = line.split(',')[1]
    Time = datetime.strptime(f"{rawTime[:2]}:{rawTime[2:4]}:{rawTime[4:]}", "%H:%M:%S")
    return Time

folder = params.RawData_Folder
collections = os.listdir("{}/".format(folder))
collections = os_sorted(collections)

msg = "Select File: \n"
count = 0
for item in collections:
    msg = msg + "{}: {}".format(count, str(item)) + "\n"
    count += 1
print(msg)

file = input("Choose File: ")
file = collections[int(file)]
filepath = f"{os.getcwd()}/data/raw_data/{file}"

with open (filepath, "r") as f:
    lines = f.readlines()

phonyCounter = 0
markedItems = []

for line in lines:
    if itemType(line) == 1 or itemType(line) == 3:
        time = itemTime(line)
        if itemType(lines[lines.index(line) + 1]) == 0:
            time2 = itemTime(lines[lines.index(line) + 1])
            if time == time2 and lines.index(line)+1 not in markedItems:
                markedItems.append(lines.index(line) + 1)
                phonyCounter += 1
    if itemType(line) == 0:
        time = itemTime(line)
        if len(lines) > lines.index(line) + 1:
            if itemType(lines[lines.index(line) + 1]) == 1 or itemType(lines[lines.index(line)+1]) == 3:
                time2 = itemTime(lines[lines.index(line) + 1])
                if time == time2 and lines.index(line) not in markedItems:
                    markedItems.append(lines.index(line))
                    phonyCounter += 1

lines = [i for i in lines if lines.index(i) not in markedItems]
print(len(lines))

with open(filepath, "w") as f:
    f.writelines(lines)

metadata = file.split(',')
metadata[1] = str(len(lines))
file = ",".join(metadata)
os.rename(filepath, f"{os.getcwd()}/data/raw_data/{file}")