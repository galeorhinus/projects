# Elev8 Bed Controller: Hardware & Wiring Specification

**Version:** 3.0 (ESP32-S3 Variant)  
**Status:** Production / "Bulletproof" Revision

## 1. System Overview

The Elev8 controller intercepts the signals between a standard adjustable bed motor and its wired remote. It allows for dual-control: standard manual operation via the original remote, or automated control via the ESP32-S3.

**Key Features:**

* **Safety First:** Input includes thermal breaker and reverse-polarity protection.
* **Isolation:** Uses a "Transfer Relay" topology to physically disconnect the manual remote during automation to prevent short circuits.
* **Limit Detection:** Uses current sensing (ACS712) to detect motor stalls/limits.
* **Remote Sensing:** Optocouplers detect manual button presses for state tracking.

## 2. Component List

* **MCU:** Espressif ESP32-S3 DevKitC-1
* **Power Regulator:** Mean Well N7805-1C-ND (29V to 5V DC-DC)
* **Relays:** 2x 4-Channel Relay Modules (5V Active Low)
  * *Board A:* Power Generation (H-Bridge)
  * *Board B:* Signal Transfer (Source Selector)
* **Sensors:**
  * ACS712 (Hall Effect Current Sensor)
  * 4x Optocouplers (EL817 or similar)
* **Protection:**
  * Thermal Circuit Breaker (5A, Push-to-Reset)
  * Blocking Diode (1N5408 or equivalent)

## 3. Wire Color Code Standard

| Function | Color | Notes |
| --- | --- | --- |
| **29V DC+** | **Green** | Main high-voltage motor power |
| **5V DC+** | **Brown** | Logic power (Post-regulator) |
| **Ground** | **White** | Common Ground (Shared 29V/5V/3.3V) |
| **Head Up** | **Yellow** | Signal & Actuation |
| **Head Down** | **Black** | Signal & Actuation |
| **Foot Up** | **Red** | Signal & Actuation |
| **Foot Down** | **Blue** | Signal & Actuation |

## 4. GPIO Pin Mapping

*Target Board: ESP32-S3 DevKitC-1*

| Logical Label | Function | Wire Color | **GPIO Pin** |
| --- | --- | --- | --- |
| **Current Sensor** |  |  |  |
| `PIN_ADC_CURRENT` | ACS712 Data (Analog) | Signal | **2** |
| **Motor Power (Relay Bd 1)** |  |  |  |
| `PIN_HEAD_PWR_A` | Head Up Power | Yellow | **4** |
| `PIN_HEAD_PWR_B` | Head Down Power | Black | **5** |
| `PIN_FOOT_PWR_A` | Foot Up Power | Red | **6** |
| `PIN_FOOT_PWR_B` | Foot Down Power | Blue | **7** |
| **Transfer Logic (Relay Bd 2)** |  |  |  |
| `PIN_HEAD_TRNS_A` | Head Transfer (Isolate) | - | **9** |
| `PIN_HEAD_TRNS_B` | Head Transfer (Isolate) | - | **10** |
| `PIN_FOOT_TRNS_A` | Foot Transfer (Isolate) | - | **11** |
| `PIN_FOOT_TRNS_B` | Foot Transfer (Isolate) | - | **12** |
| **Remote Input (Optos)** |  |  |  |
| `PIN_OPTO_H_UP` | Sense Head Up Btn | Yellow | **35** |
| `PIN_OPTO_H_DN` | Sense Head Dn Btn | Black | **36** |
| `PIN_OPTO_F_UP` | Sense Foot Up Btn | Red | **37** |
| `PIN_OPTO_F_DN` | Sense Foot Dn Btn | Blue | **38** |
| **Peripherals** |  |  |  |
| `PIN_LED_DATA` | Status LED (RGB) | Data | **8** |
| `PIN_BTN_BOOT` | Commission Button | - | **0** |

## 5. Detailed Wiring Specification

### A. Power Entry & Safety Stage

*Critical: Prevents reverse polarity damage and fire hazards.*

1. **Input Source (Wall):** 29V DC Power Supply.
2. **Protection Chain:**
   * **29V+ (Source)**  **Thermal Breaker (5A)**  **Blocking Diode (Anode)**.
   * **Blocking Diode (Cathode)**  **System 29V Line (Green Wire)**.
   * **Ground (Source)**  **System Ground (White Wire)**.

### B. Logic Power (5V & 3.3V)

*Regulates the safe 29V line down for the MCU and Relays.*

1. **N7805 Regulator:**
   * *Input:* System 29V Line (Green).
   * *Ground:* System Ground (White).
   * *Output:* **5V Line (Brown Wire)**.

2. **Distribution (Brown Wire):**
   * Connects to Relay Board 1 (VCC).
   * Connects to Relay Board 2 (VCC).
   * Connects to ACS712 (VCC).
   * Connects to ESP32 DevKit (5V Pin).

### C. Relay Wiring (The "Intercept" Topology)

*The system uses two 4-channel relay boards.*

#### Board 1: Power Generation (H-Bridge)

*Function: Generates the 29V polarity to move motors.*

* **Inputs:** 29V (Green) and Ground (White).
* **Outputs:** Sends power to the **NO** (Normally Open) terminals of Board 2.

| Relay Ch | Input (ESP32) | NO Terminal | NC Terminal | COM Output (To Bd 2) |
| --- | --- | --- | --- | --- |
| **1** | GPIO 4 | 29V (Green) | GND (White) | To Bd 2 (Relay 1 NO) |
| **2** | GPIO 5 | 29V (Green) | GND (White) | To Bd 2 (Relay 2 NO) |
| **3** | GPIO 6 | 29V (Green) | GND (White) | To Bd 2 (Relay 3 NO) |
| **4** | GPIO 7 | 29V (Green) | GND (White) | To Bd 2 (Relay 4 NO) |

#### Board 2: Transfer (Source Selector)

*Function: Selects between the Original Remote (Default) and Board 1 (Automation).*

* **Inputs:** Original Remote Wires.
* **Outputs:** Actual Bed Motors.

| Relay Ch | Input (ESP32) | NC Terminal (Default) | NO Terminal (Active) | COM Output (To Motor) |
| --- | --- | --- | --- | --- |
| **1** | GPIO 9 | Remote Head (+) | From Bd 1 (Relay 1 COM) | **Head Motor (+)** |
| **2** | GPIO 10 | Remote Head (-) | From Bd 1 (Relay 2 COM) | **Head Motor (-)** |
| **3** | GPIO 11 | Remote Foot (+) | From Bd 1 (Relay 3 COM) | **Foot Motor (+)** |
| **4** | GPIO 12 | Remote Foot (-) | From Bd 1 (Relay 4 COM) | **Foot Motor (-)** |

### D. Sensor Wiring

#### 1. Current Sensing (Limit Detection)

The ACS712 intercepts the main 29V feed *before* it reaches the Relay Boards.

* **Power Path:** System 29V (Green)  ACS712 IP+  ACS712 IP-  Relay Board 1 COM.
* **Data Path (Voltage Divider):**
  * ACS712 Out  47kΩ  **GPIO 2**.
  * GPIO 2  68kΩ  GND.

#### 2. Manual Remote Sensing (Optocouplers)

Detects when a button is pressed on the physical remote.

* **High Voltage Side (29V):**
  * Remote Wire (Yellow/Black/Red/Blue)  4.7kΩ  Opto Anode (+).
  * Opto Cathode (-)  System Ground (White).

* **Low Voltage Side (3.3V):**
  * Opto Collector  GPIO (35/36/37/38).
  * Opto Emitter  Ground.
  * *Note: GPIOs configured as `INPUT_PULLUP`.*
