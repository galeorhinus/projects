#include <TFT_eSPI.h> // We only need the display library
#include <SPI.h>

// --- THIS WAS THE MISSING LINE ---
TFT_eSPI tft = TFT_eSPI(); // Create the display object
// ---

// This array will hold our new calibration data
uint16_t calibrationData[5]; 

void setup() {
  Serial.begin(115200);
  Serial.println("Booting up for PORTRAIT calibration...");

  // 1. Initialize the display in PORTRAIT mode
  tft.begin();
  tft.setRotation(0); // 0 = Portrait (320x480)
  tft.fillScreen(TFT_BLACK);
  
  // 2. Run the calibration routine
  Serial.println("Starting Touch Calibration... Please tap the dots.");
  tft.calibrateTouch(calibrationData, TFT_WHITE, TFT_RED, 15);
  Serial.println("Calibration complete.");

  // 3. Force-print the result in the exact format we need
  Serial.println("--- Your New PORTRAIT Calibration Line Is: ---");
  Serial.print("uint16_t calData[5] = { ");
  Serial.print(calibrationData[0]); Serial.print(", ");
  Serial.print(calibrationData[1]); Serial.print(", ");
  Serial.print(calibrationData[2]); Serial.print(", ");
  Serial.print(calibrationData[3]); Serial.print(", ");
  Serial.print(calibrationData[4]); // This is the rotation
  Serial.println(" };");
  Serial.println("----------------------------------------------");

  // 4. Stop here
  tft.fillScreen(TFT_BLACK);
  tft.drawCentreString("Calibration Done.", 160, 230, 2);
  tft.drawCentreString("Check Serial Monitor.", 160, 260, 2);
}

void loop() {
  // We loop forever so the sketch doesn't restart
  while(1) {
    delay(100);
  }
}