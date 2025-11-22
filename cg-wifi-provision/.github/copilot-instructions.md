# Copilot Instructions for cg-wifi-provision (ESP32 Wi-Fi Provisioning)

## Project Overview
- This project provisions Wi-Fi for ESP32 devices, providing a captive portal and web dashboard for setup and control.
- Main logic is in `main/main.cpp`, using ESP-IDF APIs, FreeRTOS, and C++.
- The device starts as a SoftAP (`HomeYantric-Setup`), runs a DNS server for captive portal, and an HTTP server for provisioning and app UI.

## Architecture & Data Flow
- **Entry Point:** `app_main()` in `main/main.cpp` initializes NVS, network interfaces, Wi-Fi, event handlers, and starts SoftAP, HTTP server, and DNS server.
- **Provisioning Flow:**
  1. Device boots in AP+STA mode, serving a captive portal (`/` and catch-all URLs).
  2. User connects to AP, accesses web UI (`HOMEYANTRIC_HTML`), submits Wi-Fi credentials via `/wifi` POST.
  3. Device attempts STA connection, updates status via `/status` endpoint (polling from frontend).
  4. On success, device switches to normal mode; on failure, stays in provisioning mode for retries.
- **Endpoints:**
  - `/scan` (GET): Scans and returns available Wi-Fi networks (JSON).
  - `/wifi` (POST): Accepts credentials, triggers STA connect.
  - `/status` (GET): Returns connection state (`connected`, `error`, `connecting`).
  - `/reset_wifi` (POST): Resets Wi-Fi config and restarts device.
  - `/close_ap` (POST): Disables AP mode, switches to STA only.
  - Captive portal detection URLs (e.g., `/hotspot-detect.html`, `/generate_204`, etc.) all serve the provisioning UI.

## Developer Workflows
- **Build:** Use ESP-IDF build system (CMake). Run:
  ```bash
  idf.py build
  ```
- **Flash:**
  ```bash
  idf.py -p <PORT> flash
  ```
- **Monitor Serial Output:**
  ```bash
  idf.py -p <PORT> monitor
  ```
- **Clean Build:**
  ```bash
  idf.py fullclean && idf.py build
  ```
- **Config:**
  ```bash
  idf.py menuconfig
  ```
- **Debugging:** Use ESP_LOG macros for logging. Key events and errors are logged with context tags (see `TAG`).

## Patterns & Conventions
- **HTTP Handlers:** All endpoints are registered in `start_webserver()`. Handlers use C++ and C APIs, return JSON or HTML as appropriate.
- **Frontend:** HTML/CSS/JS is embedded as C++ string literals. UI logic is in the HTML string, not separate files.
- **Wi-Fi State:** State is tracked with flags (`wifi_connected`, `wifi_error`, etc.) and exposed via `/status`.
- **Error Handling:** Errors are logged and surfaced to the frontend via `/status` and JSON responses.
- **mDNS:** Hostname is set dynamically based on MAC address for easy discovery (`homeyantric-XXXX.local`).
- **Captive Portal:** DNS server always resolves to AP IP; catch-all HTTP handler serves provisioning UI for unknown URLs.

## Key Files & Directories
- `main/main.cpp`: All core logic, handlers, and provisioning flow.
- `build/`, `sdkconfig`: ESP-IDF build artifacts and configuration.
- `esp-idf/`, `managed_components/`: ESP-IDF components and dependencies.

## External Dependencies
- ESP-IDF (C/C++ SDK for ESP32)
- FreeRTOS (RTOS for ESP32)
- cJSON (JSON parsing)
- mDNS (service discovery)

---

**For AI agents:**
- Focus on `main/main.cpp` for all logic and patterns.
- Use ESP-IDF build and flash commands for development.
- Follow the endpoint and handler conventions for adding new features.
- Reference the embedded HTML/JS for frontend changes.
- Log errors and state changes for debugging and frontend status updates.

---

*If any section is unclear or missing, please specify which part needs more detail or examples.*
