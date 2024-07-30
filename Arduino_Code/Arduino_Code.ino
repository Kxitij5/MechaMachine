#include<Servo.h>

//------- info for serial communication-----
// consider changing byte to int, cuz byte will truncate the data of x and y coordinates to lie in the range of (0,255)
const int buffer_size = 6;
int input_buffer[buffer_size];
const int startMarker = 999;
const int endMarker = 998;
boolean data_rcvd = false;


//------- info for servos ---------
Servo pan, tilt, trigger;
int width = 640, height = 480;  // resolution of the video
int xpos = 90, ypos = 90;  // variables for movement angles of pan -> xpos, tilt -> ypos
const int angle = 1; // increment or decrement to the xpos and ypos to make the servos move




//----- info for arming MehcaMachine -------
const int arm_motor = 7;
boolean is_armed = false;

//----- info for firing and reloading ------
boolean is_firing = false;
boolean reloading = false;
boolean can_fire = false;
const int laser = 13;

unsigned long fire_start_time = 0;
unsigned long fire_current_time = 0;
const long fire_time = 150;

unsigned long reload_start_time = 0;
unsigned long reload_current_time = 0;
const long reload_time = 2 * fire_time;

const int trigger_pulled = 180;    // Angle of the trigger servo when at rest
const int trigger_pushed = 125;    // Angle of the trigger servo when pushed

void setup() {
  // put your setup code here, to run once:
  pan.attach(9);
  pan.write(xpos);
  tilt.attach(10);
  tilt.write(ypos);
  trigger.attach(11);
  trigger.write(trigger_pulled);
  pinMode(arm_motor,OUTPUT);
  pinMode(laser,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(laser,HIGH);
  getData();
  arm();
  if(data_rcvd){
    track_face();
    set_trigger();
    arm();
    fire();
    }
  
  
}

void getData(){
// input from serial communication will be of this structure:
//  [startMarker, x_coordinate, y_coordinate, arm_motor, fire, endMarker]
// startMarker  -> this variable indicates the start of the data being sent by the python code.
// x_coordinate -> this indicates the x coordinates of the face being sent by the python code.
// y_coordinate -> this indicates the y coordinates of the face being sent by the python code.
// arm_motor    -> this indicates whether MechaMachine should be armed or not
// fire         -> this indicates whether MechaMachine should shoot or not
// endMarker -> this is the end marker of the data being sent by the computer.

if (Serial.available() > 0)
  {
    data_rcvd = true;
    if (Serial.read() == 'S')
    {
      input_buffer[0] = Serial.parseInt();  
      if (Serial.read() == 'X')
        input_buffer[1] = Serial.parseInt();
        if (Serial.read() == 'Y')
          input_buffer[2] = Serial.parseInt();
          if (Serial.read() == 'A')
            input_buffer[3] = Serial.parseInt();
            if (Serial.read() == 'F')
              input_buffer[4] = Serial.parseInt();
              if (Serial.read() == 'E')
                input_buffer[5] = Serial.parseInt();
        
    }
  }  else{
    data_rcvd = false;
    }
  

}


void track_face(){
  int face_x, face_y;
  face_x = input_buffer[1];
  face_y = input_buffer[2];
  // if the servo degree is outside its range of the rectangle perimeter of 30 pixels
  if (face_x > width / 2 + 30)
      xpos += angle;
    if (face_x < width / 2 - 30)
      xpos -= angle;
    if (face_y < height / 2 + 30)
      ypos += angle;
    if (face_y > height / 2 - 30)
      ypos -= angle;

      
//A better acceleration based movement of the servos:
/* const int xThreshhold[] = {96, 192, 290, 446, 542, 640};
 *  const int yThreshhold[] = {70, 140, 210, 340, 410, 480};
 *  
 *  const int xSteps[] = {-3, -2, -1, 1, 2, 3};
 *  const int ySteps[] = {3, 2, 1, -1, -2, -3};
 *  
 *  for(int i = 0 ; i < sizeof(xThreshold); i++){
 *    if(face_x < xThreshold[i]){
 *      xpos += xSteps[i];
 *    }
 *  }
 *  
 *  for(int i = 0 ; i < sizeof(yThreshold); i++){
 *    if(face_y < yThreshold[i]){
 *      ypos += ySteps[i];
 *    }
 *    
 *    
 *  }
 */

    
    if (xpos >= 180)
      xpos = 180;
    else if (xpos <= 0)
      xpos = 0;
    if (ypos >= 180)
      ypos = 180;
    else if (ypos <= 0)
      ypos = 0;

    pan.write(xpos);
    tilt.write(ypos);




}


void arm(){
  if(input_buffer[3] == 1){
    digitalWrite(arm_motor,HIGH);
    is_armed = true;
    }
  else{
    digitalWrite(arm_motor,LOW);
    is_armed = false;
    }
}


void set_trigger(){
   if(input_buffer[4] == 1){
    if(!is_firing && !reloading){
      can_fire = true;
      }
    }
   else{
    can_fire = false;
    }
}


void fire(){
    if(can_fire && !is_firing && is_armed){
      fire_start_time = millis();
      reload_start_time = millis();
      is_firing = true;
    }
    fire_current_time = millis();
    reload_current_time = millis();

    if(is_firing && fire_current_time - fire_start_time < fire_time){
      trigger.write(trigger_pushed);
      }
    else if(is_firing && fire_current_time - fire_start_time < reload_time){
      trigger.write(trigger_pulled);
      }
    else if(is_firing && reload_current_time - reload_start_time > reload_time){
      is_firing = false;
      }
}
