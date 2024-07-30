import cv2
import torch
import serial,time

# Load YOLOv5 model
model = torch.hub.load(r"<path/to/the/git/cloned/yolov5/repository>", "custom", path=r"<path/to/your/quantized/model>", source="local",device = 'cpu')

# Specify the confidence threshold
confidence_threshold = 0.5

# Initialize the webcam; change the index based on the index of the camera
cap = cv2.VideoCapture(0)

# Initialize the arduino UNO; change the port based on the connected com port
ArduinoSerial=serial.Serial('com4',9600,timeout=0.1)

# Initialize the variables for the string to be sent to arduino
tolerance_x = 640//2-30
tolerance_y = 480//2-30
tolerance_w = 640//2+30
tolerance_h = 480//2+30
arming_tolerance_x = tolerance_x - 25
arming_tolerance_y = tolerance_y - 25
arming_tolerance_w = tolerance_w + 25
arming_tolerance_h = tolerance_h + 25
startMarker = 999
endMarker = 998
arm_motor = 0 
fire = 0
in_box_time = 0

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

try:
    while True:
        
        ret, frame = cap.read()
        cv2.flip(frame,1)
        if not ret:
            print("Error: Could not read frame.")
            break

        # Perform inference
        results = model(frame)

        # Process results
        for result in results.xyxy[0]:  # xyxy format: (x1, y1, x2, y2, confidence, class)
            x1, y1, x2, y2, confidence, cls = result
            
            #Check for confidence
            if confidence > confidence_threshold:
                
                #Check if it is enemy? 0 -> enemy 1 -> friend; change the class based on the model.
                if int(cls)==1:
                    
                    #convert all the values from YOLOv5 inference to int for ease of use.
                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)
                    
                    # Calculate the center or the point on the face to be tracked.
                    cor_x = (x1+x2)//2
                    cor_y = (y1+y2)//2
                                        
                    #Check if the face coordinates are incide the range of arming square
                    if cor_x in range(arming_tolerance_x, arming_tolerance_w) and cor_y in range(arming_tolerance_y, arming_tolerance_h):
                        arm_motor = 1
                    else:
                        arm_motor = 0
                        
                    #Check if the face coordinates are in in tolerence zone for firing 
                    if cor_x in range(tolerance_x, tolerance_w) and cor_y in range(tolerance_y, tolerance_h):
                        in_box_time = int(time.time() * 1000)
                        if in_box_time > 500:
                            fire = 1
                    else: 
                        in_box_time = 0 
                        fire = 0
                        
                    #Prepare the string to send to the Arduino
                    string='S{0:d}X{1:d}Y{2:d}A{3:d}F{4:d}E{5:d}'.format((startMarker),(cor_x),(cor_y),(arm_motor),(fire),(endMarker))
                    print(string)
                    
                    #Send the string to the Arduino
                    ArduinoSerial.write(string.encode('utf-8'))
                    
                    #Mark the Bounding box of the face and the point blank
                    cv2.circle(frame, (cor_x,cor_y),2,(255,255,255),2)
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),3)
                    
                    
                else:
                    #If a friend is detected then don't shoot.
                    #convert all the values from YOLOv5 inference to int for ease of use.
                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)
                    #Calculate the center or the point on the face to be tracked.
                    cor_x = (x1+x2)//2
                    cor_y = (y1+y2)//2
                    
                    print("Friend Detected Shooting Halted.")
                    
                    #Mark the Bounding box of the face and the point blank
                    cv2.circle(frame, (cor_x,cor_y),2,(255,255,255),2)
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
                    
                    
                    
                
                
        #Display the resulting frame
        cv2.imshow('MechaMachine', frame)

        #Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
