import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils     # Loop through points and draw lines

preTime = 0
currTime = 0

while True:
    success, img = cap.read()                       # Capture frame from video camera

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # Convert frame to RGB
    results = hands.process(imgRGB)                 # Process frame

    if results.multi_hand_landmarks:
        for handsLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handsLms.landmark):
                h, w, c = img.shape
                x, y, z = int(lm.x * w), int(lm.y * h), lm.z * -1

                print("ID {:.0f} X: {:.2f}, Y: {:.2f}, Size: {:.2f}".format(id, x, y, z))

                # Mark point (Thumb)
                if id==4:
                    cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)

            mpDraw.draw_landmarks(img, handsLms, mpHands.HAND_CONNECTIONS)

    # FPS Counter
    currTime = time.time()
    fps = 1/(currTime-preTime)
    preTime = currTime
    cv2.putText(img, "FPS: {:.2f}".format(int(fps)), (0, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)

