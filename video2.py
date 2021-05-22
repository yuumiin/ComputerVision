import cv2

def onChange(pos):
    pass

cv2.namedWindow("Trackbar Windows")

cv2.createTrackbar("threshold", "Trackbar Windows", 0, 255, onChange)
cv2.createTrackbar("maxValue", "Trackbar Windows", 0, 255, lambda x : x)

cv2.setTrackbarPos("threshold", "Trackbar Windows", 127)
cv2.setTrackbarPos("maxValue", "Trackbar Windows", 255)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open failed!")
    sys.exit()
 
count = 0

while(True):
    ret, frame = cap.read()

    thresh = cv2.getTrackbarPos("threshold", "Trackbar Windows")
    maxval = cv2.getTrackbarPos("maxValue", "Trackbar Windows")

    edge = cv2.Canny(frame, thresh, maxval) # 윤곽선

    if cv2.waitKey(1) == 27:
        break

    cv2.imshow('frame', frame)
    cv2.imshow("Trackbar Windows", edge)

cap.release()
cv2.destroyAllWindows()