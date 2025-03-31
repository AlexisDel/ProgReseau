from flask import Flask, render_template, Response
import src.cam.camera as camera
from src.cam.camera import Camera
import threading
import time
import os
import signal
#sudo ../rasptank/bin/python3 -m src.cam.app

app = Flask(__name__)
stream_active = False
flask_thread = None
cam = Camera()
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    global stream_active
    stream_active = True
    try:
        while True:
            frame = camera.get_frame()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'
    finally:
        stream_active = False

@app.route('/video_feed')
def video_feed():
    global cam
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')


def run_stream():
    global flask_thread

    def start_flask():
        print("Flask server starting...")
        #os.environ['WERKZEUG_RUN_MAIN'] = 'true'  # Prevent double start
        app.run(host='0.0.0.0', port=5000, threaded=True)

    if not flask_thread or not flask_thread.is_alive():
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.start()
        time.sleep(1)

def stop_stream():
    print("Stopping Flask server...")
    os.kill(os.getpid(), signal.SIGINT)

def scan_code():
    global stream_active, cam

    if not stream_active:
        print("stream was off, turning on...")
        run_stream()
        time.sleep(1)

    print("QR code scan enabled")
    #Camera.scanned_result = None
    cam.scanning_enabled = True
    while cam.scanning_enabled:
        if cam.scanned_result:
            print("boo")
            #print("QR Code scanned:", cam.scanned_result)
            cam.scanning_enabled = False
            return cam.scanned_result
        time.sleep(0.2)

if __name__ == "__main__":
    scan_code()