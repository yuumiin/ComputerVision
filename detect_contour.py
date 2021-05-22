import cv2
import sys
import shutil
import os, glob
from natsort import natsorted, ns

camera = 1

def onChange(pos):
    pass

cv2.namedWindow("Threshold Trackbar")

cv2.createTrackbar("threshold_min", "Threshold Trackbar", 0, 255, onChange)
cv2.createTrackbar("threshold_max", "Threshold Trackbar", 0, 255, lambda x : x)

cv2.setTrackbarPos("threshold_min", "Threshold Trackbar", 231)
cv2.setTrackbarPos("threshold_max", "Threshold Trackbar", 255)

def make_folder(path, new_path, new_folder, extention):
    dir = path + '/'
    glob_file = glob.glob('*.'+extention) 

    for i in glob_file :
        if i == "classes.txt":
            glob_file.remove(i)
    
    new_dir = new_path + '/' + new_folder 

    try:
        if not os.path.exists(new_dir) :
            os.makedirs(new_dir)
    except OSError:
        print('Error')

    for i, path_lst in enumerate(glob_file):
        print('path_lst: ' + path_lst)
        if os.path.isfile(new_dir+'\\' + path_lst):
            print("파일이 이미 존재함: " + new_dir + '/' + path_lst)
        else:
            shutil.move(dir+path_lst, new_dir)

def first_video(image):
    img = cv2.cvtColor(image,cv2.IMREAD_COLOR)
    height = img.shape[0]
    width = img.shape[1]
    cv2.rectangle(img,(150,150),(450,350),(255,0,0),1)
    cv2.imshow('window',img)

def threshold_setting():

    global minval, maxval

    capture = cv2.VideoCapture(camera)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cv2.waitKey(33) < 0:
        ret, frame = capture.read()
        minval = cv2.getTrackbarPos("threshold_min", "Threshold Trackbar")
        maxval = cv2.getTrackbarPos("threshold_max", "Threshold Trackbar")
        first_video(frame)
        contour(frame, minval, maxval)
        # cv2.imshow("Threshold Trackbar", frame)
    # print(minval, maxval)

    capture.release()
    cv2.destroyAllWindows()

def convert(size, x, y, x2, y2):
    dw = 1./size[0] 
    dh = 1./size[1] 
    w = x2 - x
    h = y2 - y

    x = (x + x2)/2.0 
    y = (y + y2)/2.0 

    x = round(x*dw ,6)
    w = round(w*dw ,6)
    y = round(y*dh ,6)
    h = round(h*dh ,6)

    return (x,y,w,h)

def contour(image, minval, maxval):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    roi = img[150:350, 150:450]
    # dst = roi.copy()
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    ret, binary = cv2.threshold(gray, minval, maxval, cv2.THRESH_BINARY)
    #binary = cv2.bitwise_not(binary)
    # cv2.imshow('binary', binary)
    
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print(contours)    

    for i in contours:
        cv2.drawContours(roi, [i], 0, (0, 0, 255), 2)
        peri =cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i ,0.02*peri, True)
        global x, y, w,h
        x , y , w, h = cv2.boundingRect(approx)
        # print("x :" ,x, 'y :', y, 'w :',w,'h:', h)
        
        cv2.rectangle(roi, (x,y),(x+w,y+h),(0,255,0),1)
        height = img.shape[0]
        width = img.shape[1]

        # x,y 좌표 잘라준만큼 150 필셀 더해줘서 반영함
        x= x+150
        y= y+150
        x2 = x+w
        y2 = y+h

        Yolo_test=convert((width, height), x, y, x2, y2)

    #좌표
    left = tuple(i[i[:,:,0].argmin()][0]) #i[:,:,0] x좌표만 있는 배열
    right = tuple(i[i[:,:,0].argmax()][0])
    top = tuple(i[i[:,:,1].argmin()][0]) #i[:,:,1] y좌표만 있는 배열
    bottom = tuple(i[i[:,:,1].argmax()][0])

    # 좌표 표시
    cv2.circle(roi,left,5,(0,0,255),-1)
    cv2.circle(roi,right,5,(255,0,0),-1) #파
    cv2.circle(roi,top,5,(0,0,255),-1) #빨
    cv2.circle(roi,bottom,5,(0,255,0),-1) #초

    # cv2.imshow("Threshold Trackbar", img)
    cv2.imshow("Threshold Trackbar", roi)
    return Yolo_test

def save_txt(x, y, w, h, classes, name):
    with open('classes.txt', 'r') as file:
        label = file.readlines()[classes][0]
    
    with open(str(name) + '_reja.txt','w') as file:
        file.write(str(label) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h))

def dir_save(load_path, name, write_path):
    with open(name+'.txt','w') as file:
        file_list = natsorted(os.listdir(load_path))
        for i in range(len(file_list)):
            # file.write(path + '/' + file_list[i] + '\n')
            file.write(write_path + file_list[i] + '\n')

threshold_setting()

cap = cv2.VideoCapture(camera)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Camera open failed!")
    sys.exit()
 
count = 0

while(True):
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    first_video(frame)
    print('minval:', str(minval), 'maxval:', str(maxval))
    yolo_value = contour(frame, minval, maxval)
    if ret : 
        if count < 100 :
            save_txt(yolo_value[0], yolo_value[1], yolo_value[2], yolo_value[3], 1, count)
            # print('Saved frame number : ' + str(int(cap.get(1)))) 
            cv2.imwrite(str(count) + '_reja.jpg', frame)
            print(yolo_value[0], yolo_value[1], yolo_value[2], yolo_value[3])
        count += 1

    if cv2.waitKey(1) == 27:
        make_folder('/Users/leeyumin/Desktop/vision', '/Users/leeyumin/Desktop', 'image2', 'jpg')
        make_folder('/Users/leeyumin/Desktop/vision', '/Users/leeyumin/Desktop', 'label2', 'txt')
        # dir_save('/Users/leeyumin/Desktop/image', 'train_dir', '/content/drive/My Drive/Torch/data/plate/images/')
        break
cap.release()
cv2.destroyAllWindows()



dir_save('/Users/leeyumin/Desktop/image', 'train_dir', '/content/drive/My Drive/Torch/data/plate/images/')
