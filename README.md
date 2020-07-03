# Smarta – A smart ball to teach turn-taking 🏀💬

Smarta is a project developed during the MSc. in Computer Science and Engineering (Human-Computer Interaction and Design) at Politecnico di Milano for the Advanced User Interfaces course by Stefano Formicola (@ste7en), Fabiana Ferrara (@fabif11), Elena Palombini (@elenapalombini) and Marta Mazzi (@MartaMazzi).

It is based on a Raspberry Pi, a MPU6050 accelerometer and gyroscope, a vibration motor and a WS2812 LED strip. Any model of Raspberry Pi can work for this project, however we suggest to use a model with a built-in Wi-Fi module to have the access point working correctly.

## Design and Technology documentation

The full documentation of the project is available [here](/docs/Design_and_Technology.pdf).

## Requirements

In order to have the web interface of the smart object accessible to control Smarta we suggest to install an easy to use access point setup and wifi management like [RaspAP](https://github.com/billz/raspap-webgui), while all the other requirements are listed in [requirements_dev.txt](/requirements_dev.txt) file and [setup.py](/setup.py).

## GPIO wiring connection

Coming soon.

## Testing

Some libraries, like RPi.GPIO and rpi_ws281x, are executable only on Raspberry Pi, which makes the testing of the application a bit frustrating when dealing with trials and errors.
A mock class of the application (Smarta) has been included and imported when a ImportError exception is raised.
