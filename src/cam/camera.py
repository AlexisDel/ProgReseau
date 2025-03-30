import io
import time
import cv2
import numpy as np
import picamera
import picamera.array
from base_camera import BaseCamera

scanning_enabled = False
scanned_result = None

class Camera(BaseCamera):
    @staticmethod
    def frames():
        global scanning_enabled, scanned_result
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            time.sleep(2)  # Allow camera to warm up

            stream = io.BytesIO()
            qr_detector = cv2.QRCodeDetector()

            for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
                stream.seek(0)
                data = np.frombuffer(stream.read(), dtype=np.uint8)
                image = cv2.imdecode(data, 1)

                if scanning_enabled:
                    data, _, _ = qr_detector.detectAndDecode(image)
                    if data:
                        print("QR Code scanned:", data)
                        scanned_result = data
                        scanning_enabled = False

                ret, jpeg = cv2.imencode('.jpg', image)
                stream.seek(0)
                stream.truncate()
                if ret:
                    yield jpeg.tobytes()

    @staticmethod
    def scan_qr_code(timeout=10):
        qr_detector = cv2.QRCodeDetector()
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            time.sleep(2)
            with picamera.array.PiRGBArray(camera) as output:
                start = time.time()
                for frame in camera.capture_continuous(output, format='bgr', use_video_port=True):
                    image = output.array
                    data, _, _ = qr_detector.detectAndDecode(image)
                    if data:
                        print("QR Code detected:", data)
                        return data
                    output.truncate(0)
                    if time.time() - start > timeout:
                        break
        return None
