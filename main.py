# Imports
# For the Vision System
from ultralytics import YOLO
import cv2
import mediapipe as mp
import numpy as np
from function import calculate_angle, check_element
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import animation
# For Physical Robot system serial communication with Arduino
import serial


# Motor Control Function
def motor_control(move_forward, turn_left, turn_right, release_all):
    if move_forward == 1:
        arduino_board.write(b'F')  # Use bytes for serial communication
    elif turn_left == 1:
        arduino_board.write(b'L')
    elif turn_right == 1:
        arduino_board.write(b'R')
    elif release_all == 1:
        arduino_board.write(b'E')
    # else:
    #     # Add any codes if required
    #     pass



# Connecting to the serial communication
# Change the port when it is different
arduino_board = serial.Serial('COM12', 9600)

# Create figures for plotting
fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()

# Creating the arrays to plot
times = []
angles = []
length_hip = []
length_shoulder = []

# Giving drawing utilities to when visualizing through sources
mp_drawing = mp.solutions.drawing_utils

# Importing the pose estimation model
mp_pose = mp.solutions.pose

# Load YoloV8 model
model = YOLO('yolov8n.pt')
# Detection class with YOLO (Here "Person" which os '0')
detection_classes = [0]

# Initializing the sources
# For Camera Source
cap = cv2.VideoCapture(0)
# For a Video Source
# cap = cv2.VideoCapture("test climbing.mp4")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
resolution = [1280, 720]

# Capturing Classes

detection_classes = []
with open("classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        detection_classes.append(class_name)

# Setting up targets

# Operation

# Setting up mediapipe instance
# Confidence values improves the accuracy of detection or closer to 1 accurate it is
with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:  # variable pose represent this line

    # frames to process from sources

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:

            # Object detection # Human Detection using YOLO
            results_ = model(frame)
            # results_ = model.track(frame, persist=True)
            result = results_[0]

            # Identification of the bounding boxes around the detected objects
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            # Identification of the class ID of the detected objects

            classes = np.array(result.boxes.cls.cpu(), dtype="int")

            print(classes)

            person = 0
            detected_person = check_element(classes, person)

            # print(bboxes)

            # Drawing Bounding boxes
            # Create contour on the selected patient/ patients
            if detected_person:
                for cls, bbox in zip(classes, bboxes):
                    class_name = detection_classes[cls].lower() if detection_classes else None
                    if class_name == 'person':
                        (x, y, x2, y2) = bbox
                        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
                        cv2.putText(frame, str(class_name), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
            else:
                pass
            # Patient Detection using the trained dataset model

            # Create contour on the selected patient/ patients

            # Contour Dimension monitoring

            # MediaPipe with BlasePose
            # Detect stuff and render
            # Recolor image by re-ordering the color arrays
            # Recolor image to RGBqqq
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # MAKE DETECTION
            results = pose.process(image)  # By processing we save detections in results variable

            # Recolor image to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Estimating angles of the selected landmarks for patient condition

            # Extracting Landmarks
            # using try to make no disturb to the feed in case of no landmarks detected
            # this code of block will extract landmarks without destroying the loop
            try:
                landmarks = results.pose_landmarks.landmark

                # Getting Coordinates of the specific landmarks that are being used to create angles
                # Right side landmarks
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                right_foot_index = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]

                # Left side landmarks
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                left_foot_index = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]

                # Calculating Angles  made out  with the 3 landmark coordinates for each angle
                # For left hip
                angle_hip_left = round(calculate_angle(left_shoulder, left_hip, left_knee), 2)
                # For left ankle
                angle_ankle_left = round(calculate_angle(left_knee, left_ankle, left_foot_index), 2)
                # For left knee
                angle_knee_left = round(calculate_angle(left_hip, left_knee, left_ankle), 2)
                # For right hip
                angle_hip_right = round(calculate_angle(right_shoulder, right_hip, right_knee), 2)
                # For right ankle
                angle_ankle_right = round(calculate_angle(right_knee, right_ankle, right_foot_index), 2)
                # For right knee
                angle_knee_right = round(calculate_angle(right_hip, right_knee, right_foot_index), 2)

                # Creating midpoint of the line connecting left and right hips

                mid_hip = ((right_hip[0] + left_hip[0]) / 2, (right_hip[1] + left_hip[1]) / 2)
                hip_length = np.sqrt((right_hip[0] - left_hip[0]) ** 2 + (right_hip[1] - left_hip[0]) ** 2)

                # Creating midpoint of the line connecting left and right hips

                mid_shoulder = ((right_shoulder[0] + left_shoulder[0]) / 2, (right_shoulder[1] + left_shoulder[1]) / 2)
                shoulder_length = np.sqrt(
                    (right_shoulder[0] - left_shoulder[0]) ** 2 + (right_shoulder[1] - left_shoulder[0]) ** 2)
                # direction_person is used for shoulder determination
                direction_person = mid_shoulder[0]

                mid_knee = ((right_knee[0] + left_knee[0]) / 2, (right_knee[1] + left_knee[1]) / 2)
                knee_length = np.sqrt(
                    (right_knee[0] - left_knee[0]) ** 2 + (right_knee[1] - left_knee[0]) ** 2)
                # direction_person1 is used for knee determination
                direction_person1 = mid_knee[0]
                # print(direction_person)

                # print(mid_hip)
                # print(hip_length)
                # print(shoulder_length)

                # Visualization angle
                cv2.putText(image, str(angle_hip_left),
                            tuple(np.multiply(left_hip, resolution).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # print(angle_hip_left)

                cv2.putText(image, str(angle_ankle_left),
                            tuple(np.multiply(left_ankle, resolution).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # print(angle_ankle_left)

                cv2.putText(image, str(angle_knee_left),
                            tuple(np.multiply(left_knee, resolution).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # print(angle_knee_left)

                # mp_drawing.plot_landmarks(results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                # Append current time and angle_knee_left to the lists
                # Py-plotting
                # Update the plot
                # Plotting the angles and other parameters
                current_time = dt.datetime.now()
                times.append(current_time)
                angles.append(angle_hip_left)
                length_hip.append(hip_length)
                length_shoulder.append(shoulder_length)


                def update_plot1(frame):
                    ax.clear()
                    ax.plot(times[:frame], angles[:frame], label='Angle Hip Left')
                    ax.legend()


                animate1 = animation.FuncAnimation(fig, update_plot1, frames=len(times), interval=1000, repeat=False)


                def update_plot2(frame):
                    ax1.clear()
                    ax1.plot(times[:frame], length_shoulder[:frame], label='Shoulder Length')
                    ax1.legend()


                animate2 = animation.FuncAnimation(fig1, update_plot2, frames=len(times), interval=1000, repeat=False)

                # Conditions and limitations for the angles and to provide the condition of the patient
                # Print the condition on the screen
                if angle_knee_right and angle_knee_right < 175 and angle_ankle_right and angle_ankle_right < 170:
                    print("failure")
                    cv2.putText(image, str("Failure !!!"), (x - 300, y + 300), cv2.FONT_HERSHEY_PLAIN, 2, (0, 102, 225),
                                2)

                    # Bring the robot control section in the latter part to here
                    # It will only be implemented if there is only a failure

                else:
                    print("all good")
                    cv2.putText(image, str("All Good"), (x - 300, y + 300), cv2.FONT_HERSHEY_PLAIN, 2, (102, 513, 51),
                                2)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 666), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )  # 1st drawing code-line for joint color, 2nd for connections(bones)

                # If contour dimension and patient condition from landmarks suspicious

                # Estimate the realtime distance from camera to the patient
                # distance_patient =

                # Estimate the direction of the detected person
                # Move the below code lines to the failure code above as an if Failure condition
                # Connect to the robot_control

                # Initialize flags
                move_forward = 0
                turn_left = 0
                turn_right = 0
                release_all = 0

                # Pixel Calibration formula for the direction determination conditions

                if detected_person:
                    if direction_person < 0.48:
                        turn_left = 1
                        print("Turn Left")
                        cv2.putText(image, str("Robot Turning Left"), (x + 100, y + 300), cv2.FONT_HERSHEY_PLAIN, 1,
                                    (0, 102, 225), 2)

                    elif direction_person > 0.52:
                        turn_right = 1
                        print("Turn Right")
                        cv2.putText(image, str("Robot Turning Right"), (x + 100, y + 300), cv2.FONT_HERSHEY_PLAIN, 1,
                                    (0, 102, 225), 2)

                    elif 0.48 < direction_person < 0.52:

                        move_forward = 1
                        print("Move Forward")
                        cv2.putText(image, str("Robot Moving Forward"), (x + 100, y + 300), cv2.FONT_HERSHEY_PLAIN, 1,
                                    (0, 102, 225), 2)

                    else:
                        release_all = 1
                        print("Stopping")
                        cv2.putText(image, str("Robot Moving Forward"), (x + 100, y + 300), cv2.FONT_HERSHEY_PLAIN, 1,
                                    (0, 102, 225), 2)

                    # Call the motor_control function
                    motor_control(move_forward, turn_left, turn_right, release_all)

                # Reset the flags
                move_forward = 0
                turn_left = 0
                turn_right = 0
                release_all = 0
            except:
                pass
        # Processed Feed Visualization
        cv2.imshow('Mediapipe Feed', image)

        # The existing command (checking whether we hit the exit key
        # 0xFF - what is the key where the key is letter 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

            # Output visualization and relevant data required

    # Matplotlib Visualization for Graphical Data Plots
    plt.show()

cap.release()
cv2.destroyAllWindows()
