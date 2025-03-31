import io
import time
import cv2
import numpy as np
import picamera
import picamera.array
from src.cam.base_camera import BaseCamera



class Camera(BaseCamera):

    def __init__(self):
        self.scanning_enabled = False
        self.scanned_result = None
        super().__init__()

    def frames(self):
        #global scanning_enabled, scanned_result
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

                if self.scanning_enabled:
                    data, _, _ = qr_detector.detectAndDecode(image)
                    if data:
                        print("QR Code scanned:", data)
                        self.scanned_result = data  
                        self.scanning_enabled = False

                ret, jpeg = cv2.imencode('.jpg', image)
                stream.seek(0)
                stream.truncate()
                if ret:
                    yield jpeg.tobytes()

    def scan_qr_code(self, timeout=10):
        #global scanning_enabled, scanned_result
        self.scanning_enabled = True
        while self.scanning_enabled:
            if self.scanned_result:
                self.scanning_enabled   = False
                return self.scanned_result

        return None
