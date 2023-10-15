import cv2
import numpy as np

'''
work flow -> image -> gray -> edges -> contour -> area -> perimeter with arclength -> gives four corner points -> warp it 
'''

print("want to detect in image or stream\n")
print("Enter 'img' for image\n")
print("Enter 'vid' for video\n")

opt = str(input("Enter here >>>> "))

default_width = 600
default_height = 800

def preprocess_image(image):
    #gray scale image will be more helpfull in finding edges
    gray_image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    #apply canny edge detector
    '''
        # Low Threshold: This threshold determines the minimum intensity gradient required 
                         for a pixel to be considered as a potential edge point
        # High Threshold: This threshold establishes the minimum gradient 
                          value for a pixel to be considered an initial edge point
    '''
    low = 50
    high = 300
    edged_image = cv2.Canny( gray_image , low , high)
    # dilate and erode it 
    '''
    Dilating and eroding together (morphological opening) smoothes 
    an image by removing noise while preserving larger object structures.
    '''
    kernel = np.ones((1,1) , np.uint8)
    image_dilation = cv2.dilate(edged_image , kernel , iterations=2)
    image_erosion = cv2.dilate(image_dilation , kernel , iterations=1)
    return image_erosion

def contour(preprocessed_image , image):
    # a contour is a continuous curve or boundary that represents the outline of an object in an image
    detected_contour , hirearchy = cv2.findContours(preprocessed_image , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)
    image_copy = image.copy()
    
    maxArea = 0
    points_of_large_contour = np.array([])

    for i in detected_contour:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i , True)
            approx = cv2.approxPolyDP(i , 0.02*peri , True)
            if area > maxArea and len(approx) == 4:
                points_of_large_contour = approx

    print("The large contour with 4 corner points" , points_of_large_contour)
    cv2.drawContours(image_copy , detected_contour , -1 ,(5 , 255 , 0) , 3)
    cv2.drawContours(image_copy , points_of_large_contour , -1 ,(5 , 255 , 255) , 15)
    return image_copy , points_of_large_contour

def reorder_points(points):
    sums = np.sum(points, axis=(1, 2))
    sorted_indices = np.argsort(sums)
    sorted_points = points[sorted_indices]
    return sorted_points
    

def wrap_perspective(image, points):
    points1 = np.float32(reorder_points(points))
    points2 = np.float32([[0,0] , [default_width , 0] , [0 , default_height] , [default_width , default_height]])
    ROI = cv2.getPerspectiveTransform(points1 , points2)
    output_image = cv2.warpPerspective(image , ROI , (default_width , default_height))
    return output_image


if opt == 'img':
    image = cv2.imread("../OpenCV-Projects/2_document_scanner/source/doc1.jpeg")
    image = cv2.resize(image , (default_width , default_height))
    cv2.imshow("The image" , image)
    preprocessed_image = preprocess_image(image)
    cv2.imshow("preprocessed_image" , preprocessed_image)
    contour_image , points = contour(preprocessed_image , image)
    cv2.imshow("contour image" , contour_image)
    output_image = wrap_perspective(image , points)
    cv2.imshow("The output" , output_image)
else:
    counter = 0
    cap = cv2.VideoCapture(0)

    print("Press 's' to save the snap shot\n")
    print("press 'q' to quit")

    while True:
        ret , frame = cap.read()
        if ret:
            frame_copy = frame.copy()
            frame_pre = preprocess_image(frame)
            contour_image , points = contour(frame_pre , frame_copy)
            cv2.imshow("The output" , contour_image)

            document = 0
            if len(points) == 4:
                output_image = wrap_perspective(frame_copy , points)
                cv2.imshow("The document" , output_image)
                document = output_image

            cv2.imshow("The output" , contour_image)

            if cv2.waitKey(1) & 0xFF==ord('s'):
                cv2.imwrite("../OpenCV-Projects/2_document_scanner/scanned_documents/document"+str(counter)+".jpg" , output_image)
                cv2.rectangle(frame , (0 , 250) , (1500 , 400 ) , (255 , 0 , 0 ) , -1 )
                cv2.putText(frame , "Snap saved" , (500 , 350) , cv2.FONT_HERSHEY_COMPLEX , 2 , (255 , 0 , 255 ) , 2)
                cv2.waitKey(500)
                counter = counter + 1;
            
            if 0xFF==ord('q'):
                break
        else:
            break
    cap.release()

cv2.waitKey(10000)
cv2.destroyAllWindows()