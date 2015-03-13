/* Buttons to USB Keyboard Example

   You must select Keyboard from the "Tools > USB Type" menu

   This example code is in the public domain.
*/

#include <Bounce.h>

// Create Bounce objects for each button.  The Bounce object
// automatically deals with contact chatter or "bounce", and
// it makes detecting changes very simple.
Bounce button0 = Bounce(10, 10);
Bounce button1 = Bounce(11, 10);  // 10 = 10 ms debounce time
Bounce button2 = Bounce(12, 10);  // which is appropriate for

static const float FACTOR = 60.0/1024;
void setup() {
  // Configure the pins for input mode with pullup resistors.
  // The pushbuttons connect from each pin to ground.  When
  // the button is pressed, the pin reads LOW because the button
  // shorts it to ground.  When released, the pin reads HIGH
  // because the pullup resistor connects to +5 volts inside
  // the chip.  LOW for "on", and HIGH for "off" may seem
  // backwards, but using the on-chip pullup resistors is very
  // convenient.  The scheme is called "active low", and it's
  // very commonly used in electronics... so much that the chip
  // has built-in pullup resistors!
  pinMode(10, INPUT);
  pinMode(11, INPUT);
  pinMode(12, INPUT);
  
  Keyboard.begin();

}

void loop() {
  // Update all the buttons.  There should not be any long
  // delays in loop(), so this runs repetitively at a rate
  // faster than the buttons could be pressed and released.
  button0.update();
  button1.update();
  button2.update();

  // Check each button for "falling" edge.
  // Type a message on the Keyboard when each button presses
  // Update the Joystick buttons only upon changes.
  // falling = high (not pressed - voltage from pullup resistor)
  //           to low (pressed - button connects pin to ground)
  if (button0.risingEdge()) {
//    val = analogRead(0);
//    char str[6];
//    str = sprintf("%f", val);
//    Keyboard.print(str);
    Keyboard.press('n');
  }
  if (button1.risingEdge()) {
    Keyboard.press(KEY_TAB);
    delay(100);
    Keyboard.release(KEY_TAB);
  }
  if (button2.risingEdge()) {
//    Keyboard.press(KEY_LEFT_SHIFT);
//    Keyboard.press(KEY_TAB);
//    delay(100);
//    Keyboard.release(KEY_TAB);
//    Keyboard.release(KEY_LEFT_SHIFT);

    uint32_t accumulated_value = 0;
    
    for(int i=0; i < 5; i++)
    {
      accumulated_value  += analogRead(0);
    }
    
    int val = accumulated_value / 5;

    String mystring = String(FACTOR*val);
    Keyboard.print(mystring);
  }

}

