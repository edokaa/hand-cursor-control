import cv2
import numpy as np
import HandDetector as hd
import Camera
import Mouse
import time
import autopy

camera = Camera(frame_r=100,w_cam=640,h_cam=480,smoothening = 10)
cap = camera.start_cam()

pTime = 0

detector = hd.HandDetector(maxHands=1)
# screen size

while True:
	# find hand landmarks
	_, img = cap.read()
	
	img = detector.find_hands(img)
	lm_list, bbox = detector.find_position(img)

	# get the tip of the index and middle fingers
	if len(lm_list) != 0:
		x1, y1 = lm_list[8 ][1:]
		x2, y2 = lm_list[12][1:]
		mouse = Mouse(x1, y1, camera)

		# check which fingers are up
		fingers = detector.fingers_up()
		# print(fingers)
		cv2.rectangle(img, (frame_r, frame_r), (w_cam - frame_r, h_cam - frame_r),
						(255, 0, 255), 2)
		# only index finger = moving mode
		if fingers[1] == 1 and fingers[2] == 0:
			mouse.move()
		# 8. both index and middle fingers are up = clicking mode
		if fingers[1] == 1 and fingers[2] == 1:
			length, img, line_info = detector.find_distance(8, 12, img)
			mouse.click(length, img, line_info)

	# frame rate
	cTime = time.time()
	fps = camera.get_frame_rate(cTime, pTime)
	pTime = cTime

	cv2.putText(
		img,
		str(int(fps)),
		(10, 70),
		cv2.FONT_HERSHEY_PLAIN,
		3,
		(255, 0, 255),
		3
	)

	# display
	cv2.imshow("Image", img)
	cv2.waitKey(1)