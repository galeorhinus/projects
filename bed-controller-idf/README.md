# Elev8 Bed Controller (Firmware v1.5 - Native IDF)

**Professional-grade firmware for the HomeYantric Elev8 adjustable bed system.**

This project replaces the standard Arduino framework with the **Native ESP-IDF (Espressif IoT Development Framework)** running on FreeRTOS. It provides robust motor control, thread-safe networking, and a responsive web interface without the overhead of the Arduino abstraction layer.

---

## 🏗 Architecture

The system is modularized into three core components running on the ESP32 dual-core architecture:

### 1. `main.cpp` (The Entry Point)
* **Role:** System Orchestrator.
* **Logic:** Initializes hardware and networking, then spawns the physics engine as a pinned FreeRTOS task.
* **Context:** `app_main` (Core 0).

### 2. `BedControl` (The Physics Engine)
* **Role:** Hardware abstraction and State Machine.
* **Logic:** Handles GPIO switching, PWM LED fading, Safety Mutexes, and NVS (Non-Volatile Storage) for saving presets.
* **Context:** Dedicated FreeRTOS Task pinned to **Core 1** (10ms tick).

### 3. `NetworkManager` (The Connectivity)
* **Role:** WiFi, mDNS, and Web Server.
* **Logic:** Manages the `esp_http_server`, handles JSON API requests (`cJSON`), and serves the Single Page Application (SPA) from SPIFFS.
* **Context:** Event Loop (Core 0).

---

## 🔌 Hardware Wiring

**Controller:** ESP32-WROVER (or standard ESP32 DevKit V1)

### Motor Relays (Active Low)
| Function | GPIO Pin | Description |
| :--- | :--- | :--- |
| **Head UP** | GPIO 22 | Relay 1 |
| **Head DOWN** | GPIO 23 | Relay 2 |
| **Foot UP** | GPIO 18 | Relay 3 |
| **Foot DOWN** | GPIO 19 | Relay 4 |

### Transfer Switch (Remote Isolation)
| Function | GPIO Pin | Description |
| :--- | :--- | :--- |
| **Transfer 1-4** | 32, 33, 25, 26 | Isolates wired remote during operation |

### Status LED (Common Anode)
| Color | GPIO Pin | Resistor | Status |
| :--- | :--- | :--- | :--- |
| **Red** | GPIO 13 | 220Ω | Head Down / Error |
| **Green** | GPIO 27 | 220Ω | Head Up |
| **Blue** | GPIO 14 | 220Ω | Presets / Auto |

*> **Note:** GPIO 12 is NOT used to avoid boot strapping issues.*

---

## ⚙️ Configuration

All settings are centralized in `main/Config.h`.

**WiFi Credentials:**
```cpp
#define WIFI_SSID  "galeasus24"
#define WIFI_PASS  "galeasus2.4"
