from PIL import Image, ImageDraw, ImageFilter
import random

# 取得(3*3 5*5 7*7)周圍像素值
def getpixel(x,y,image,num):
    pixel = []
    width, height = image.size
    for i in range(-(int(num/2)),int(num/2)+1):
        # 超過圖片範圍則忽略
        if y+i < 0 or y+i >= height:
            continue
        for j in range(-(int(num/2)),int(num/2)+1):
            # 超過圖片範圍則忽略
            if x+j < 0 or x+j >= width :
                continue
            else:
                p = image.getpixel((x+j ,y+i))
                pixel.append(p)

    return(pixel)

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

# 將圖像加入雜訊
def Noise(image):
    width, height = image.size

    noise_img = Image.new("L", (width,height), (0))
    noise_draw = ImageDraw.Draw(noise_img)

    for x in range(0, width):
        for y in range(0, height):
            # random 0～1 的數字
            p = random.random()

            # 黑色
            if p <= 0.25:
                pixel_value = 0
            # 白色
            elif p <= 0.5:
                pixel_value = 255
            else:
                pixel_value = image.getpixel((x,y))

            noise_draw.point((x,y), fill=(int(pixel_value)))

    noise_img.save('Noise.jpg')
    return noise_img

# 處理雜訊圖像
def Median_Filter(image):
    width, height = image.size

    median_img = Image.new("L", (width,height), (0))
    median_draw = ImageDraw.Draw(median_img)

    for x in range(0, width):
        for y in range(0, height):
            # 用7*7，取med當(x,y)的輸出
            pixelList = getpixel(x,y,image,7)
            pixelList.sort(reverse = False)
            med = pixelList[int(len(pixelList)/2) + 1]
            median_draw.point((x,y), fill=(med))

    median_img.save('Median.jpg')
    return median_img

# 處理雜訊圖像
def Adaptive_Median_Filter(image):
    width, height = image.size

    adaptive_median_img = Image.new("L", (width,height), (0))
    adaptive_median_draw = ImageDraw.Draw(adaptive_median_img)

    for x in range(0, width):
        for y in range(0, height):
            # 3*3 5*5 7*7
            for num in range(3,8,2):
                pixelList = getpixel(x,y,image,num)
                pixelList.sort(reverse = False)
                Zxy = image.getpixel((x,y))

                min = pixelList[0]
                med = pixelList[int(len(pixelList)/2) + 1]
                max = pixelList[len(pixelList) - 1]

                if min < med < max:
                    # (x,y)不是雜訊，輸出(x,y)像素值
                    if min < Zxy < max:
                        adaptive_median_draw.point((x,y), fill=(Zxy))
                        break
                    # (x,y)是雜訊，輸出med
                    else:
                        adaptive_median_draw.point((x,y), fill=(med))
                        break
                # 7*7的(x,y)還是在白色或黑色區域，輸出(x,y)像素值
                elif num == 7:
                    adaptive_median_draw.point((x,y), fill=(Zxy))
                else: continue

    adaptive_median_img.save('AdaptiveMedian.jpg')
    return adaptive_median_img

def main():
    origin_img = Image.open('Origin.jpg')

    # 原始圖像轉灰階
    gray_img = Gray(origin_img)

    # 加入雜訊
    noise_img = Noise(gray_img)

    # 用Median Filter處理雜訊
    median_img = Median_Filter(noise_img)

    # 用Adaptive Median Filter處理雜訊
    adaptive_median_img = Adaptive_Median_Filter(noise_img)

    print('Finish!')

if __name__ == '__main__':
    main()