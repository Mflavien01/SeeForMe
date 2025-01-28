
# Raspberry Pi Vision and Haptic Feedback System

![Project Logo](logo/logo_name.png)

This project is designed to run on a Raspberry Pi and utilizes cameras and sensors to detect specific objects in real-time. It offers visual, auditory, and haptic feedback based on the detected objects' characteristics and positions.

## Features

- Real-time image processing with OpenCV.
- Auditory feedback using pygame for different detections.
- Haptic feedback through a custom-built vibration controller.
- Utilization of PiCamera2 for seamless integration with Raspberry Pi Camera.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Raspberry Pi (Model 3B or newer recommended).
- Raspberry Pi Camera Module installed and enabled.
- Appropriate sensors and haptic devices connected to the GPIO pins.

## Installation

1. **Set Up Your Raspberry Pi**: 
   Ensure that your Raspberry Pi is set up with the latest version of Raspberry Pi OS and that the camera interface is enabled through the `raspi-config` utility.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mflavien01/SeeForMe.git
   cd SeeForMe
   ```
3. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   sudo pip3 install opencv-python-headless pygame picamera2
   ```

   Note: The `opencv-python-headless` package is used to avoid unnecessary dependencies on GUI packages.

## Usage

To run the project, navigate to the project directory and execute the following command:
```bash
python raspi/main.py
```

This script will start processing frames from the camera and provide auditory and haptic feedback based on object detection results. Make sure all devices and sensors are correctly connected before starting the script.

## Configuration

- **`LOWER_SCREEN_RATIO`**: Adjust this value to change the detection zone to the lower part of the screen. Lower values increase the detection area.
- **`DISTANCE_THRESHOLD`**: Set this threshold to define what is considered a "close" obstacle. Decrease this value to increase sensitivity to nearby objects.

## Troubleshooting

- **Camera Not Detected**: Ensure the camera is properly connected and enabled in the `raspi-config`.
- **Dependencies Not Installing**: Make sure you are using the latest version of pip. Upgrade pip using `sudo pip3 install --upgrade pip` and try installing the dependencies again.
- **No Output from Script**: Verify that your sensors and haptic devices are wired correctly to the GPIO pins specified in the script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Contact

![Project Logo with Name](logo/logo_name.png)

[Flavien MATHIEU](https://www.linkedin.com/in/flavien-mathieu/)  
Project Link: [https://github.com/Mflavien01/SeeForMe](https://github.com/Mflavien01/SeeForMe)
