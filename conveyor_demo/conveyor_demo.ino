
// included libraries
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
// NOTE that LED backlight for LCD is connected to pin 10!
const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// ultrasonic sensor
const int trigPin = 13;
const int echoPin = 12;
const int threshold = 6; // distance is cm
long duration;
int distance;
bool objectInFront = false;

// motor controller
int in1 = 11; // controls motor spin direction
int in2 = 2;  // controls motor spin direction
int EnA = 3; // connect to PWM pin and to ENA on motor controller to control motor speed via PWM

// variables
int count = 0;
int tmpCount = 0;
unsigned long countDelta = 0;
unsigned long lastMillis = 0;  // variable to store the last time interval measurement
unsigned long interval = 10000;  // time interval in milliseconds

// function prototypes
void turnMotor(int speed);

// setup function
void setup() {

    lcd.begin(16, 2);               // set up the LCD's number of columns and rows
    
    lcd.print("Count | Units/hr");  // LCD header

    // ultrasonic sensor
    pinMode(trigPin, OUTPUT);       // Sets the trigPin as an Output
    pinMode(echoPin, INPUT);        // Sets the echoPin as an Input

    // motor controller
    pinMode(11, OUTPUT);
    pinMode(2, OUTPUT); 
    pinMode(3, OUTPUT);
}

// loop function
void loop() {
    unsigned long currentMillis = millis();

    lcd.setCursor(0, 1);

    // moving time interval to find estimated production per hour
    if (currentMillis - lastMillis >= interval) {
        // calculate the change in count value
        countDelta = count - tmpCount;

        // set tmp count to current count at start of new 10 second window
        tmpCount = count;
        lastMillis = currentMillis;
    }

    // DC motor control ----------------------------------------------------
    int speed = analogRead(A5); //declaring and reading value from the pin
    speed = map(speed, 0, 1023, 0, 255);

    turnMotor(speed);   // turn motor
    
    // ---------------------------------------------------------------------

    // Ultrasonic sensor object detection ----------------------------------
    //Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance
    distance = duration * 0.034 / 2;

    //  --------------------------------------------------------------------

    // count logic
    if (distance < threshold && !objectInFront) {
        objectInFront = true;
        count++;
    } else if (distance > threshold && objectInFront) {
        objectInFront = false;
    }

    // LCD display ---------------------------------------------------------
    // set the cursor to column 0, line 1
    // (note: line 1 is the second row, since counting begins with 0):
    lcd.setCursor(0, 1);
  
    // print number of objects seen by ultrasonic sensor
    lcd.print(count);

    lcd.setCursor(6,1);
    lcd.print("|");

    lcd.setCursor(8,1);
    // print the total units production in units/hr based on 10 second moving window

    // convert delta is 10 seconds to production per hour
    // countDelta * 6 * 60
    lcd.print(countDelta * 6 * 60);

    // --------------------------------------------------------------------
}

// function to control DC motor speed via PWM
void turnMotor(int speed)  { 
    digitalWrite(in1, LOW);     // change to HIGH to spin motor in other direction
    digitalWrite(in2, HIGH);    // change to LOW to spin motor in other direction
    analogWrite(EnA, speed);    // command motor
}
