#!/usr/bin/env python3
"""
AM-ARM200 (7-DOF) Robotic Arm Hand Gesture Controller Server
-----------------------------------------------------------
Zero-dependency Python server that launches the AM-ARM200 3D URDF
simulation and dual-hand gesture vision interface in your browser.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        sys.stderr.write(f"[Server] {args[0]} - {args[1]}\n")

def run():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 65)
        print("🤖 AM-ARM200 (7-DOF) ROBOTIC ARM GESTURE CONTROLLER")
        print("=" * 65)
        print(f"[*] Serving locally at: {url}")
        print("[*] Opening your web browser automatically...")
        print("[*] Press Ctrl+C to stop the server.")
        print("=" * 65)
        print("\n💡 GESTURE CONTROLS CHEAT SHEET:")
        print("  --- 1 HAND GESTURES ---")
        print("  • Fist (0)     : Standby / Home neutral pose")
        print("  • 1 Finger     : J1 Shoulder Pan (Base Yaw)")
        print("  • 2 Fingers    : J2 Shoulder Lift (Boom Pitch)")
        print("  • 3 Fingers    : J3 Elbow Flex (Forearm)")
        print("  • 4 Fingers    : J4 Wrist Flex (Pitch)")
        print("  • 5 Fingers    : J5 Wrist Yaw (Swivel)")
        print("  --- 2 HANDS GESTURES ---")
        print("  • 6 (5 + 1)    : J6 Wrist Roll (Tool Flange Rotation)")
        print("  • 7 (5 + 2)    : J7 Gripper Jaw (Moving Jaw Clamp/Open)")
        print("  • Keys 0-7 on keyboard also trigger joints/poses directly!\n")
        
        try:
            webbrowser.open(url)
        except Exception:
            print(f"[!] Please open {url} manually in your browser.")
            
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[+] Server stopped successfully.")

if __name__ == "__main__":
    run()
