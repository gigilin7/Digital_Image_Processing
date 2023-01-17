from PIL import Image
import numpy as np

# 算8個參數{a,b,c,d,e,f,g,h}
def get_eight():
    # 舊座標 (原始影像)
    old_x = [304,1145,50,1447]
    old_y = [336,313,854,807]
    # 新座標 (影像校正後)
    x = [0,1478,0,1478]
    y = [0,0,1108,1108]

    A = np.array([[x[0], y[0], x[0]*y[0], 1],
                [x[1], y[1], x[1]*y[1], 1],
                [x[2], y[2], x[2]*y[2], 1],
                [x[3], y[3], x[3]*y[3], 1]])

    b1 = np.array([old_x[0],old_x[1],old_x[2],old_x[3]]) # x
    b2 = np.array([old_y[0],old_y[1],old_y[2],old_y[3]]) # y

    # Solve AX=b 
    X1 = np.linalg.solve(A, b1)
    X2 = np.linalg.solve(A, b2)

    # 水平(按列順序)把array堆疊起來
    eight = np.hstack((X1,X2))

    return eight # eight[a,b,c,d,e,f,g,h]
    

def transform(output,eight):

    # get width and height of new image
    width, height = output.size

    for i in range(width):
        for j in range(height):
            
            # 用8個參數取得座標
            x1 = (eight[0]*i) + (eight[1]*j) + (eight[2]*i*j) + eight[3]
            y1 = (eight[4]*i) + (eight[5]*j) + (eight[6]*i*j) + eight[7]

            # 取整數
            x = int(x1)
            y = int(y1)

            # distance
            a = x1 - x
            b = y1 - y

            # Bilinear Interpolation (用於影像放大)
            # f(x,y) = (1-a)(1-b)g(x,y) + a(1-b)g(x,y+1) + b(1-a)g(x+1,y) + ab(x+1,y+1)
            temp = [0,0,0]
            for c in range(3):
                temp[c] = int((1-a) * (1-b) * pixel1[x, y][c] + a * (1-b) * pixel1[x+1, y][c] + (1-a) * b * pixel1[x, y+1][c] + a * b * pixel1[x+1, y+1][c])
            pixel2[i, j] = (temp[0],temp[1],temp[2])

# Loadding Image
image = Image.open('before_img.jpg')

# Calculate Perspective Value{a,b,c,d,e,f,g,h}
eight = get_eight()

# Create a Image Space for Perspective Transfrom (width、height)
# 設定輸出圖片大小
output = Image.new(image.mode, (1478, 1108))

# Allocates storage for the image and loads the pixel data
pixel1 = image.load() # old
pixel2 = output.load() # new

#  Perspective Transfrom Processing
transform(output,eight)

# Save the Perspective Image
output.save("after_img.jpg")