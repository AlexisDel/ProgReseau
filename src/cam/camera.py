import io
import time
import cv2
import numpy as np
from picamera2 import Picamera2
from base_camera import BaseCamera

class Camera(BaseCamera):
    @staticmethod
    def frames():
        picam = Picamera2()
        picam.configure(picam.create_still_configuration())
        picam.start()
        time.sleep(2)

        qr_detector = cv2.QRCodeDetector()

        try:
            while True:
                frame = picam.capture_array()

                # Detect QR code
                data, bbox, _ = qr_detector.detectAndDecode(frame)
                if data:
                    print(f"📷 QR Code detected: {data}")

                # Encode frame to JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    continue

                yield jpeg.tobytes()
        finally:
            picam.stop()
