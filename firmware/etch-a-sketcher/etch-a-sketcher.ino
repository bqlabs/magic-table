/* 
  etch-a-sketcher 
  -----------------------------------
  Creative computer interface
  
  author: def
*/

#include <Encoder.h>
#include <Bounce.h>

//-- Pins
const int boardLedPin = 13;
const int userLedPins[4] = {12, 14, 11, 15};

const int encoderLeftButtonPin = 2;
const int encoderRightButtonPin = 21;

const int buttonPins[4] = {10, 16, 9, 17};


//-- Global objects:
Encoder knobLeft(1, 0);
Encoder knobRight(23, 22);

Bounce encoderLeftButton  = Bounce(encoderLeftButtonPin, 10);
Bounce encoderRightButton = Bounce(encoderRightButtonPin, 10);

Bounce buttons[4] = { Bounce(buttonPins[0], 10),
                      Bounce(buttonPins[1], 10),
                      Bounce(buttonPins[2], 10),
                      Bounce(buttonPins[3], 10)};

//-- State-related variables & defines
#define MODE_0 0  //-- Emulate cursor position
#define MODE_1 1  //-- Emulate mouse scroll
#define MODE_2 2  //-- Emulate keyboard arrows
#define MODE_3 3  //-- ?

int state = MODE_0;

//-- Encoder position related variables
long positionLeft  = 0;
long positionRight = 0;

void setup() 
{  
  //-- Buttons & leds
  pinMode(boardLedPin, OUTPUT);
  
  for(int i = 0; i < 4; i++)
  {
    pinMode(userLedPins[i], OUTPUT);
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
  
  //-- Encoder pins config
  pinMode(encoderLeftButtonPin, INPUT_PULLUP);
  pinMode(encoderRightButtonPin, INPUT_PULLUP);
  
  //-- Keyboard, mouse, and other HID init
  Keyboard.begin();
  Mouse.begin();
  
  //-- Init lights sequence
  for(int i = 0; i < 4; i++)
  {
    digitalWrite(userLedPins[i], HIGH);   // set the LED on
    delay(200);                  // wait for a second
    digitalWrite(userLedPins[i], LOW);    // set the LED off
    delay(200);                  // wait for a second
  }
  
  //-- Initial button update (to cleanup initial rising edge detect (?))
  encoderLeftButton.update();
  encoderRightButton.update();
  
  for(int i = 0; i < 4; i++)
    buttons[i].update();
  
}


void loop() 
{
  //-- Update button status
  encoderLeftButton.update();
  encoderRightButton.update();
  
  for(int i = 0; i < 4; i++)
    buttons[i].update();
    

  
  //-- Things to be done on each state:
  if (state == MODE_0)
  {
    //-- Things to do here
    digitalWrite(userLedPins[0], HIGH);
    digitalWrite(userLedPins[1], LOW);
    digitalWrite(userLedPins[2], LOW);
    digitalWrite(userLedPins[3], LOW);
  }
  else if (state == MODE_1)
  {
      mode1();
  }
  else if (state == MODE_2)
  {
      mode2();
  }
  else if (state == MODE_3)
  {
    //-- Things to do here
    digitalWrite(userLedPins[0], LOW);
    digitalWrite(userLedPins[1], LOW);
    digitalWrite(userLedPins[2], LOW);
    digitalWrite(userLedPins[3], HIGH);
  }
  
  //-- State transitions:
  for(int i = 0; i < 4; i++)
    if (buttons[i].risingEdge())
    {
      //-- Change state variable & reset knobs
      state = i;
      positionLeft  = 0;
      positionRight = 0;
      knobLeft.write(0);
      knobRight.write(0);
    }
}

void mode1()
{
    //-- Mode 1: position control
    //----------------------------------
    digitalWrite(userLedPins[0], LOW);
    digitalWrite(userLedPins[1], HIGH);
    digitalWrite(userLedPins[2], LOW);
    digitalWrite(userLedPins[3], LOW);
    
    //-- Read encoders
    long newLeft, newRight;
    newLeft = knobLeft.read();
    newRight = knobRight.read();
    
    //-- Do things if encoders where moved
  
    if (newLeft > positionLeft)
    {
      //-- Left turned right
      Mouse.move(5, 0, 0);  
    }
    else if (newLeft < positionLeft)
    {
      //-- Left turned left
      Mouse.move(-5, 0, 0);  
    }
      
    if (newRight > positionRight)
    {
      //-- Right turned right
      Mouse.move(0, 5, 0);        
    }
    else if (newRight < 0)
    {
      //-- Right turned left
      Mouse.move(0, -5, 0);       
    }
    
    //-- Update encoder counters
    positionLeft = newLeft;
    positionRight = newRight;
    delay(50);      
}
void mode2()
{
    //-- Mode 2: arrow control
    //----------------------------------
    digitalWrite(userLedPins[0], LOW);
    digitalWrite(userLedPins[1], LOW);
    digitalWrite(userLedPins[2], HIGH);
    digitalWrite(userLedPins[3], LOW);
    
    //-- Read encoders
    long newLeft, newRight;
    newLeft = knobLeft.read();
    newRight = knobRight.read();
    
    //-- Do things if encoders where moved
  
    if (newLeft > positionLeft)
    {
      //-- Left turned right
      Keyboard.press(KEY_LEFT_ARROW);
      digitalWrite(boardLedPin, HIGH);
      delay(100);
      Keyboard.release(KEY_LEFT_ARROW);
      digitalWrite(boardLedPin, LOW);    
    }
    else if (newLeft < positionLeft)
    {
      //-- Left turned left
      Keyboard.press(KEY_RIGHT_ARROW);
      digitalWrite(boardLedPin, HIGH);
      delay(100);
      Keyboard.release(KEY_RIGHT_ARROW);
      digitalWrite(boardLedPin, LOW);     
    }
      
    if (newRight > positionRight)
    {
      //-- Right turned right
      Keyboard.press(KEY_UP_ARROW);
      digitalWrite(boardLedPin, HIGH);
      delay(100);
      Keyboard.release(KEY_UP_ARROW); 
      digitalWrite(boardLedPin, LOW);        
    }
    else if (newRight < positionRight)
    {
      //-- Right turned left
      Keyboard.press(KEY_DOWN_ARROW);
      digitalWrite(boardLedPin, HIGH);
      delay(100);
      Keyboard.release(KEY_DOWN_ARROW);
      digitalWrite(boardLedPin, LOW);        
    }
    
    //-- Update encoder counters
    positionLeft = newLeft;
    positionRight = newRight;
    delay(100);      
}
