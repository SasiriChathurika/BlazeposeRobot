// First, download and unzip the Adafruit-Motor-Shield-library-master library from https://github.com/adafruit/Adafruit-Motor-Shield-library
// Extract the ZIP file and copy the folder into the Arduino/libraries directory (inside your Documents folder)

#include <AFMotor.h> 

// Initialise the four motors
AF_DCMotor front_left(2, MOTOR12_64KHZ);
AF_DCMotor rear_left(3, MOTOR12_64KHZ);
AF_DCMotor front_right(1, MOTOR12_64KHZ);
AF_DCMotor rear_right(4, MOTOR12_64KHZ);

// Pyserial Comunication
int incomingData;



void setup() {
  // put your setup code here, to run once:
  // Serial Communication
  Serial.begin(9600);

  // Motor PWM Speed Control (at a range 0-225)
  
}

void loop() {
  // If there's serial data available, read it
  if (Serial.available() > 0) {
    incomingData = Serial.read();

    // Control the motors based on the received data
    if (incomingData == 'E') {
      // Your motor control logic for 'E'
      // Motor Speeds
      front_left.setSpeed(0);
      rear_left.setSpeed(0);
      front_right.setSpeed(150);
      rear_right.setSpeed(150);
      // Motor Directions
      front_left.run(RELEASE);       
      rear_left.run(RELEASE);  
      front_right.run(RELEASE);       
      rear_right.run(RELEASE);
      
    } else if (incomingData == 'L') {
      // Your motor control logic for 'L'
      // Motor Speeds
      front_left.setSpeed(0);
      rear_left.setSpeed(0);
      front_right.setSpeed(150);
      rear_right.setSpeed(150);
      // Motor Directions
      front_left.run(RELEASE);       
      rear_left.run(RELEASE);  
      front_right.run(FORWARD);       
      rear_right.run(FORWARD);
      
    } else if (incomingData == 'F') {
      // Your motor control logic for 'F'
      // Motor Speeds
      front_left.setSpeed(225);
      rear_left.setSpeed(225);
      front_right.setSpeed(225);
      rear_right.setSpeed(225);
      // Motor Directions
      front_left.run(FORWARD);       
      rear_left.run(FORWARD);  
      front_right.run(FORWARD);       
      rear_right.run(FORWARD); 
      
    } else if (incomingData == 'R') {
      // Your motor control logic for 'R'
      // Motor Speeds
      front_left.setSpeed(150);
      rear_left.setSpeed(150);
      front_right.setSpeed(0);
      rear_right.setSpeed(0);
      // Motor Directions
      front_left.run(FORWARD);       
      rear_left.run(FORWARD);  
      front_right.run(RELEASE);       
      rear_right.run(RELEASE);
      
    }
  } else {
    // If there's no serial data available, release all motors
    front_left.run(RELEASE);
    rear_left.run(RELEASE);
    front_right.run(RELEASE);
    rear_right.run(RELEASE);
  }
}
