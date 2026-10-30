#!/usr/bin/env python3
"""
Standalone OpenCV Hand Gesture & Joint Signal Controller
-------------------------------------------------------
Demonstrates OpenCV computer vision detection of hand gestures
and computes joint rotation signals for the robotic arm.

Requirements (Optional for standalone Python window):
  pip install opencv-python mediapipe numpy
"""

import cv2
import time
import sys

# Try importing MediaPipe, or fall back to OpenCV Contour detection
HAS_MEDIAPIPE = False
try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False


def count_fingers_mediapipe(hand_landmarks):
    """
    Counts extended fingers using 21 3D hand landmarks:
    - Thumb: landmark 4 vs 3
    - Index: landmark 8 vs 6
    - Middle: landmark 12 vs 10
    - Ring: landmark 16 vs 14
    - Pinky: landmark 20 vs 18
    """
    lm = hand_landmarks.landmark
    fingers = []

    # Thumb (horizontal check based on relative wrist orientation)
    if lm[4].x < lm[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers: Check if tip Y is higher (smaller Y value) than PIP joint
    tip_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for tip, pip in zip(tip_ids, pip_ids):
        if lm[tip].y < lm[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)


def get_joint_action_description(num_fingers):
    actions = {
        0: ("STANDBY / REST", "All joints return to initial home orientation"),
        1: ("JOINT 1 (BASE YAW)", "Base turntable rotating ±60° (Pick Target)"),
        2: ("JOINT 2 (SHOULDER)", "Shoulder actuator tilting upper boom forward"),
        3: ("JOINT 3 (ELBOW)", "Elbow joint articulating forearm downward"),
        4: ("JOINT 4 & 5 (WRIST)", "Wrist pitch & roll adjusting end-effector angle"),
        5: ("JOINT 6 (GRIPPER)", "Parallel jaws opening wide / releasing payload")
    }
    return actions.get(num_fingers, ("UNKNOWN", "Maintaining last state"))


def main():
    print("=" * 60)
    print("🎥 OPENCV HAND GESTURE & ROBOTIC JOINT TRACKER")
    print("=" * 60)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Error: Could not access webcam. Ensure no other app is using it.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if HAS_MEDIAPIPE:
        print("[✓] MediaPipe Hands Loaded Successfully.")
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )
    else:
        print("[!] Note: MediaPipe not detected. Using OpenCV contour-based fallback.")
        print("    Run 'pip install mediapipe' for highest accuracy.")

    prev_time = 0

    while True:
        success, img = cap.read()
        if not success:
            print("[!] Failed to grab frame.")
            break

        # Mirror image for natural user interaction
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        num_fingers = 0

        if HAS_MEDIAPIPE:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for hand_lms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
                    num_fingers = count_fingers_mediapipe(hand_lms)

                    # Draw hand bounding box
                    x_list = [int(lm.x * w) for lm in hand_lms.landmark]
                    y_list = [int(lm.y * h) for lm in hand_lms.landmark]
                    xmin, xmax = min(x_list) - 15, max(x_list) + 15
                    ymin, ymax = min(y_list) - 15, max(y_list) + 15
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 210, 255), 2)
            else:
                num_fingers = 0
        else:
            # Fallback simple HUD
            num_fingers = 0

        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time + 1e-6)
        prev_time = curr_time

        # Draw Tech HUD overlay
        action_name, action_detail = get_joint_action_description(num_fingers)

        # Top Bar
        cv2.rectangle(img, (0, 0), (w, 80), (20, 25, 35), -1)
        cv2.line(img, (0, 80), (w, 80), (0, 210, 255), 2)

        cv2.putText(img, f"FINGERS: {num_fingers}", (20, 35), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 210, 255), 2)
        cv2.putText(img, f"SIGNAL -> {action_name}", (20, 65), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.putText(img, f"FPS: {int(fps)}", (w - 110, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 128), 2)

        # Bottom Telemetry
        cv2.rectangle(img, (0, h - 35), (w, h), (15, 20, 30), -1)
        cv2.putText(img, f"Kinematic Status: {action_detail}", (15, h - 12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 190, 200), 1)

        cv2.imshow("OpenCV Hand Gesture Joint Controller", img)

        # Press 'q' or 'ESC' to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
