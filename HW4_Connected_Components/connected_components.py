import cv2
import numpy as np
from google.colab.patches import cv2_imshow
from skimage.filters import threshold_local
from skimage import measure
import queue

img = cv2.imread('car.jpg', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
num_labels, origin_img = cv2.connectedComponents(img)

def imshow_components(labels):
    # Map component labels to hue val
    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # 將圖片由RGB轉為HSV格式，然後取HSV中的Ｖ值，此效果與灰階效果類似
    V = cv2.split(cv2.cvtColor(labeled_img, cv2.COLOR_BGR2HSV))[2]

    labeled_img = threshold_local(V, 47, offset=15).astype("uint8") * 255
    labeled_img = cv2.bitwise_not(labeled_img)
    
    # set background label to black
    labeled_img[label_hue==0] = 0

    # cv2.imshow('labeled_img.jpg', labeled_img)
    cv2_imshow(labeled_img)
    cv2.waitKey()
    cv2.imwrite('labeled_img.jpg', labeled_img)

    # 黑轉白，白轉黑
    for i, row in enumerate(labeled_img):
      # print('pix:', pix.shape)
      for j, val in enumerate(row):
        if val == 0:
          labeled_img[i][j] = 255
        else:
          labeled_img[i][j] = 0
   
    cv2_imshow(labeled_img)
    cv2.imwrite('labeled_img2.jpg', labeled_img)


    # connected components analysis
    # background=0表示pixel值為0則認定為背景
    labels = measure.label(labeled_img, background=0)

    # 建立一個空的圖，存放稍後將篩選出的字母及數字
    mask = np.zeros(labeled_img.shape, dtype="uint8")

    # 依序處理每個labels(components)
    for (i, label) in enumerate(np.unique(labels)):
      # label=0，表示為背景
      if label == 0:
        continue

      # 否則為前景
      # 建立該前景的Binary圖
      labelMask = np.zeros(labeled_img.shape, dtype="uint8")
      labelMask[labels == label] = 255

      # 有幾個非0的像素
      numPixels = cv2.countNonZero(labelMask)

      # 如果像素數目在1500～7000之間認定為車牌的字母或數字
      if numPixels > 1500 and numPixels < 7000:
        # 放到剛剛建立的空圖中
        mask = cv2.add(mask, labelMask)


    # 顯示所抓取到的車牌
    # cv2.imshow("mask.jpg", mask)
    cv2_imshow(mask)
    cv2.waitKey(0)
    cv2.imwrite('output.jpg', mask)

    # 計算connected components的pixel數目
    pixel_cnt(mask)


  
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
def bfs(x, y, img, vis):
  sz = img.shape
  cnt = 1
  que = []
  vis[x][y] = 1
  que.append((x, y))
  while que:
    at = que.pop(0)
    x, y = at[0], at[1]
    # 上下左右移動
    for i in range(4):
      nx = x + dx[i]
      ny = y + dy[i]
      # 在component邊界內，且是白色
      if 0 <= nx < sz[0] and 0 <= ny < sz[1] and vis[nx][ny] == 0 and img[nx][ny] == 255:
        vis[nx][ny] = 1
        cnt += 1
        que.append((nx, ny))
  return cnt 
    
def pixel_cnt(img):
  vis = np.zeros(img.shape, dtype=int)
  components = []
  for i, row in enumerate(img):
    for j, val in enumerate(row):
      if val == 255 and vis[i][j] == 0: 
        cnt = bfs(i, j, img, vis)
        # 雜訊去除
        if cnt > 50:
          components.append(cnt)
  # components.sort()
  print('components:', components)

imshow_components(origin_img)