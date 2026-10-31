#!/usr/bin/env python3
"""
OpenCV Dual-Hand Gesture Controller for AM-ARM200 (7-DOF Robotic Arm)
-------------------------------------------------------------------
Tracks up to 2 hands in real time, computes extended finger counts (0-7),
and maps them to the 7 active joints of the AM-ARM200 robotic arm.

Supported Gestures:
  • 1 Hand (0-5): J1 Shoulder Pan, J2 Shoulder Lift, J3 Elbow Flex (Reversed), J4 Wrist Flex, J5 Wrist Yaw
  • 2 Hands (6-7): J6 Wrist Roll (5+1), J7 Gripper Jaw (5+2)
"""

import cv2
import time
import sys
from collections import deque, Counter

HAS_MEDIAPIPE = False
try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False


def count_fingers_for_hand(hand_landmarks):
    """
    High-precision finger counting using landmark geometry:
    - Thumb: relative horizontal clearance against Index MCP (5) and Pinky MCP (17)
    - 4 Fingers: Tip Y coordinate distinctly above PIP and PIP above MCP
    """
    lm = hand_landmarks.landmark
    count = 0

    # Index MCP (5) vs Pinky MCP (17) determines if thumb side is left or right in 2D space
    is_thumb_side_left = lm[5].x < lm[17].x
    thumb_tip = lm[4]
    thumb_ip = lm[3]
    thumb_mcp = lm[2]

    # Thumb is counted ONLY if projected outward past IP and MCP with safety margin
    if is_thumb_side_left:
        if thumb_tip.x < (thumb_ip.x - 0.025) and thumb_tip.x < thumb_mcp.x:
            count += 1
    else:
        if thumb_tip.x > (thumb_ip.x + 0.025) and thumb_tip.x > thumb_mcp.x:
            count += 1

    # 4 Fingers: Check if tip Y is distinctly above PIP and PIP is above MCP
    fingers = [
        (8, 6, 5),    # Index
        (12, 10, 9),  # Middle
        (16, 14, 13), # Ring
        (20, 18, 17)  # Pinky
    ]

    for tip, pip, mcp in fingers:
        if lm[tip].y < (lm[pip].y - 0.02) and lm[pip].y < (lm[mcp].y + 0.04):
            count += 1

    return count


def get_joint_action_description(num_fingers):
    """
    Maps finger counts 0-7 to AM-ARM200 7-DOF joints
    """
    actions = {
        0: ("HOME / STANDBY", "All 7 joints neutral / Rest position"),
        1: ("J1: SHOULDER PAN", "Base turntable rotating ±90° (left_shoulder_pan)"),
        2: ("J2: SHOULDER LIFT", "Upper arm boom articulating (left_shoulder_lift)"),
        3: ("J3: ELBOW FLEX (REVERSED)", "Forearm flexing forward in reversed natural direction"),
        4: ("J4: WRIST FLEX", "Wrist pitch articulating (left_wrist_flex)"),
        5: ("J5: WRIST YAW", "Wrist lateral swivel ±60° (left_wrist_yaw_joint)"),
        6: ("J6: WRIST ROLL [2 HANDS 5+1]", "Wrist tool roll continuous rotation (left_wrist_roll)"),
        7: ("J7: GRIPPER JAW [2 HANDS 5+2]", "Moving jaw clamp & payload release (left_gripper)")
    }
    return actions.get(num_fingers, ("HOLD STATE", "Maintaining current joint angles"))


def main():
    print("=" * 65)
    print("🤖 AM-ARM200 (7-DOF) STABILIZED DUAL-HAND GESTURE TRACKER")
    print("=" * 65)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Error: Could not access webcam. Ensure no other application is using it.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if HAS_MEDIAPIPE:
        print("[✓] MediaPipe Hands Loaded (Dual-Hand Precision Tracking enabled).")
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.65
        )
    else:
        print("[!] Note: MediaPipe not detected. Run 'pip install mediapipe' to enable vision.")

    prev_time = 0
    gesture_history = deque(maxlen=7)
    current_stable_gesture = 0

    while True:
        success, img = cap.read()
        if not success:
            print("[!] Failed to grab camera frame.")
            break

        # Mirror image for natural user interaction
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        num_hands_detected = 0
        h_counts = []

        if HAS_MEDIAPIPE:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                num_hands_detected = len(results.multi_hand_landmarks)
                colors = [(0, 210, 255), (0, 145, 255)] # Cyan for hand 1, Orange for hand 2

                for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                    color = colors[idx % len(colors)]
                    mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
                    fingers = count_fingers_for_hand(hand_lms)
                    h_counts.append(fingers)

                    # Bounding Box
                    x_list = [int(lm.x * w) for lm in hand_lms.landmark]
                    y_list = [int(lm.y * h) for lm in hand_lms.landmark]
                    xmin, xmax = min(x_list) - 15, max(x_list) + 15
                    ymin, ymax = min(y_list) - 15, max(y_list) + 15
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)
                    cv2.putText(img, f"Hand {idx+1}: {fingers}", (xmin, ymin - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

                raw_total = sum(h_counts)
                raw_total = min(7, raw_total)
                gesture_history.append(raw_total)
            else:
                gesture_history.append(0)
        else:
            gesture_history.append(0)

        # Temporal Majority Filter to eliminate vibration and flicker
        if len(gesture_history) > 0:
            most_common, count = Counter(gesture_history).most_common(1)[0]
            if count >= 4:
                current_stable_gesture = most_common

        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time + 1e-6)
        prev_time = curr_time

        action_name, action_detail = get_joint_action_description(current_stable_gesture)

        # Tech HUD Overlay
        cv2.rectangle(img, (0, 0), (w, 85), (15, 20, 30), -1)
        cv2.line(img, (0, 85), (w, 85), (0, 210, 255), 2)

        if num_hands_detected == 2:
            hand_str = f"2 HANDS ({h_counts[0]}+{h_counts[1]}={current_stable_gesture})"
        elif num_hands_detected == 1:
            hand_str = f"1 HAND ({current_stable_gesture} FINGERS)"
        else:
            hand_str = "NO HAND DETECTED (STANDBY)"

        cv2.putText(img, f"SIGNAL -> {action_name}", (15, 32), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 210, 255), 2)
        cv2.putText(img, f"TRACKING: {hand_str}", (15, 65), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        cv2.putText(img, f"FPS: {int(fps)}", (w - 110, 32), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 128), 2)

        # Bottom Bar
        cv2.rectangle(img, (0, h - 35), (w, h), (10, 14, 22), -1)
        cv2.putText(img, f"Kinematics: {action_detail}", (15, h - 12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 190, 200), 1)

        cv2.imshow("AM-ARM200 (7-DOF) OpenCV Controller", img)

        # Press 'q' or 'ESC' to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
