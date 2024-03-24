from ultralytics import YOLO
import cv2
import mediapipe as mp
import numpy as np
from function import calculate_angle, check_element
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import animation
import serial

def motor_control(move_forward, turn_left, turn_right, release_all):
    if move_forward == 1:
        arduino_board.write(b'F')
    elif turn_left == 1:
        arduino_board.write(b'L')
    elif turn_right == 1:
        arduino_board.write(b'R')
    elif release_all == 1:
        arduino_board.write(b'E')

arduino_board = serial.Serial('COM12', 9600)
fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
times = []
angles = []
length_hip = []
length_shoulder = []
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
model = YOLO('yolov8n.pt')
detection_classes = [0]
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
resolution = [1280, 720]
detection_classes = []
with open("classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        detection_classes.append(class_name)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            results_ = model(frame)
            result = results_[0]
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            classes = np.array(result.boxes.cls.cpu(), dtype="int")
            person = 0
            detected_person = check_element(classes, person)
            if detected_person:
                for cls, bbox in zip(classes, bboxes):
                    class_name = detection_classes[cls].lower() if detection_classes else None
                    if class_name == 'person':
                        (x, y, x2, y2) = bbox
                        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
                        cv2.putText(frame, str(class_name), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            try:
                landmarks = results.pose_landmarks.landmark
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                # More landmark calculations...
                direction_person = ((right_shoulder[0] + left_shoulder[0]) / 2)
                # More direction calculations...
                move_forward = 0
                turn_left = 0
                turn_right = 0
                release_all = 0
                if detected_person:
                    if direction_person < 0.48:
                        turn_left = 1
                    elif direction_person > 0.52:
                        turn_right = 1
                    elif 0.48 < direction_person < 0.52:
                        move_forward = 1
                    else:
                        release_all = 1
                    motor_control(move_forward, turn_left, turn_right, release_all)
                move_forward = 0
                turn_left = 0
                turn_right = 0
                release_all = 0
            except:
                pass
            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    plt.show()

cap.release()
cv2.destroyAllWindows()
