import cv2

cap = cv2.VideoCapture("../OpenCV-Projects/1_number_plate_detection/source/car_vid.mp4")
detect_number_plate = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_russian_plate_number.xml")

counter=0

print("\n\t[[[press >>>>>>>> 's' <<<<<<<<< to save the snap shot of the detected number plate]]]\n")

print("\ttype 'yes' for number plate detection")

opt = str(input("\tEnter here >> "))

while opt == 'yes':
    ret , frame = cap.read()
    frame = cv2.resize(frame , (1500 , 800))
    if ret:
        gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)

        number_plate = detect_number_plate.detectMultiScale(gray , 1.1 , 4)

        frameROI = 0
        for x , y , w, h in number_plate:
            cv2.rectangle(frame , (x,y) , (x+w , y+h) , (0,255,0) , 2)
            cv2.putText(frame, "Number Plate", (x, y - 7), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
            frameROI = frame[y:y+h , x:x+w]

        if cv2.waitKey(1) & 0xFF==ord('s'):
            cv2.imwrite("../OpenCV-Projects/1_number_plate_detection/predicted_number_plates/number_plate"+str(counter)+".jpg" , frameROI)
            cv2.rectangle(frame , (0 , 250) , (1500 , 400 ) , (255 , 0 , 0 ) , -1 )
            cv2.putText(frame , "Snap saved" , (500 , 350) , cv2.FONT_HERSHEY_COMPLEX , 2 , (255 , 0 , 255 ) , 2)
            cv2.waitKey(500)
            counter = counter + 1;
    
        cv2.imshow("the number plate" , frameROI)
        cv2.imshow("The output" , frame)

    else:
        break

cap.release()
cv2.destroyAllWindows()