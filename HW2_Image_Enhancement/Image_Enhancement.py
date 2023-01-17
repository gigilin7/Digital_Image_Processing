from PIL import Image, ImageDraw, ImageFilter

# 使用3*3的mask，取得mask周圍像素值
def getpixel(x, y, image, num=3):
    pixel = []
    for i in range(-(int(num/2)),int(num/2)+1):
        for j in range(-(int(num/2)), int(num/2)+1):
            p = image.getpixel((x+j, y+i))
            pixel.append(p)
    return pixel

# 原始圖像轉灰階
def Gray(image):
    width, height = image.size

    gray_img = Image.new("L", (width,height), (0))  
    gray_draw = ImageDraw.Draw(gray_img)

    for x in range(0, width):       
        for y in range(0, height):
            gray_scale = (image.getpixel((x,y))[0] + image.getpixel((x,y))[1] + image.getpixel((x,y))[2]) / 3
            gray_draw.point((x,y), fill=int(gray_scale))
    
    gray_img.save('Gray.jpg')
    return gray_img

# Laplacian得到二階微分結果
def Laplacian(x, y, image):
    pixel = getpixel(x, y, image)
    result = 8*pixel[4] - (pixel[0] + pixel[1] + pixel[2] + pixel[3] + pixel[5] + pixel[6] + pixel[7] + pixel[8])

    if result > 255: 
        result = 255 
    elif result < 0: 
        result = 0

    return int(result)

# Sobel得到一階微分結果(找Edge)
def Sobel(x,y,image):
    pixel = getpixel(x, y, image)
    result  = abs(-(pixel[0]) + pixel[2] - 2 * pixel[3] + 2 * pixel[5] - pixel[6] + pixel[8]) + \
            abs(-(pixel[0]) - 2 * pixel[1] - pixel[2] + pixel[6] + 2 * pixel[7] + pixel[8])
    
    if result > 255: 
        result = 255 
    elif result < 0: 
        result = 0
    return int(result)

# 模糊
def Blur(x,y,image):
    pixel = getpixel(x, y, image)
    result = (pixel[0] + pixel[1] + pixel[2] + pixel[3] + pixel[4] + pixel[5] + pixel[6] + pixel[7] + pixel[8]) / 9

    if result > 255: 
        result = 255 
    elif result < 0: 
        result = 0
    return int(result)

def main():

    origin_img = Image.open('Origin.jpg')

    # 原始圖像轉灰階
    gray_img = Gray(origin_img)
    width, height = gray_img.size

    # Laplacian
    laplacian_img = Image.new("L",(width,height),0)
    laplacian_draw = ImageDraw.Draw(laplacian_img)
    for x in range(1, width-1):       
        for y in range(1, height-1):
            pixel = Laplacian(x, y, gray_img)
            laplacian_draw.point((x,y), fill=pixel)
    laplacian_img.save('Laplacian.jpg')

    # Sobel
    sobel_img = Image.new("L", (width,height), (0))  
    sobel_draw = ImageDraw.Draw(sobel_img)
    for x in range(1, width-1):       
        for y in range(1, height-1):
            pixel = Sobel(x, y, gray_img)
            sobel_draw.point((x,y), fill=pixel)
    sobel_img.save('Sobel.jpg')

    # Blur
    blur_img = Image.new("L", (width,height), (0))  
    blur_draw = ImageDraw.Draw(blur_img)
    for x in range(1, width-1):       
        for y in range(1, height-1):
            pixel = Blur(x, y, sobel_img)
            blur_draw.point((x,y), fill=pixel)
    blur_img.save('Blur.jpg')

    # 正規化後乘上Laplacian，並加上灰階圖像
    normalization_img = Image.new("L", (width,height), (0))  
    normalization_draw = ImageDraw.Draw(normalization_img)
    for x in range(0, width):       
        for y in range(0, height):
            pixel = (blur_img.getpixel((x,y)) / 255) * laplacian_img.getpixel((x,y)) + gray_img.getpixel((x,y)) 
            if pixel > 255: 
                pixel = 255 
            elif pixel < 0: 
                pixel = 0
            normalization_draw.point((x,y), fill=int(pixel))
    normalization_img.save('Enhancement.jpg')

    print('Finish!')

if __name__ == '__main__':
    main()