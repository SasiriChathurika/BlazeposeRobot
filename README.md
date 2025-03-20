# 🤖BlazePoseRobot with YOLOv8: Vision-Guided Mobile Assistance🚶‍♀️

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)]

## 🎥 Video Demonstration

<!-- Replace this with your video embedding code -->
[![BlazePoseRobot Demo](https://drive.google.com/file/d/17HDwnNH4M6Vy3RRwG8kHtKke7scPXhaH/view?usp=sharing)

## 📃 Table of Contents

*   [🌟 Overview](#-overview)
*   [🎯 Key Features](#-key-features)
*   [🛠️ Hardware Requirements](#️-hardware-requirements)
*   [⚙️ Software Requirements](#️-software-requirements)
*   [📦 Installation](#-installation)
*   [🚀 Execution Guide: Step-by-Step](#-execution-guide-step-by-step)
*   [🧪 Code Structure](#-code-structure)
*   [🚦 Robot Control Logic](#-robot-control-logic)
*   [📈 Data Visualization](#-data-visualization)
*   [⚠️ Limitations](#️-limitations)
*   [🤝 Contributing](#-contributing)
*   [📄 License](#-license)
*   [🙏 Acknowledgments](#-acknowledgments)
*   [📧 Contact](#-contact)

## 🌟 Overview

This project implements a vision-guided mobile robot designed to track and assist a selected person.  It uses a combination of Computer Vision techniques, including:

*   **YOLOv8:** For robust human detection and bounding box generation.
*   **MediaPipe BlazePose:**  For real-time pose estimation and landmark extraction, enabling fall risk assessment.

The system runs on a laptop and communicates with an Arduino board via a serial connection. The robot, equipped with four motors, maneuvers towards the tracked individual based on commands sent from the laptop to the Arduino.  This project provides a foundation for building assistive robots, security systems, or other applications requiring person-following capabilities.

**This robot and vision system was designed and built by Sasiri Chathurika.**

## 🎯 Key Features

*   **Real-time Human Detection:** Employs YOLOv8 for accurate and fast detection of people in the camera feed.
*   **Pose Estimation with BlazePose:**  Extracts key body landmarks using MediaPipe BlazePose for posture analysis.
*   **Fall Risk Detection:** Calculates joint angles and potentially integrates vibration data (as mentioned in your description, though not currently present in the code) to identify potential fall risks.  *Note: Vibration analysis needs to be implemented based on your hardware setup.*
*   **Robot Motion Control:**  Sends commands to an Arduino board to control four motors, enabling precise movement towards the tracked person.
*   **Serial Communication:** Establishes a reliable serial connection between the laptop and the Arduino.
*   **Data Visualization:** Utilizes Matplotlib to generate real-time plots of joint angles, distance and person direction providing insights into the tracked person's movements and posture.

## 🛠️ Hardware Requirements

*   **Laptop/Computer:**  For running the Python code and processing the camera feed.
*   **Webcam/Camera:** To capture the video feed for human detection and pose estimation.
*   **Arduino Board:**  To receive commands from the laptop and control the motors.  *(e.g., Arduino Uno, Nano)*
*   **Quad-Wheel Robot Platform:** A mobile robot base with four motors (or a differential drive system).
*   **Motor Driver:**  To interface the Arduino with the motors (e.g., L298N).
*   **Jumper Wires:** For connecting the components.
*   **(Optional) Vibration Sensor:** If implementing vibration analysis for fall detection.

## ⚙️ Software Requirements

*   **Python 3.x:**  The core programming language.
*   **Libraries:**
    *   `ultralytics`: For YOLOv8 object detection.
    *   `cv2` (OpenCV): For image processing and camera input.
    *   `mediapipe`: For BlazePose pose estimation.
    *   `numpy`: For numerical computations.
    *   `pyserial`: For serial communication with the Arduino.
    *   `matplotlib`: For plotting graphs.
    *   `datetime`: For timestamps.

## 📦 Installation

1.  **Clone the repository:**

    ```bash
    git clone [YOUR_REPOSITORY_URL]
    cd [YOUR_REPOSITORY_DIRECTORY]
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```
    *Note: I will provide requirements.txt below*

3.  **Download YOLOv8 Model:**
    Download the YOLOv8 model (e.g., `yolov8n.pt`) from the [Ultralytics YOLOv8 repository](https://github.com/ultralytics/ultralytics) and place it in the project directory. *Or modify the `model = YOLO('yolov8n.pt')` line in `main.py` to point to the correct path.*

4.  **Arduino Setup:**
    *   Upload the `new_working_controller.ino` sketch to your Arduino board using the Arduino IDE.
    *   **Important:**  Modify the `COM12` port in `main.py` to match the actual serial port your Arduino is connected to (e.g., `COM3` on Windows, `/dev/ttyACM0` on Linux). You can usually find this information in the Arduino IDE under "Tools > Port."

## 🚀 Execution Guide: Step-by-Step

Follow these steps carefully to execute the `BlazePoseRobot` project:

1.  **Hardware Connection:**
    *   Assemble your quad-wheel robot platform.
    *   Connect the motors to the motor driver. Be sure to connect them according to the pin configuration you've defined in `new_working_controller.ino`.
    *   Connect the motor driver to the Arduino board. Refer to your motor driver's documentation for the correct wiring.
    *   Connect the Arduino board to your computer using a USB cable.

2.  **Software Setup:**
    *   Ensure that all the software requirements are installed correctly as outlined in the [Installation](#installation) section.
    *   Verify that the YOLOv8 model (`yolov8n.pt` or the model you've chosen) is in the correct directory, or that the path to it is correctly specified in `main.py`.
    *   Double-check that the serial port in `main.py` (`COM12` or your alternative) matches the port your Arduino is actually connected to.

3.  **Open a Terminal or Command Prompt:**
    *   Navigate to the project directory where `main.py` is located using the `cd` command:

        ```bash
        cd [YOUR_REPOSITORY_DIRECTORY]
        ```

4.  **Run the Python Script:**
    *   Execute the main script by typing:

        ```bash
        python main.py
        ```

    *   The script will now start:
        *   Initializing the camera.
        *   Loading the YOLOv8 model.
        *   Establishing the serial connection with the Arduino.

5.  **Observe the Output:**
    *   A window titled "Mediapipe Feed" will appear, showing the processed video feed from your camera.
    *   You should see bounding boxes around detected people, along with BlazePose landmarks overlaid on their bodies.
    *   Joint angles will be displayed near the corresponding joints.
    *   The script will print messages to the terminal indicating whether a "Failure" (potential fall risk) is detected or if everything is "All Good". It will also indicate which action the robot is taking.
    *   Matplotlib windows will open, showing the real-time plots of the selected angles.

6.  **Robot Calibration and Observation:**
    *   Place a person in front of the camera.
    *   Observe the robot's behavior. It should attempt to follow the person.
    *   **Crucial Calibration Step:** The most important part is calibrating the `direction_person` thresholds (0.48 and 0.52) in `main.py`. You will likely need to adjust these values based on your robot's dimensions, camera position, and how accurately it follows the person.
        *   If the robot consistently turns too early or too late, adjust the thresholds accordingly. Small adjustments (e.g., 0.01 or 0.02) can make a big difference.
        *   Iterate and test until the robot smoothly follows the person.
    *   If fall risk detection is implemented, test scenarios to see if that works.

7.  **Troubleshooting:**
    *   **No Video Feed:** Double-check that your camera is connected properly and that OpenCV can access it. You might need to specify the correct camera index (e.g., `cv2.VideoCapture(1)` if you have multiple cameras).
    *   **Serial Communication Errors:** Verify that the Arduino is connected to the correct serial port and that the baud rate (9600 in this case) matches in both the Python script and the Arduino sketch.
    *   **YOLOv8 Errors:** Ensure that the YOLOv8 model is downloaded and in the correct directory.
    *   **Robot Not Moving:** Check the wiring between the Arduino, motor driver, and motors. Also, verify that the pin numbers in the Arduino sketch match the physical connections.

8.  **Stopping the Script:**
    *   To stop the script, press the 'q' key in the "Mediapipe Feed" window.
    *   The Matplotlib windows will also close.
    *   The serial connection with the Arduino will be terminated.

## 🧪 Code Structure

*   **`main.py`:** The main script that handles camera input, object detection, pose estimation, robot control, and visualization.
*   **`function.py`:** Contains helper functions for:
    *   `calculate_angle()`: Calculates the angle between three points (landmarks).
    *   `check_element()`: Checks if an element exists in an array.
    *   `estimate_distance()`: Estimates the distance from the camera to the tracked person.
*   **`new_working_controller.ino`:** The Arduino sketch that receives commands from the laptop and controls the motors.
*   **`classes.txt`:** (Optional) Contains the class names for the YOLOv8 object detection model.
*   **`requirements.txt`:** Lists the Python packages required for the project.

## 🚦 Robot Control Logic

The `main.py` script uses the `direction_person` variable (based on the midpoint of the shoulders) to determine the robot's movement:

*   `direction_person < 0.48`: Turn the robot left.
*   `direction_person > 0.52`: Turn the robot right.
*   `0.48 < direction_person < 0.52`: Move the robot forward.
*   Otherwise, stop the robot.

These thresholds need to be calibrated based on your robot's dimensions, camera placement, and desired responsiveness.

## 📈 Data Visualization

The script generates Matplotlib plots to visualize the following data:

*   **Angle Hip Left vs. Time:**  Shows the change in the left hip angle over time.
*   **Shoulder Length vs. Time:** Shows the change in the shoulder length over time.

These plots can be helpful for:

*   Monitoring the tracked person's posture.
*   Identifying trends in their movements.
*   Tuning the fall risk detection algorithm.

## ⚠️ Limitations

*   **Lighting Conditions:** The performance of YOLOv8 and BlazePose can be affected by poor lighting.
*   **Occlusion:**  If the tracked person is partially occluded, the pose estimation may be inaccurate.
*   **Calibration:**  Accurate calibration of the camera and robot's movement is crucial for proper tracking.
*   **Processing Power:** Real-time processing of the video feed and pose estimation requires sufficient computing power.  Performance may be limited on older or less powerful laptops.
*   **Fall Detection Reliability:** Angle-based fall detection can be unreliable in certain situations. Incorporating data from additional sensors (e.g., accelerometer, gyroscope) could improve accuracy.
*   **Serial Port Dependency:** Code needs to be updated according to the serial port the Arduino is on.

## 🤝 Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to improve the code, please submit an issue or pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

*   [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8.
*   [Google MediaPipe](https://developers.google.com/mediapipe) for BlazePose.
*   The open-source community for providing valuable resources and support.

## 📧 Contact

[Your Name] - [Your Email]
