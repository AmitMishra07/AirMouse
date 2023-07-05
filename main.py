import cv2
import mediapipe as mp
import numpy as np
import pyautogui

#commit test
#test 2

pyautogui.FAILSAFE=False
screen_w, screen_h = pyautogui.size()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
index_y=0
index_x=0
ring_y=0

smoothening = 4
ploc_x,ploc_y=0,0
cloc_x,cloc_y=0,0

wCam,hCam = 640,480

cam = cv2.VideoCapture(0)
cam.set(3,wCam)
cam.set(4,hCam)
frameR = 150

while cam.isOpened():
    ret, img = cam.read()
    img = cv2.flip(img,1)
    img_rgb = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    retangle = cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,0),2)
    if result.multi_hand_landmarks:
        for hand_marks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img,hand_marks)
            for id,lms in (enumerate(hand_marks.landmark)):
                h,w,c = img.shape
                cx,cy = int(lms.x*w), int(lms.y*h)
                print(cx,cy)
                if id == 8:
                    index_x = np.interp(cx,(frameR,wCam-frameR),(0,screen_w))
                    index_y = np.interp(cy,(frameR,hCam-frameR),(0,screen_h))

                    cloc_x = ploc_x+(index_x-ploc_x)/smoothening
                    cloc_y = ploc_y + (index_y - ploc_y) / smoothening
                    pyautogui.moveTo(cloc_x,cloc_y)
                    ploc_x,ploc_y = cloc_x,cloc_y

                if id == 16:
                    ring_y = (screen_h / h * cy)

                if id == 12:
                    thumb_x = np.interp(cx, (frameR, wCam - frameR), (0, screen_w))
                    thumb_y = np.interp(cy, (frameR, hCam - frameR), (0, screen_h))

                    if index_y-thumb_y<60 and index_y-thumb_y>1:
                            print(index_y-thumb_y)
                            print("click")
                            pyautogui.click()
                            pyautogui.sleep(1)


    cv2.imshow("image", img)

    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
