#include <Arduino.h>
#include <WiFiManager.h>
#include <LittleFS.h>
#include <WebServer.h>
#include <ESPmDNS.h>  // Include mDNS library

WebServer server(80);

void handleNotFound() {
  server.send(404, "text/plain", "404: Not Found");
}

void setup() {
  Serial.begin(115200);
  
  // 1. Mount File System
  if(!LittleFS.begin(true)){
    Serial.println("An Error has occurred while mounting LittleFS");
    return;
  }

  // 2. Connect to Wi-Fi
  WiFiManager wm;
  // wm.resetSettings(); // Uncomment to force the setup portal to appear
  
  // --- NEW: Add Custom Text to Portal ---
  // This tells the user where to go AFTER the portal closes.
  WiFiManagerParameter custom_text("<br/><div style='text-align: center;'>After setup, access this device at:<br/><h3>http://esp32.local/</h3></div>");
  wm.addParameter(&custom_text);

  bool res = wm.autoConnect("ESP32-Setup-Portal");
  if(!res) {
    Serial.println("Failed to connect");
    ESP.restart();
  } 
  
  Serial.println("Connected to Wi-Fi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // --- NEW: Start mDNS Responder ---
  // This allows the user to type "http://esp32.local" instead of the IP
  if (!MDNS.begin("esp32")) {
      Serial.println("Error setting up MDNS responder!");
  } else {
      Serial.println("mDNS responder started: http://esp32.local");
      // Add service to let network scanners find us
      MDNS.addService("http", "tcp", 80);
  }

  // 3. Serve the HTML with Manual Replacement
  server.on("/", HTTP_GET, []() {
    File file = LittleFS.open("/index.html", "r");
    if (!file) {
      server.send(500, "text/plain", "index.html missing");
      return;
    }

    String html = file.readString();
    file.close();

    html.replace("%IP_ADDRESS%", WiFi.localIP().toString());
    // We can also replace the hostname now
    html.replace("%HOSTNAME%", "http://esp32.local");

    server.send(200, "text/html", html);
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
  delay(2); // Allow CPU to switch to other tasks
}