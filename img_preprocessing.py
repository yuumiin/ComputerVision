# 이미지를 학습하기 위해서슨 각 이미지를 숫자 배열로 저장해야됨
# 하나의 폴더 안에 카테고리 별로 폴더를 만들고 그 카테고리에 맞는 이미지 넣기
import os, cv2, numpy as np
from sklearn.model_selection import train_test_split

groups_folder_path = '/Users/leeyumin/Desktop/images/'
categories = ["silicon", "reja"] # 폴더명
num_classes = len(categories)

img_w = 28
img_h = 28

x = []
y = []

for idx, categorie in enumerate(categories):
    label = [0 for i in range(num_classes)]
    label[idx] = 1
    img_dir = groups_folder_path + categorie +'/'
    print("img_dir:", img_dir)
    for top, dir, f in os.walk(img_dir):
        for filename in f:
            print(img_dir + filename)
            img = cv2.imread(img_dir + filename)
            img = cv2.resize(img, None, fx = img_w/img.shape[0], fy = img_h/img.shape[1])
            x.append(img/256)
            # print(x)
            y.append(label)

x = np.array(x)
y = np.array(y)
# print(x)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
xy = (x_train, x_test, y_train, y_test)



