import cv2 
import numpy as np
from pyzbar.pyzbar import decode

image=cv2.imread("../OpenCV-Projects/3_detect_and_decode_qr_bar_codes/source/qr.png")
# image = cv2.resize(image , (1500 , 600))

decoded = decode(image)


for i in decoded:
    cv2.rectangle(image , (i.polygon[0].x , i.polygon[0].y) , (i.polygon[-2].x , i.polygon[-2].y)  , (0,255,0) , 4)
    data = i.data.decode('utf-8')
    cv2.putText(image , i.data.decode('utf-8') ,(i.polygon[0].x  , i.polygon[0].y)  , cv2.FONT_HERSHEY_COMPLEX_SMALL , 1 , (255 , 0 , 0 ) , 2)


cv2.imshow("The image" , image)

cv2.waitKey(5000)
cv2.destroyAllWindows()
# ---------------UNDER CONSTRUCTION ------------
