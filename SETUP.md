# Setup
To use this repository as a method of data collection, there are some prerequisites.
## Equipment
The necessary equipment for this project is as follows:

1. Luxonis OAK-1 Lite Depth-AI Camera
2. Camera Tripod (This project used Sunpak 2001UT Tripod)
3. Raspberry Pi 4 Model B (Does **not** work with earlier versions)
4. Rechargeable Power Bank (**5V 2.1A**, 10,000-20,000 mAh, USB-C PD)
5. Cables
 * USB 3.0 -> USB-C
 * USB-C -> USB-C
6. 2 Arduino LED's soldered with wires and resistors - connected to GPIO 14 and GPIO 23 **(OPTIONAL)**
7. Necessary Computer Peripherals for RPi (Mouse, Keyboard, Monitor)

## Software Setup
All necessary code and programs can be found in this repository:

    git clone https://github.com/zach4098/TrafficMonitoring-usingYOLO.git

**Note:** Make sure to adjust the directories in [params.py](params.py) - it is set up for a RPi with the name "pi"

### Python Modules
See [requirements.txt](requirements.txt) for Python Modules needed

    pip install -r requirements.txt

### Autostart
You can autostart the [main.py](depthai_collection/main.py) program in many different ways, but this is how it was done with this project:
#### Starting LXTerminal on startup
1. Navigate to /home/pi/.config/lxsession/LXDE-pi/autostart
 * If the directory does not exist, you can simply create your own folder/autostart file
2. Input the following command:

        nano autostart
3. Configure your autostart file to look like the following:

        @lxpanel --profile LXDE-pi
        @pcmanfm --desktop --profile LXDE-pi
        point-rpi
        @lxterminal
4. Close autostart file

#### Running [main.py](depthai_collection/main.py) on LXTerminal start
1. In terminal, enter

    ```bash
    sudo nano /home/pi/.bashrc
    ```
2. Scroll to the very bottom of the file.
3. In .bashrc file, enter

    ```bash
    echo running on startup    # optional
    python3 /home/pi/Desktop/TrafficMonitoring-usingYOLO/depthai_collection/main.py
    ```
      
4. Save and close all files

## Hardware Setup
Once software setup is complete and working, the hardware setup of this project is straightforward.

**Note:** It is best to have an understanding of the area you wish to survey before this step - you can configure the sensor box in [params.py](params.py) to fit the situation beforehand.

Once you reach your destination, whether it be overhead bridge or any roadside, follow these steps:
1. Setup tripod to optimal height
2. Connect Depth-AI camera to Raspberry Pi (using **USB 3.0** port & cable)
 * Optional - To configure the axis of the sensor box, connect a mouse: left button = left->right, right button = up->down
3. Plug Raspberry Pi into power bank

<font size="1.5">See - fairly straightforward! </font>

### IMPORTANT:

Once done recording, make sure to **unplug the Depth-AI Camera first**, then wait for 5-10 seconds. This is to ensure that your data is saved and named properly.

## LED Signals
If you added the LEDs in GPIO 14 and GPIO 23, there are certain signals for troubleshooting/ease of mind:

* **Both LEDs on for ~45 seconds:** This is simply to give time for the RPi to recognize and connect to the Depth-AI camera.

* **GPIO 14 LED blinks on and off continuously:** This shows that the Depth-AI camera is at work and recording.

* **GPIO 23 LED flashes:** The LED will turn on whenever it sees a vehicle in the sensor box zone. This flash can vary in length, depending on vehicle speed.

* **GPIO 14 LED flashes 4 times:** This appears only after unplugging the Depth-AI camera. It signifies that your data has been saved and named properly. You are now safe to unplug the RPi.

* **GPIO 23 LED flashes 4 times:** This appears only when something goes wrong, and data is not collected properly - Check if your camera is plugged in correctly

* **GPIO 23 LED flashes on left click:** Switching to left->right axis for sensor box.

* **GPIO 23 LED flashes twice on right click:** Switching to up->down axis for sensor box.

## Troubleshooting
Luxonis' [Depth-AI Troubleshooting page](https://docs.luxonis.com/en/latest/pages/troubleshooting/) is very useful for any issues or errors

While the Depth-AI camera does heat up a lot, this should not warrant any crashes or performance drops unless in extreme situations. This [page on operative temperature range](https://docs.luxonis.com/projects/hardware/en/latest/pages/articles/operative_temperature_range/) provides more specific information.

**Note:** A message such as the following:

    RuntimeError: Communication exception - possible device error/misconfiguration. Original message 'Couldn't read data from stream: 'preview' (X_LINK_ERROR)'

May be due to a faulty USB connection. Make sure that you are using a USB 3.0 Port and wire. Power supply may also be an issue, but would only be if there are other high-demand USB devices being used.

[//]: <img src="media/images/oak1lite.jpeg" alt="Oak-1 Lite" width="200"/>