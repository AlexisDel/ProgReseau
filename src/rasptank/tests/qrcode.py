import time

###########################
#   CODE QR CODE          #
###########################

import cv2


detect = cv2.QRCodeDetector()

while True:
	cam = cv2.VideoCapture(0)
	ret, frame = cam.read()
	value, points, straight_qrcode = detect.detectAndDecode(frame)
	print("QR CODE :", value)
	cam.release()
	time.sleep(1)
