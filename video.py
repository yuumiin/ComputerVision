import cv2
import sys
import shutil
import os, glob
 

def make_folder(path, new_path, new_folder):
    dir = path + '/'
    glob_file = glob.glob('*.jpg') 

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

# 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Camera open failed!")
    sys.exit()
 
count = 0
 
while(True):
    # read()는 grab()와 retrieve() 두 함수를 한 함수로 불러옴
    # 두 함수를 동시에 불러오는 이유는 프레임이 존재하지 않을 때
    # grab() 함수를 이용하여 return false 혹은 NULL 값을 넘겨 주기 때문
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)

    # if ret : 
    #     if count < 100 :
    #         print('Saved frame number : ' + str(int(cap.get(1)))) 
    #         cv2.imwrite(str(count) + '.jpg', frame)
    #         print('Saved frame%d.jpg' % count) 
    #     count += 1
    edge = cv2.Canny(frame, 100, 150) # 윤곽선

    if cv2.waitKey(1) == 27:
        # make_folder('/Users/leeyumin/Desktop/opencv', '/Users/leeyumin/Desktop', 'img')
        break

    cv2.imshow('frame', frame)
    cv2.imshow("Trackbar Windows", edge)

cap.release()
cv2.destroyAllWindows()
 

