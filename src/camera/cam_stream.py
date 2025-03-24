#pip3 install flask
#pip3 install flask_cors

"""
camera.py : picks the correct cam driver (_pi, _opencv...) ddepends the setup
camera_opencv.py : Works well with generic webcams, uses opencv to get vid from usb webcam
camera_pi.py / camera_pi2.py : uses  picamera library (PiCamera()), specifically for raspnpi camera module
camera_v4l2.py : Video4Linux2 (V4L2) API for camera input

"""

from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration())
picam2.start()

def generate_frames():
    while True:
        # Capture a frame
        frame = picam2.capture_array()
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        jpg_frame = buffer.tobytes()
        # Build the MJPEG frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Return a multipart response for the stream
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the app on all network interfaces, port 8000
    app.run(host='0.0.0.0', port=8000)


# ip:port/video_feed