# Connected Components
+ 影像中具有相同像素值且位置相鄰的像素組成的區域
+ Origin
<img src="https://github.com/gigilin7/Digital_Image_Processing/blob/main/HW4_Connected_Components/car.jpg" width="300" />

+ label 1 ( RGB轉為HSV格式，然後取HSV中的V值，此效果與灰階效果類似 )
<img src="https://github.com/gigilin7/Digital_Image_Processing/blob/main/HW4_Connected_Components/labeled_img.jpg" width="300" />

+ label 2 ( 黑轉白且白轉黑，確保後續能順利抓出需要的範圍 )
<img src="https://github.com/gigilin7/Digital_Image_Processing/blob/main/HW4_Connected_Components/labeled_img2.jpg" width="300" />

+ 取得connected components，得到我們要的車牌字母與數字
<img src="https://github.com/gigilin7/Digital_Image_Processing/blob/main/HW4_Connected_Components/output.jpg" width="300" />

+ 計算connected components的pixel數目 ( 若是雜訊就會去除 )

![image](https://user-images.githubusercontent.com/43805264/212847715-0c96d948-611c-4c57-a19b-130f259bdaef.png)

