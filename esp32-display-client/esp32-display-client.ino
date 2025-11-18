// 1. Include all necessary libraries
#include <TFT_eSPI.h>
#include <SPI.h>
#include <WiFi.h>
#include <HTTPClient.h>
// We must include the new library
#include <ArduinoJson.h>

// --- Wi-Fi Credentials ---
const char* ssid = "galeasus24";
const char* password = "galeasus2.4";
// ---

// --- This is your Mongoose OS server's RPC URL ---
const char* rpc_url = "http://192.168.0.67/rpc/Bed.Command";

// 8. --- Flags for touch logic ---
bool isFingerDown = false;      // Is the screen currently being touched?
bool isRockerActive = false;    // Was the last press on a rocker button?
// ---

// 3. Create instances of the objects
TFT_eSPI tft = TFT_eSPI();
HTTPClient http;

// 4. --- Define our Screen Layout (320x480 Portrait) ---
#define SCREEN_WIDTH  320
#define SCREEN_HEIGHT 480
#define CONTENT_WIDTH 300 // 320 - 20px for margins
#define MARGIN_X (SCREEN_WIDTH - CONTENT_WIDTH) / 2 // 10px
#define MARGIN_Y 15
#define GAP 12 // Gap between rows and buttons

// 5. --- Define UI Colors (from your CSS) ---
#define TFT_BACKGROUND 0x1F29 // #1f2937 (gray-800)
#define TFT_TEXT_LIGHT 0xF7DE // #f9fafb (gray-50)
#define TFT_TEXT_GRAY  0xE71C // #e5e7eb (gray-200)
#define TFT_FRAME      0x9D13 // #9ca3af (bed frame)
#define TFT_MATTRESS   0x8400 // #808000 (olive)

#define TFT_BLUE       0x3C1F // #3b82f6 (control-btn)
#define TFT_RED        0xF204 // #ef4444 (stop-btn)
#define TFT_GREEN      0x05E9 // #10b981 (flat-btn)
#define TFT_AMBER      0xFCA0 // #f59e0b (preset-btn)
#define TFT_VIOLET     0x8ACF // #8b5cf6 (light-btn)
#define TFT_GRAY       0x6B6D // #6b7280 (util-btn)
#define TFT_ORANGE     0xFD20 // A bright orange for "Sending"

// 6. --- Define our Buttons (Screen Coordinates) ---
// We will define all button Y positions in the drawUI() function.
// Widths:
int rocker_w = (CONTENT_WIDTH - (GAP * 2)) / 3; // (300 - 24) / 3 = 92
int rocker_h = 80;
int rocker_half_h = (rocker_h / 2) - 2;
int btn_h = 45; // Standard button height
int row_3_w = (CONTENT_WIDTH - (GAP * 2)) / 3; // 92
int row_2_w = (CONTENT_WIDTH - GAP) / 2; // 144

// 7. --- Your new, permanent PORTRAIT calibration data ---
uint16_t calData[5] = { 285, 3506, 301, 3583, 4 }; // <-- YOUR DATA IS IN!

// 8. --- A flag to prevent runaway presses ---
bool touch_pressed = false;

// 9. --- Button Region Definitions ---
// We'll define a struct to make this cleaner
struct Button {
  int x, y, w, h;
  const char* cmd;
};

// 9. --- Bed Position State ---
float currentHeadPos = 0.0;
float currentFootPos = 0.0;

// Define all our button regions
Button btn_head_up;
Button btn_head_down;
Button btn_all_up;
Button btn_all_down;
Button btn_foot_up;
Button btn_foot_down;
Button btn_stop;
Button btn_flat;
Button btn_zerog;
Button btn_snore;
Button btn_legs;
Button btn_p1;
Button btn_p2;
Button btn_set;
Button btn_light;

// --- Helper function declarations (defined after loop()) ---
void drawButton(int x, int y, int w, int h, const char* label, uint16_t color, int fontSize = 4);
void drawRockerButton(int x, int y, int w, int h, uint16_t color);
void drawVisualizer(int y_pos);
void sendCommand(const char* cmd);
void drawUI();

// =========================================================================
//    SETUP
// =========================================================================
void setup() {
  Serial.begin(115200);
  Serial.println("Booting up...");

  // 1. INITIALIZE THE DISPLAY
  tft.begin();
  tft.setRotation(0); // Set to PORTRAIT (320x480)
  
  // 2. --- SET PERMANENT CALIBRATION DATA ---
  tft.setTouch(calData); // This loads your numbers
  
  // 3. CONNECT TO WI-FI
  tft.fillScreen(TFT_BACKGROUND);
  tft.setTextColor(TFT_TEXT_LIGHT);
  tft.setTextSize(2);
  tft.drawCentreString("Connecting to WiFi...", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 2);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // 4. Draw the final UI
  Serial.println("\nWiFi connected! Drawing UI.");
  drawUI();
}


// =========================================================================
//    MAIN LOOP (New Visuals)
// =========================================================================
void loop() {
  uint16_t x, y;
  bool pressed = tft.getTouch(&x, &y);

  // --- Check for a NEW PRESS ---
  if (pressed && !isFingerDown) {
    isFingerDown = true;
    isRockerActive = false;
    
    Serial.printf("Touch Start at (x,y): %d, %d\n", x, y);

    // Check if this press is on a ROCKER button
    if ( (x > btn_head_up.x) && (x < (btn_head_up.x + btn_head_up.w)) &&
         (y > btn_head_up.y) && (y < (btn_head_up.y + btn_head_up.h)) ) {
      isRockerActive = true;
      // --- NEW: Draw pressed state ---
      tft.fillRoundRect(btn_head_up.x, btn_head_up.y, btn_head_up.w, btn_head_up.h, 8, TFT_ORANGE);
      tft.fillTriangle(btn_head_up.x + btn_head_up.w/2, btn_head_up.y + btn_head_up.h/2 - 6, btn_head_up.x + btn_head_up.w/2 - 8, btn_head_up.y + btn_head_up.h/2 + 6, btn_head_up.x + btn_head_up.w/2 + 8, btn_head_up.y + btn_head_up.h/2 + 6, TFT_TEXT_LIGHT);
      // ---
      sendCommand(btn_head_up.cmd);
    }
    else if ( (x > btn_head_down.x) && (x < (btn_head_down.x + btn_head_down.w)) &&
              (y > btn_head_down.y) && (y < (btn_head_down.y + btn_head_down.h)) ) {
      isRockerActive = true;
      // --- NEW: Draw pressed state ---
      tft.fillRoundRect(btn_head_down.x, btn_head_down.y, btn_head_down.w, btn_head_down.h, 8, TFT_ORANGE);
      tft.fillTriangle(btn_head_down.x + btn_head_down.w/2, btn_head_down.y + btn_head_down.h/2 + 6, btn_head_down.x + btn_head_down.w/2 - 8, btn_head_down.y + btn_head_down.h/2 - 6, btn_head_down.x + btn_head_down.w/2 + 8, btn_head_down.y + btn_head_down.h/2 - 6, TFT_TEXT_LIGHT);
      // ---
      sendCommand(btn_head_down.cmd);
    }
    // (Repeat this pattern for ALL_UP, ALL_DOWN, FOOT_UP, FOOT_DOWN)
    
    // ... (Example for FOOT_DOWN)
    else if ( (x > btn_foot_down.x) && (x < (btn_foot_down.x + btn_foot_down.w)) &&
              (y > btn_foot_down.y) && (y < (btn_foot_down.y + btn_foot_down.h)) ) {
      isRockerActive = true;
      // --- NEW: Draw pressed state ---
      tft.fillRoundRect(btn_foot_down.x, btn_foot_down.y, btn_foot_down.w, btn_foot_down.h, 8, TFT_ORANGE);
      tft.fillTriangle(btn_foot_down.x + btn_foot_down.w/2, btn_foot_down.y + btn_foot_down.h/2 + 6, btn_foot_down.x + btn_foot_down.w/2 - 8, btn_foot_down.y + btn_foot_down.h/2 - 6, btn_foot_down.x + btn_foot_down.w/2 + 8, btn_foot_down.y + btn_foot_down.h/2 - 6, TFT_TEXT_LIGHT);
      // ---
      sendCommand(btn_foot_down.cmd);
    }

    
    // Check if this press is on a PRESET button
    else if ( (x > btn_stop.x) && (x < (btn_stop.x + btn_stop.w)) &&
              (y > btn_stop.y) && (y < (btn_stop.y + btn_stop.h)) ) {
      drawButton(btn_stop.x, btn_stop.y, btn_stop.w, btn_stop.h, "STOP", TFT_ORANGE, 4);
      sendCommand(btn_stop.cmd);
      drawUI(); // Redraw UI after one-shot
    }
    else if ( (x > btn_flat.x) && (x < (btn_flat.x + btn_flat.w)) &&
              (y > btn_flat.y) && (y < (btn_flat.y + btn_flat.h)) ) {
      drawButton(btn_flat.x, btn_flat.y, btn_flat.w, btn_flat.h, "Flat", TFT_ORANGE, 4);
      sendCommand(btn_flat.cmd);
      drawUI(); // Redraw UI after one-shot
    }
    // ... (Repeat for zerog, snore, legs, p1, p2, set, light) ...
  }
  
  // --- Check for a RELEASE ---
  else if (!pressed && isFingerDown) {
    isFingerDown = false;

    // If the button we just released was a rocker, send STOP
    if (isRockerActive) {
      Serial.println("Rocker released, sending STOP");
      // Show STOP button pressed
      drawButton(btn_stop.x, btn_stop.y, btn_stop.w, btn_stop.h, "STOP", TFT_ORANGE, 4);
      sendCommand("STOP");
      isRockerActive = false;
      drawUI(); // Redraw UI after stop
    }
  }
}

// =========================================================================
//    HELPER FUNCTIONS
// =========================================================================

/**
 * @brief Helper function to draw the entire UI
 */
void drawUI() {
  tft.fillScreen(TFT_BACKGROUND);
  int current_y = MARGIN_Y;

  // 1. Draw Title
  tft.setTextColor(TFT_TEXT_GRAY);
  tft.drawCentreString("Bed Control", SCREEN_WIDTH / 2, current_y, 4); // Font 4
  current_y += 30; // Add space

  // 2. Draw Visualizer (y=45)
  drawVisualizer(current_y);
  current_y += 70; // Add space for visualizer (now at y=115)

  // 3. Draw Rocker Labels (y=115)
  int x1 = MARGIN_X;
  int x2 = x1 + rocker_w + GAP;
  int x3 = x1 + (rocker_w + GAP) * 2;
  
  tft.setTextColor(TFT_TEXT_GRAY);
  tft.setTextSize(1);
  tft.drawCentreString("HEAD", x1 + rocker_w/2, current_y, 2);
  tft.drawCentreString("ALL",  x2 + rocker_w/2, current_y, 2);
  tft.drawCentreString("FOOT", x3 + rocker_w/2, current_y, 2);
  current_y += 20; // Add space for labels (now at y=135)

  // 4. Draw Rocker Buttons (y=135)
  drawRockerButton(x1, current_y, rocker_w, rocker_h, TFT_BLUE);
  btn_head_up   = {x1, current_y, rocker_w, rocker_half_h, "HEAD_UP"};
  btn_head_down = {x1, current_y + rocker_half_h + 4, rocker_w, rocker_half_h, "HEAD_DOWN"};

  drawRockerButton(x2, current_y, rocker_w, rocker_h, TFT_BLUE);
  btn_all_up   = {x2, current_y, rocker_w, rocker_half_h, "ALL_UP"};
  btn_all_down = {x2, current_y + rocker_half_h + 4, rocker_w, rocker_half_h, "ALL_DOWN"};

  drawRockerButton(x3, current_y, rocker_w, rocker_h, TFT_BLUE);
  btn_foot_up   = {x3, current_y, rocker_w, rocker_half_h, "FOOT_UP"};
  btn_foot_down = {x3, current_y + rocker_half_h + 4, rocker_w, rocker_half_h, "FOOT_DOWN"};
  
  current_y += rocker_h + GAP; // Add height + gap (now at y=227)

  // 5. Draw Stop/Flat Row (y=227)
  drawButton(x1, current_y, row_2_w, btn_h, "STOP", TFT_RED, 4);
  btn_stop = {x1, current_y, row_2_w, btn_h, "STOP"};
  
  drawButton(x1 + row_2_w + GAP, current_y, row_2_w, btn_h, "Flat", TFT_GREEN, 4);
  btn_flat = {x1 + row_2_w + GAP, current_y, row_2_w, btn_h, "FLAT"};
  
  current_y += btn_h + GAP; // (now at y=284)

  // 6. Preset Row 1 (y=284)
  drawButton(x1, current_y, row_3_w, btn_h, "Zero G", TFT_AMBER, 2);
  btn_zerog = {x1, current_y, row_3_w, btn_h, "ZERO_G"};
  
  drawButton(x2, current_y, row_3_w, btn_h, "Anti-Snore", TFT_AMBER, 2);
  btn_snore = {x2, current_y, row_3_w, btn_h, "ANTI_SNORE"};
  
  drawButton(x3, current_y, row_3_w, btn_h, "Legs Up", TFT_AMBER, 2);
  btn_legs = {x3, current_y, row_3_w, btn_h, "LEGS_UP"};
  
  current_y += btn_h + GAP; // (now at y=341)

  // 7. Preset Row 2 (y=341)
  drawButton(x1, current_y, row_3_w, btn_h, "P1", TFT_AMBER, 4);
  btn_p1 = {x1, current_y, row_3_w, btn_h, "P1"};
  
  drawButton(x2, current_y, row_3_w, btn_h, "P2", TFT_AMBER, 4);
  btn_p2 = {x2, current_y, row_3_w, btn_h, "P2"};
  
  drawButton(x3, current_y, row_3_w, btn_h, "Set", TFT_GRAY, 4);
  btn_set = {x3, current_y, row_3_w, btn_h, "SET"};
  
  current_y += btn_h + GAP; // (now at y=398)

  // 8. Light Button (y=398)
  drawButton(x1, current_y, CONTENT_WIDTH, btn_h, "Toggle Light", TFT_VIOLET, 4);
  btn_light = {x1, current_y, CONTENT_WIDTH, btn_h, "LIGHT_TOGGLE"};
  
  // 9. Draw Status Lines (at bottom)
  tft.setTextColor(TFT_TEXT_LIGHT);
  tft.setTextSize(1);
  tft.drawString("Connected", 10, SCREEN_HEIGHT - 12, 1);
  tft.drawString(WiFi.localIP().toString(), SCREEN_WIDTH - 90, SCREEN_HEIGHT - 12, 1);
}

/**
 * @brief Draws the DYNAMIC bed visualizer
 */
void drawVisualizer(int y_pos) {
  int y_base = y_pos + 40; // Vertical position of the visualizer
  int x_start = MARGIN_X + 5;
  int x_end = SCREEN_WIDTH - MARGIN_X - 5;
  int base_w = x_end - x_start;
  int mattress_h = 12;

  // Draw Bed Base
  tft.fillRoundRect(x_start, y_base, base_w, 8, 3, TFT_FRAME);
  // Draw Legs
  tft.fillRoundRect(x_start + 10, y_base, 8, 15, 3, TFT_FRAME);
  tft.fillRoundRect(x_end - 18, y_base, 8, 15, 3, TFT_FRAME);
  
  // --- DYNAMIC MATTRESS DRAWING ---
  
  // 1. Define the 4 "joints" of the polyline
  int joint1_x = x_start;
  int joint2_x = x_start + (base_w * 0.35); // 35% mark
  int joint3_x = x_start + (base_w * 0.75); // 75% mark
  int joint4_x = x_end;

  // 2. Calculate Y positions based on state
  // We map the 0-100 position to a 0-30 pixel upward movement
  int y_flat = y_base - mattress_h;
  int head_y = y_flat - map(currentHeadPos, 0, 100, 0, 30);
  int foot_y = y_flat - map(currentFootPos, 0, 100, 0, 30);
  
  // 3. Draw the 3 segments as thick lines (polygons)
  
  // Head Segment (Joint 1 to 2)
  tft.fillTriangle(joint1_x, head_y, 
                   joint2_x, y_flat, 
                   joint1_x, head_y + mattress_h, 
                   TFT_MATTRESS);
  tft.fillTriangle(joint2_x, y_flat, 
                   joint1_x, head_y + mattress_h, 
                   joint2_x, y_flat + mattress_h, 
                   TFT_MATTRESS);

  // Middle Segment (Joint 2 to 3)
  tft.fillRoundRect(joint2_x, y_flat, (joint3_x - joint2_x), mattress_h, 0, TFT_MATTRESS);

  // Foot Segment (Joint 3 to 4)
  tft.fillTriangle(joint3_x, y_flat, 
                   joint4_x, foot_y, 
                   joint3_x, y_flat + mattress_h, 
                   TFT_MATTRESS);
  tft.fillTriangle(joint4_x, foot_y, 
                   joint3_x, y_flat + mattress_h, 
                   joint4_x, foot_y + mattress_h, 
                   TFT_MATTRESS);
}

/**
 * @brief Helper function to draw a standard single button
 */
void drawButton(int x, int y, int w, int h, const char* label, uint16_t color, int fontSize) {
  tft.fillRoundRect(x, y, w, h, 8, color);
  tft.setTextColor(TFT_TEXT_LIGHT);
  // Use font 2 for small text, 4 for large text
  int font = (fontSize <= 2) ? 2 : 4; 
  int y_offset = (font == 2) ? -6 : -8;
  tft.drawCentreString(label, x + w / 2, y + h / 2 + y_offset, font);
}

/**
 * @brief Helper function to draw a 2-part rocker button
 */
void drawRockerButton(int x, int y, int w, int h, uint16_t color) {
  int half_h = (h / 2) - 2; // Height of one button, with a small gap

  // Draw UP button
  tft.fillRoundRect(x, y, w, half_h, 8, color);
  tft.fillTriangle(x + w/2, y + half_h/2 - 6,    // Top point
                   x + w/2 - 8, y + half_h/2 + 6, // Bottom-left
                   x + w/2 + 8, y + half_h/2 + 6, // Bottom-right
                   TFT_TEXT_LIGHT);

  // Draw DOWN button
  tft.fillRoundRect(x, y + half_h + 4, w, half_h, 8, color);
  tft.fillTriangle(x + w/2, y + half_h + 4 + half_h/2 + 6, // Bottom point
                   x + w/2 - 8, y + half_h + 4 + half_h/2 - 6, // Top-left
                   x + w/2 + 8, y + half_h + 4 + half_h/2 - 6, // Top-right
                   TFT_TEXT_LIGHT);
}
/**
 * @brief Helper function to send the RPC command
 */
void sendCommand(const char* cmd) {
  // ... (Keep the visual "pressed" logic from your loop) ...
  
  // 1. Build the JSON body
  String json_body = "{\"cmd\": \"" + String(cmd) + "\"}";
  
  // 2. Send the HTTP POST request
  Serial.print("Sending POST: "); Serial.println(json_body);
  
  http.begin(rpc_url);
  http.setTimeout(5000); 
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(json_body);

  // 3. Check the result
  if (httpCode > 0) {
    String payload = http.getString();
    Serial.printf("HTTP Code: %d, Response: %s\n", httpCode, payload.c_str());

    // --- 4. NEW: PARSE THE JSON RESPONSE ---
    StaticJsonDocument<256> doc; // Create a JSON document
    deserializeJson(doc, payload); // Parse the response

    // Read the values and update our global variables
    currentHeadPos = doc["headPos"];
    currentFootPos = doc["footPos"];
    
    Serial.printf("New State: Head=%.2f, Foot=%.2f\n", currentHeadPos, currentFootPos);
    // ---
    
  } else {
    Serial.printf("Error on HTTP request: %d\n", httpCode);
  }
  
  http.end();
  
  // 5. Redraw the UI
  // This will now call the new drawVisualizer()
  // which will use the new head/foot variables.
  drawUI();
}



