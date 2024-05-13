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
  
  // Initialize motor speeds
  front_left.setSpeed(0);
  rear_left.setSpeed(0);
  front_right.setSpeed(0);
  rear_right.setSpeed(0);

  // Motor PWM Speed Control (at a range 0-225)
  
}

void loop() {
  // Check if there's data available from serial
  if (Serial.available()>0){
    incomingData = Serial.read();
    
    if (incomingData == 'R'){
      // Command for left movement
      // Motor Speeds
      //front_left.setSpeed(150);
      //rear_left.setSpeed(150);
      front_right.setSpeed(150);
      rear_right.setSpeed(150);
      // Motor Directions
      front_left.run(RELEASE);       
      rear_left.run(RELEASE);  
      front_right.run(FORWARD);       
      rear_right.run(FORWARD);
      delay(200);
    }
    
    else if (incomingData == 'F') {
      // Command for forward movement
      // Motor Speeds
      front_left.setSpeed(200);
      rear_left.setSpeed(200);
      front_right.setSpeed(200);
      rear_right.setSpeed(200);
      // Motor Directions
      front_left.run(FORWARD);       
      rear_left.run(FORWARD);  
      front_right.run(FORWARD);       
      rear_right.run(FORWARD); 
      delay(200);
    }
    
    else if (incomingData == 'L'){
      // Command for right movement
      // Motor Speeds
      front_left.setSpeed(150);
      rear_left.setSpeed(150);
      //front_right.setSpeed(150);
      //rear_right.setSpeed(150);
      // Motor Directions
      front_left.run(FORWARD);       
      rear_left.run(FORWARD);  
      front_right.run(RELEASE);       
      rear_right.run(RELEASE);
      delay(200);
     
    }

    else{
      // Error handling for unexpected input
      front_left.run(RELEASE);       
      rear_left.run(RELEASE);  
      front_right.run(RELEASE);       
      rear_right.run(RELEASE);
      Serial.println("Invalid command received.");
    }
  }
  
  else {
    // If no command received, release all motors
    front_left.run(RELEASE);       
    rear_left.run(RELEASE);  
    front_right.run(RELEASE);       
    rear_right.run(RELEASE);
  }
  
}
