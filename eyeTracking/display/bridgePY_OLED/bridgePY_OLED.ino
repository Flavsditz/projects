/*
  This sketch is responsible to bridge the python script and the hardware of the NKKSwitch OLED Display.
  
  created by Flavio Diez 
  as part of the final thesis 
  
  pin 10  -  CS
  pin 11  -  MOSI
  pin 12  -  MISO (not used)
  pin 13  -  CLK
  
  pin 09  -  Shutdown from VCC 
             0 - low power shutdown mode, 
             1 - normal operation mode
*/

// include the SPI library
#include<SPI.h>

// Constant Definitions

#define CS    10
#define MOSI  11
#define MISO  12
#define CLK   13

#define SHTDN 9
#define DATA  8
#define RST   7

void setup() {
  // Initialize the SPI
  SPI.begin()
  
  // Start the display
  initialize()
  
}

void loop() {
  
}

/*
 * Initialization from the OLED Display
 */
void initialize(){
  // 1. By design VCC should be disabled upon power up. 
  
  // 2. The Reset pin should be set to low for 3 µs and then set to high. 

  // 3. Enable VCC. 

  // 4. Initialize the OLED controller by transmitting the commands and data from the appropriate table of the documentation.
}
