import cv2
from cvzone.FaceDetectionModule import FaceDetector
import serial,time

#Initialize face detector from the cvzone package 
detector = FaceDetector(minDetectionCon=0.7, modelSelection=0)

#Initialize the serial communication with the arduino; change com based on the connected com port
ArduinoSerial=serial.Serial('com4',9600,timeout=0.1)

#Initialize the camera; change index based on the connected camera 
cap = cv2.VideoCapture(1)


#Initialize the variable to be sent to the arduino
# The firing square is 60px wide and high 
tolerance_x = 640//2-30
tolerance_y = 480//2-30
tolerance_w = 640//2+30
tolerance_h = 480//2+30

# The arming square is 25px wider and higher than the firing square
arming_tolerance_x = tolerance_x - 25
arming_tolerance_y = tolerance_y - 25
arming_tolerance_w = tolerance_w + 25
arming_tolerance_h = tolerance_h + 25
startMarker = 999
endMarker = 998
arm_motor = 0 
fire = 0
in_box_time = 0

# Start Checking for the faces 
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img, faces = detector.findFaces(img, draw=False)
    #If a lot of faces are found then take the first occurence of the face in the array
    if faces:
        face = faces[0]
        #Get the coordinates of the face
        x, y, w, h = face['bbox']
        cor_x = x+w//2
        cor_y = y+h//4
        
        # Check if the coordinates are inside the amring range of the MechaMachine
        if cor_x in range(arming_tolerance_x, arming_tolerance_w) and cor_y in range(arming_tolerance_y, arming_tolerance_h):
            arm_motor = 1
        else:
            arm_motor = 0
            
        # Check if the coordinates are inside the firing range of MechaMachine
        if cor_x in range(tolerance_x, tolerance_w) and cor_y in range(tolerance_y, tolerance_h):
            in_box_time = int(time.time() * 1000)
            if in_box_time > 500:
                fire = 1
        else: 
            in_box_time = 0 
            fire = 0
        
        #Prepare the string to be sent to the arduino
        string='S{0:d}X{1:d}Y{2:d}A{3:d}F{4:d}E{5:d}'.format((startMarker),(cor_x),(cor_y),(arm_motor),(fire),(endMarker))
        print(string)
        
        
        #Data structure sent to the arduino:
        # {S999X100Y100A0F0E998} 
        # S999 = Start Marker
        # X100 = X coordinate of the face
        # Y100 = Y coordinate of the face
        # A0 = Arm Motor (0 = Off, 1 = On)
        # F0 = Fire (0 = Off, 1 = On)
        # E998 = End Marker
        
        
        
        
        #Send the data to the aruino
        ArduinoSerial.write(string.encode('utf-8'))
        
        #Mark the face on the display
        cv2.circle(img, (cor_x,cor_y),2,(255,255,255),2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
        
    # This the constraint rectangle. 30 is the tolerable pixel length.
    cv2.rectangle(img,(tolerance_x, tolerance_y),(tolerance_w,tolerance_h),(0,0,0),3)
    cv2.rectangle(img,(arming_tolerance_x, arming_tolerance_y),(arming_tolerance_w, arming_tolerance_h),(255,0,0),3)
    
    cv2.imshow("MechaMachine",img)
    # press q to Quit
    if cv2.waitKey(1)&0xFF== ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
