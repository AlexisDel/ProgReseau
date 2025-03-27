import io
import time
import cv2
import numpy as np
from picamera2 import Picamera2
from base_camera import BaseCamera

scanning_enabled = False
scanned_result = None
class Camera(BaseCamera):
    @staticmethod
    def frames():
        global scanning_enabled, scanned_result
        picam = Picamera2()
        picam.configure(picam.create_still_configuration())
        picam.start()
        time.sleep(2)

        qr_detector = cv2.QRCodeDetector()

        try:
            while True:
                frame = picam.capture_array()

                if scanning_enabled:
                    data, _, _ = qr_detector.detectAndDecode(frame)
                    if data:
                        print("QR Code scanned:", data)
                        scanned_result = data
                        scanning_enabled = False  # stop scanning

                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    continue

                yield jpeg.tobytes()
        finally:
            picam.stop()
    """ @staticmethod
    def frames():
        global last_frame
        picam = Picamera2()
        picam.configure(picam.create_still_configuration())
        picam.start()
        time.sleep(2)

        qr_detector = cv2.QRCodeDetector()

        try:
            while True:
                frame = picam.capture_array()
                last_frame = frame.copy()
                data, bbox, _ = qr_detector.detectAndDecode(frame)
                if data:
                    print(f"QR Code detected: {data}")

                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    continue

                yield jpeg.tobytes()
        finally:
            picam.stop()
     """
    @staticmethod
    def scan_qr_code(timeout=10):
        qr_detector = cv2.QRCodeDetector()
        picam = Picamera2()
        picam.configure(picam.create_still_configuration())
        picam.start()
        try:
            while True:
                frame = picam.capture_array()
                data, _, _ = qr_detector.detectAndDecode(frame)
                if data:
                    print("QR Code detected:", data)
                    return data
        finally:
            picam.stop()
        return None


