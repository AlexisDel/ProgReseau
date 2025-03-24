#pip3 install flask
#pip3 install flask_cors

"""
camera.py : picks the correct cam driver (_pi, _opencv...) ddepends the setup
camera_opencv.py : Works well with generic webcams, uses opencv to get vid from usb webcam
camera_pi.py / camera_pi2.py : uses  picamera library (PiCamera()), specifically for raspnpi camera module
camera_v4l2.py : Video4Linux2 (V4L2) API for camera input

"""