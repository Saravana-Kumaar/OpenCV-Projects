import cv2

cap = cv2.VideoCapture("../OpenCV-Projects/1_number_plate_detection/source/car_vid.mp4")
detect_number_plate = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_russian_plate_number.xml")

counter=0

print("\n\t[[[press >>>>>>>> 's' <<<<<<<<< to save the snap shot of the detected number plate]]]\n")

print("\ttype 'img' for number plate detection in image and press enter")
print("\ttype 'vid' for number plate detection in image and press enter")

opt = str(input("\tEnter here >> "))


while opt == 'vid':
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


if opt == 'img':
    print("\n\t There are sample images to detect , please feel free to use it")
    print("\n\t type 'yes' to go for detection ")

    print("\n\t type 'no' , if you need to know how to try with different images\n")

    ans = str(input("\tEnter here >> "))

    if ans == 'yes':

        print("\n\t please enter the timing in seconds for the display after the detection ")

        s = str(input("\tEnter here >> "))

        image = cv2.imread("../OpenCV-Projects/1_number_plate_detection/source/car5.jpeg")
        image = cv2.resize(image , (1250 , 750))

        gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)

        number_plate = detect_number_plate.detectMultiScale(gray , 1.1 , 4)

        frameROI = 0
        for x , y , w, h in number_plate:
            cv2.rectangle(image , (x,y) , (x+w , y+h) , (0,255,0) , 2)
            cv2.putText(image, "Number Plate", (x, y - 7), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
            frameROI = image[y:y+h , x:x+w]

        cv2.imshow("detected image" , image)
        cv2.imshow("ROI" , frameROI)
        cv2.waitKey(int(f'{s}000'))
        cv2.destroyAllWindows()
    else:
        print(">>>>type 'yes' to read the instructions")

        option = str(input("\tEnter here >> "))

        if option == 'yes':
            print("\n\t\t To change the image , go to line 52 ")
            print("\n\t\t this below line ")
            print('''\n\timage = cv2.imread("../OpenCV-Projects/1_number_plate_detection/source/car5.jpeg") ''')
            print("\n\t\t now the change the number (from 1 to 5) instead of car1.jpeg ")
            print("\n\t\t you could add the image inside the source folder and detect it like ")
            print("\n\t\t let's say sample.jpeg is your image added and you want to detect it , change it accordingly as mentioned below")
            print('''\n\t\t image = cv2.imread("../OpenCV-Projects/1_number_plate_detection/source/sample.jpeg")''')

            print("\n\t\t\t Hope you understood ")
            print("\n\t\t\t HAPPY CODING!!!")
        else:
            print("\n\t\t\t HAPPY CODING!!!")


cap.release()
cv2.destroyAllWindows()