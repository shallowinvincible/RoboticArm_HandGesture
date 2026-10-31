# 🤖 AM-ARM200 (7-DOF) Robotic Arm Hand Gesture Controller

A real-time, interactive **7-DOF AM-ARM200 Robotic Arm Simulation** powered by its official **URDF & 3D STL meshes** (from [liyiteng/AM-ARM](https://github.com/liyiteng/AM-ARM.git)), controlled directly via **Computer Vision Dual-Hand Gestures** (supporting 1-hand gestures `0-5` and 2-hand gestures `6-7`).

Designed for **instant portability, zero ROS/ROS2 headaches**, and foolproof presentations.

---

## 🚀 How to Clone and Run (Step-by-Step)

Follow these exact steps to pull and launch this project on any computer (Mac, Windows, or Linux).

### Step 1: Clone the Repository
Open your Terminal (macOS/Linux) or Command Prompt / PowerShell (Windows) and run:
```bash
git clone <YOUR_REPO_URL>
cd "Tushar IPD"
```

---

### Step 2: Install Dependencies (Optional for Python Script)
The web simulation runs locally with **zero external pip dependencies**, but if you want to run the standalone OpenCV Python script:

* **On macOS / Linux:**
  ```bash
  pip3 install -r requirements.txt
  ```

* **On Windows:**
  ```bash
  pip install -r requirements.txt
  ```

---

### Step 3: Launch the Project

Run either of the following commands:

* **On macOS / Linux:**
  ```bash
  python3 main.py
  ```
  *(or `python3 server.py`)*

* **On Windows:**
  ```bash
  python main.py
  ```
  *(or `python server.py`)*

Your browser will automatically open at `http://localhost:8000/index.html` displaying:
1. **Official AM-ARM200 3D URDF Kinematic Model** rendered with realistic PBR materials, shadows, and grid floor.
2. **Live Dual-Hand Webcam Tracking** with skeletal visualization and real-time finger summation.
3. **7-Axis Joint Angle Telemetry** showing real-time angles in degrees.

*(When the browser prompts you for camera access, click **"Allow"**).*

---

## 🎯 Dual-Hand Gesture Mapping (7 Joints)

The vision pipeline tracks up to **2 hands simultaneously** using MediaPipe. It sums the extended fingers across both hands to command all 7 joints of the AM-ARM200:

| Gestures | Hands Used | Joint / Action | URDF Joint & Motion |
| :---: | :---: | :--- | :--- |
| **0 (Fist)** | 1 Hand | **Home / Standby** | Returns all 7 joints to neutral zero position. |
| **1 Finger** | 1 Hand | **J1: Shoulder Pan** | `left_shoulder_pan` — Base turntable yaw sweep. |
| **2 Fingers** | 1 Hand | **J2: Shoulder Lift** | `left_shoulder_lift` — Boom pitch elevation. |
| **3 Fingers** | 1 Hand | **J3: Elbow Flex** | `left_elbow_flex` — Forearm articulation. |
| **4 Fingers** | 1 Hand | **J4: Wrist Flex** | `left_wrist_flex` — Wrist pitch adjustment. |
| **5 Fingers** | 1 Hand | **J5: Wrist Yaw** | `left_wrist_yaw_joint` — Lateral wrist swivel. |
| **6 (5 + 1)** | **2 Hands** | **J6: Wrist Roll** | `left_wrist_roll` — Tool flange roll rotation. |
| **7 (5 + 2)** | **2 Hands** | **J7: Gripper Jaw** | `left_gripper` — Moving jaw clamping and release. |

> 💡 **Mode Switch:** Click the **"JOINT SELECT"** button at the top-left to toggle between coordinated multi-axis Preset Poses and moving individual joints (J1 to J7) one-by-one!

---

## 🛡️ Presentation Safety Net (Emergency Failsafe)

During live presentations, room lighting or camera permissions can occasionally be unpredictable. **You have built-in safeguards so the presentation NEVER fails:**

1. **Direct Keyboard Override:** Press keys **`0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`** on your keyboard to instantly trigger each joint and pose without needing the webcam!
2. **Key `M`**: Toggles between **Preset Pose Mode** and **Individual Joint Mode**.
3. **Key `R`**: Instantly resets the arm to Home position.
4. **Interactive 3D Camera:** Left-click + drag to rotate the 3D view, right-click to pan, scroll to zoom.

---

## 🐍 Standalone Python OpenCV Window (Optional)

If your professor or evaluator specifically asks: *"Can you show the raw OpenCV Python code?"*

Run the dedicated dual-hand OpenCV script:
```bash
# macOS / Linux
python3 python_vision.py

# Windows
python python_vision.py
```
This opens a native OpenCV window displaying:
- Real-time tracking of up to 2 hands simultaneously.
- Individual and combined finger counts (`Hand 1: 5 | Hand 2: 2 -> Total: 7`).
- Active AM-ARM200 joint dispatch telemetry and FPS counter.

---

## 📁 Project Structure

```
├── am-arm200/
│   ├── urdf/
│   │   └── am-arm200.urdf       # Official AM-ARM200 URDF kinematic description
│   └── am-arm200-meshes/        # 9 official STL meshes (Base, Arms, Wrist, Gripper)
├── libs/                        # Local offline Three.js, URDFLoader & STLLoader
│   ├── three.min.js
│   ├── OrbitControls.js
│   ├── STLLoader.js
│   └── URDFLoader.js
├── index.html                   # 3D AM-ARM200 URDF Viewer & Dual-Hand Vision HUD
├── server.py                    # Local HTTP server (launches browser automatically)
├── main.py                      # 1-click entry point
├── python_vision.py             # Dedicated dual-hand OpenCV Python implementation
├── requirements.txt             # Pip dependency list (OpenCV, MediaPipe, NumPy)
├── .gitignore                   # Git exclusion rules
└── README.md                    # Documentation and step-by-step presentation guide
```
