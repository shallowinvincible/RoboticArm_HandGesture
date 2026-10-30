# 🤖 3D Robotic Arm Hand Gesture Controller

A real-time, interactive **6-DOF Robotic Arm 3D Simulation** controlled directly via **OpenCV & Computer Vision Hand Gestures** (detecting finger counts 1, 2, 3, 4, 5, and closed fist 0).

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

### Step 2: Install Dependencies
Install all required libraries using `requirements.txt`:

* **On macOS / Linux:**
  ```bash
  pip3 install -r requirements.txt
  ```
  *(or `pip install -r requirements.txt`)*

* **On Windows:**
  ```bash
  pip install -r requirements.txt
  ```

> 💡 **Tip:** If you prefer using a virtual environment:
> ```bash
> # Create virtual environment
> python3 -m venv .venv
> 
> # Activate it:
> source .venv/bin/activate        # macOS / Linux
> .venv\Scripts\activate           # Windows
> 
> # Install:
> pip install -r requirements.txt
> ```

---

### Step 3: Run the Project

You can run either of the following commands:

* **On macOS / Linux:**
  ```bash
  python3 server.py
  ```
  *(or `python3 main.py`)*

* **On Windows:**
  ```bash
  python server.py
  ```
  *(or `python main.py`)*

Your default web browser will automatically open at `http://localhost:8000/index.html` featuring:
1. **Interactive 3D Articulated Robotic Arm** with realistic materials and shadows.
2. **Live Webcam Hand Tracking** with real-time skeletal detection and finger counting.
3. **Joint Angle Gauges & Kinematics Telemetry** showing real-time joint positions in degrees.

*(When the browser prompts you for camera access, click **"Allow"**).*

---

## 🎯 Gesture Controls Cheat Sheet

Position your hand in front of your webcam. The vision pipeline counts extended fingers and translates them into kinematic commands:

| Finger Count | Pose Name | Robotic Arm Action |
| :---: | :--- | :--- |
| **0 (Fist)** | **Home / Standby** | Returns all 6 joints to standard neutral position. |
| **1 Finger** | **Forward Reach (Pick)** | Actuates Base Turntable & Shoulder forward toward target. |
| **2 Fingers** | **Upward Lift (Carry)** | Elevates the boom to transport payload safely. |
| **3 Fingers** | **Side Drop (Place)** | Sweeps Base Turntable 90° and rotates wrist to drop zone. |
| **4 Fingers** | **High Inspection** | Extends forearm and tilts gripper upward for inspection. |
| **5 Fingers** | **Open Gripper / Wave** | Opens parallel gripper jaws wide and executes demo wave. |

> 💡 **Mode Switch:** Click the **"JOINT SELECT"** button at the top-left if you want each number (1, 2, 3, 4) to actuate individual joint motors (J1 Base, J2 Shoulder, J3 Elbow, J4 Wrist) one-by-one!

---

## 🛡️ Presentation Safety Net (Emergency Failsafe)

During live presentations, room lighting or projector interference can occasionally affect webcams. **You have built-in safeguards so the presentation NEVER fails:**

1. **Direct Keyboard Override:** Press keys **`0`, `1`, `2`, `3`, `4`, `5`** on your keyboard to instantly trigger the exact same robotic kinematics without needing the webcam!
2. **Key `M`**: Toggles between **Preset Pose Mode** and **Individual Joint Mode**.
3. **Key `R`**: Instantly resets the arm to Home position.
4. **Interactive 3D Camera:** Left-click + drag to rotate the 3D view, right-click to pan, scroll to zoom.

---

## 🐍 Standalone Python OpenCV Window (Optional)

If your professor or evaluator specifically asks: *"Can you show the raw OpenCV Python script?"*

Run the dedicated Python CV script:
```bash
# macOS / Linux
python3 python_vision.py

# Windows
python python_vision.py
```
This opens a native OpenCV window displaying:
- Live 21-point hand landmark tracking.
- Bounding box and real-time FPS counter.
- Joint control signal dispatches in the terminal.

---

## 📐 Common Viva / Presentation Questions

### Q: Why not use raw CAD files directly?
> **Answer:** *"CAD files (STEP / SLDASM) only contain static 3D geometry without kinematic joint hierarchies, rotation axes ($x, y, z$), or limit constraints. To make a robot move programmatically, the model must be articulated with parent-child joint transforms (like URDF or kinematic scene trees). Our simulation utilizes a 6-DOF kinematic tree with smooth interpolation (lerping) between target and current joint angles."*

### Q: How does the hand gesture detection work?
> **Answer:** *"The vision pipeline extracts 21 three-dimensional hand landmarks in real time. For the four fingers (Index, Middle, Ring, Pinky), it computes whether the tip landmark $Y$-coordinate is elevated above the PIP (Proximal Interphalangeal) joint. For the thumb, it verifies horizontal clearance against the MCP joint. The stabilized finger count is then mapped to joint coordinate trajectories."*

---

## 📁 Project Structure

```
├── index.html          # High-performance 3D Robotic Arm (Three.js) & Vision HUD (MediaPipe)
├── server.py           # Local HTTP server (launches browser automatically)
├── main.py             # Convenient entry point alias
├── python_vision.py    # Dedicated OpenCV Python implementation
├── requirements.txt    # Pip dependency list (OpenCV, MediaPipe, NumPy)
├── .gitignore          # Git exclusion rules
└── README.md           # Documentation and step-by-step execution guide
```
