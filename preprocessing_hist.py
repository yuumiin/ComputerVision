import cv2, numpy as np
import sys
import shutil
import os, glob
from natsort import natsorted, ns
from matplotlib import pyplot as plt

camera = 0

def make_folder(path, new_path, new_folder, extention, overwrite):
    dir = path + '/'
    glob_file = glob.glob('*.'+extention) 

    for i in glob_file :
        if i == "classes.txt":
            glob_file.remove(i)
    
    new_dir = new_path + '/' + new_folder + '/'

    try:
        if not os.path.exists(new_dir) :
            os.makedirs(new_dir)
    except OSError:
        print('Error')

    for i, filename in enumerate(glob_file):
        print('filename: ' + filename)
        try :
            shutil.move(dir+filename, new_dir)
        except shutil.Error:
            if overwrite == True:
                print("파일 덮어 씌우기")
                print(new_dir+filename)
                shutil.move(dir+filename, new_dir+filename)
            else: 
                print("파일이 이미 존재함: " + new_dir + filename)

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

def first_video(image):
    img = cv2.cvtColor(image,cv2.IMREAD_COLOR)
    height = img.shape[0]
    width = img.shape[1]
    cv2.rectangle(img,(150,150),(28,28),(255,0,0),1)
    cv2.setMouseCallback('window', onMouse)
    dst = img[150:270, 150:270]
    cv2.imshow('window',img)

def threshold_setting():
    capture = cv2.VideoCapture(camera)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cv2.waitKey(33) < 0:
        ret, frame = capture.read()
        first_video(frame)

    capture.release()
    cv2.destroyAllWindows()

def hist(img, filename) :
    img = cv2.imread('./'+str(img)+'.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_equalize = cv2.equalizeHist(gray)

    hist = cv2.calcHist([gray], [0], None, [256], [0,256]) #image, channel, mask, size, range
    hist_equlize = cv2.calcHist([img_equalize], [0], None, [256], [0,256])

    #hist데이터를 csv파일로 저장
    # hist_list= np.array(hist)
    # np.savetxt(str(filename) + '.csv', hist_list, delimiter=',', fmt='%s')
    plt.hist(gray.ravel(), 256, [0,256]) #grayscale의 픽셀범위: 0~255
    plt.yscale('log')
    # plt.plot(hist, color = 'r') #선으로그리는거
    # plt.title(filename)
    plt.axis('off')
    plt.savefig(str(filename)+'.png',bbox_inches='tight',pad_inches = 0)
    # plt.ylim(0,65000) #y축 scale맞춰줌 #yscale쓸거면 필요없음

def data(count, target):
    cap = cv2.VideoCapture(camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Camera open failed!")
        sys.exit()

    cv2.waitKey(1000)
    while(True):
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        # first_video(frame)
        cv2.imshow('camera', frame)
        if ret : 
            if count < target:
                # dst = frame[150:270, 150:270]
                cv2.imwrite(str(count) + '.jpg', frame)
            if count == target :
                print("finish!")
            count += 1

        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

# count = 20
# target = 30
# # 20까지!

# threshold_setting()
# data(count, target)

# for i in range(0,30):
#     print(i)
#     hist(i, i)
#     plt.clf()

# make_folder('/Users/leeyumin/Documents/GitHub/ComputerVision', '/Users/leeyumin/Desktop/train0604_ori', 'silicon9', 'jpg', True)
# make_folder('/Users/leeyumin/Documents/GitHub/ComputerVision', '/Users/leeyumin/Desktop/train0604', 'silicon9', 'png', True)