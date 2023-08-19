# TrafficMonitoring-usingYOLO
## Setup
For how to set up and use this project, see [SETUP.md](SETUP.md)
## Research Documentation
Research Documentation can be found [here](research_journals/), with studies on each area surveyed.
## Project Overview
### Context
Singapore is a densely populated city, and as a result much effort is put in by the government in order to create road infrastructure that safely and effectively controls traffic. However, peak hours still result in high car density, which can vary depending on the intersection.

Being able to collect data on traffic such as vehicles per hour, speed, and even type of vehicle can provide valuable insight into how to increase road efficiency. For instance, it is shown that vehicle size has a larger correlation with congestion than vehicle speed. Being able to record data showing many trucks can help show the average size of a vehicle.

### Objective
This project aims to collect traffic flow data at busy roads and intersections. This data can be used to determine when traffic density spikes, and which intersections are busiest. 

In order to collect accurate data in various settings, Luxonis' [Oak-1 Lite Depth-AI camera](https://docs.luxonis.com/projects/hardware/en/latest/pages/NG9096/) was used. This is a high-resolution camera which employs on-chip machine learning, allowing it to efficiently run real-time computer vision programs, even on smaller computers such as a Raspberry Pi. Therefore, this solution is very lightweight and can be easily compacted, allowing for an easy yet reliable setup

Collect Traffic Data using Oak-1 Lite Depth-AI Camera and YOLO-v4-tiny MobileNetV2 Neural Network

### Concept
There are 3 points of emphasis in this project: **Accuracy, Efficiency,** and **Compatability**. 

In order to collect meaningful data, the method of collection must be sound. This means that when counting cars moving through traffic, the Depth-AI camera should be able to count the vehicle without missing it or double-counting it, as well as record it with enough information to be used later. Ideally, the neural network employed should be able to distinguish between vehicle types as well.

While accuracy is a significant part of the project, it is rendered useless if the program is not efficient. Luxonis' Depth-AI module uses a pipeline-based model in order to initiate active object detection and machine learning. Without proper setup, numerous problems can occur, such as low framerates and data overload. These can result in programs crashing and miscounting.

Compatability, or variablity, is also very important for this project. The intention is to be able to simply set up the camera and power it on at any street, with any vehicle at any time. Therefore, it is important that this project can acheive results in a variety of conditions, whether that be on the side of a street or on an overhead bridge.

### Structure
In order to acheive these 3 points of emphasis, my project is set up in the following structure:
1. Data collection by Oak-1 Lite camera, data written in .csv format into .txt file. This program runs on RPi autostart
2. .txt files stored in [raw_data](data/raw_data) folder with the following convention: Data Sample #,# of vehicles,time elapsed,time started
3. Post-collection, programs that compile the raw data into legible forms such as spreadsheets and graphs can be ran, which offer user configurability

Further notes on research/project progress can be found [here](research_journals/NOTEBOOK.md)

## Data Collection

**Important Note on Data Collection:** The data collected in this project is ***completely anonymous*** due to the following reasons:
1. The Depth-AI Camera does not record video
2. No license plate data is collected
3. When collecting data, the Raspberry Pi is not connected to any devices via Bluetooth of Wi-Fi

### Data Samples
Each sample collection is analyzed in seperate notebooks:

1. [Corporation Road](research_journals/corporation.md)
2. [Westgate Mall](research_journals/westgate.md)