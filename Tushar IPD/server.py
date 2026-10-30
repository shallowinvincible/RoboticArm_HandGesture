#!/usr/bin/env python3
"""
3D Robotic Arm Hand Gesture Controller Server
---------------------------------------------
Zero-dependency Python server that launches the 3D Robotic Arm
simulation and hand gesture vision interface in your browser.
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
        # Clean terminal output
        sys.stderr.write(f"[Server] {args[0]} - {args[1]}\n")

def run():
    os.chdir(DIRECTORY)
    # Allow port reuse so restarting works instantly
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print("🤖 3D ROBOTIC ARM GESTURE CONTROLLER")
        print("=" * 60)
        print(f"[*] Serving locally at: {url}")
        print("[*] Opening your web browser automatically...")
        print("[*] Press Ctrl+C to stop the server.")
        print("=" * 60)
        print("\n💡 PRESENTATION CHEAT SHEET:")
        print("  • Show 1 finger : Pick Pose / Base Joint")
        print("  • Show 2 fingers: Carry Pose / Shoulder Joint")
        print("  • Show 3 fingers: Place Pose / Elbow Joint")
        print("  • Show 4 fingers: High Inspection / Wrist")
        print("  • Show 5 fingers: Open Gripper / Wave")
        print("  • Closed fist (0): Home / Standby position")
        print("  • Keys 0-5 on keyboard also trigger poses directly!\n")
        
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
