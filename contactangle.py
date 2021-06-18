import cv2
import numpy as np
import math

def first_video(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    height = img.shape[0]
    width = img.shape[1]
    cv2.rectangle(img,(0,150),(640,350),(255,0,0),1)
    cv2.imshow('img',img)

def droplet_contour(image) :
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    roi = image[150:430, 300:1200] #y,x
    
    #cv2.waitKey(0)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i in contours:
        cv2.drawContours(roi, [i], 0, (0, 0, 255), 2)
        # cv2.imshow("src", roi)

    # cv2.waitKey(0)

    # print('last_contour', i) #마지막 윤곽선값 가져오기

    #좌표
    left = tuple(i[i[:,:,0].argmin()][0]) #i[:,:,0] x좌표만 있는 배열
    right = tuple(i[i[:,:,0].argmax()][0])
    top = tuple(i[i[:,:,1].argmin()][0]) #i[:,:,1] y좌표만 있는 배열
    bottom = tuple(i[i[:,:,1].argmax()][0])
    # print('right: ', right)
    # print('top: ', top)
    # print('bottom; ', bottom)


    # 좌표 표시
    # cv2.circle(roi,left,10,(0,0,255),-1)
    cv2.circle(roi,right,5,(255,0,0),-1) #파
    cv2.circle(roi,top,5,(0,0,255),-1) #빨
    cv2.circle(roi,bottom,5,(0,255,0),-1) #초

    cv2.line(roi, bottom, top, (255,255,0), 3)
    cv2.line(roi, bottom, (top[0], bottom[1]), (255, 255, 0), 3)


    #각도
    dx = top[0] - bottom[0]
    dy = bottom[1] - top[1]

    rad = math.atan2(dy, dx)

    degree = math.degrees(rad)
    angle = round(degree,4)
    
    contact_angle = 2 * degree
   
    print('각도: ', degree)
    print('contact angle: ', contact_angle)
    
    cv2.putText(roi, str(angle), (bottom[0], bottom[1]-10), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(roi, 'contact angle: ' + str(round(contact_angle,2)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,0), 1, cv2.LINE_AA)
    cv2.imshow("res", roi)


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('1.avi')
writer = None
count=0
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        # close the video file pointers
        cap.release()
        # close the writer point
        break

    # 100프레임마다 함수실행
    # if count % 100 == 0:
    #     droplet_contour(frame) 
    # count = count+1

    
    droplet_contour(frame) #모든프레임마다 함수실행

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()