# Wi-Fi Adjustable Bed Controller

[![Mongoose OS](https://img.shields.io/badge/Mongoose%20OS-powered-blue.svg)](https://mongoose-os.com/)

This project converts a standard adjustable bed (which uses a wired remote) into a "smart" bed, controllable via Wi-Fi from any device with a web browser. It runs on an ESP32 using Mongoose OS and serves a modern, responsive web UI that works perfectly on a phone.

This project is designed for a specific hardware setup that allows the original wired remote and the new Wi-Fi controller to be used simultaneously, with relays acting as a transfer switch to prevent conflicts.

![Bed Controller UI Demo](https://placehold.co/600x400/1f2937/9ca3af?text=Demo+GIF+of+the+app+in+action)
*(You should replace the image above with a `docs/demo.gif` of your app working!)*

## Features

* **Web Interface:** Fully responsive, mobile-first UI to control the bed.
* **Dual-Control Safe:** Uses a transfer switch (4 relays) to safely switch control between the original wired remote and the ESP32. This prevents short circuits.
* **Real-time Visualizer:** A dynamic SVG bed graphic shows the head and foot positions in real-time.
* **Position Tracking:** Uses motor run-time to calculate and save the bed's position, even after a reboot.
* **Standard Presets:** Includes one-touch buttons for "Flat," "Zero G," "Anti-Snore," and "Legs Up."
* **Custom Presets (P1 & P2):**
    * Save two custom head/foot positions with your own labels (e.g., "Reading", "TV").
    * Buttons feature dynamic SVG icons that show the saved position's shape.
* **Under-Bed Light:** A toggle button for a separate light relay.
* **Safe by Default:** The system boots with the wired remote active. The ESP32 only takes control of the motors when a command is sent.

## Hardware Requirements

* **ESP32 Module:** An ESP32-WROVER was used for this project.
* **Relay Modules:**
    * **1x 8-Channel Relay Module (5V):** Relays 1-4 are for motor control (Head Up/Down, Foot Up/Down). Relays 5-8 are for the transfer switch.
    * **1x 1-Channel Relay Module (5V):** For the under-bed light.
* **Power Supply:** A 5V power supply to run the ESP32 and the relays. (The ESP32's 3.3V pin may not provide enough current for the transfer relays).
* **Hookup Wires:** For connecting the ESP32 GPIOs to the relay IN pins.
* **Soldering Iron & Wires:** For intercepting the motor control lines from the wired remote.

## How it Works: Architecture

1.  **Backend (`fs/init.js`):** A Mongoose OS JavaScript file runs on the ESP32. It handles all logic.
2.  **Web Server (`http-server`):** The ESP32 hosts a web server (on port 8080 by default) that serves the `fs/index.html`, `fs/style.css`, and `fs/app.js` files.
3.  **Frontend (`fs/app.js`):** All user interaction in the browser is handled by vanilla JavaScript.
4.  **API (RPC):** The frontend sends commands (e.g., "HEAD_UP") to the backend by calling RPC (Remote Procedure Call) endpoints (e.g., `/rpc/Bed.Command`).
5.  **Polling (RPC):** The frontend polls the `/rpc/Bed.Status` endpoint every 1 second to get the bed's current position, uptime, and saved preset data, which it uses to update the SVG visualizer.
6.  **GPIO Control:** The backend logic in `fs/init.js` translates RPC commands into GPIO signals to control the relays.
7.  **Transfer Switch:** Before moving a motor, `fs/init.js` first activates the four transfer relays. After the motor stops (either by a "STOP" command or a preset timer finishing), it deactivates them, returning control to the wired remote.

## Software & Installation

This project is built for [Mongoose OS](https://mongoose-os.com/). You must have the `mos` tool installed and working.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  **Clean & Build:**
    (This step is important to clear any local caches).
    ```bash
    rm -rf build deps
    mos build --clean
    ```

3.  **Flash the Device:**
    (Hold the "Boot" button on your ESP32 if it doesn't connect automatically).
    ```bash
    mos flash --port YOUR_PORT_HERE
    ```
    *(e.g., `mos flash --port /dev/tty.usbserial-1440`)*

4.  **Configure Wi-Fi:**
    ```bash
    mos wifi YOUR_SSID YOUR_PASSWORD --port YOUR_PORT_HERE
    ```

5.  **Find Device IP:**
    After flashing, the device will connect to your Wi-Fi. Find its IP address from your router's DHCP list or by listening to the `mos console`.

6.  **Use the App:**
    Open `http://<YOUR_DEVICE_IP>:8080` in any web browser.

## Pin Configuration (Crucial!)

All hardware pin settings are at the top of `fs/init.js`. You **must** edit these to match your wiring.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `RELAY_ON` | `0` | `0` for active-LOW relays, `1` for active-HIGH. **Change this first!** |
| `RELAY_OFF` | `1` | `1` for active-LOW relays, `0` for active-HIGH. **Change this first!** |
| `HEAD_UP_PIN` | `22` | GPIO pin for the "Head Up" motor relay. |
| `HEAD_DOWN_PIN` | `23` | GPIO pin for the "Head Down" motor relay. |
| `FOOT_UP_PIN` | `18` | GPIO pin for the "Foot Up" motor relay. |
| `FOOT_DOWN_PIN` | `19` | GPIO pin for the "Foot Down" motor relay. |
| `LIGHT_PIN` | `27` | GPIO pin for the under-bed light relay. |
| `TRANSFER_PIN_1` | `32` | GPIO pin for the first transfer relay. |
| `TRANSFER_PIN_2` | `33` | GPIO pin for the second transfer relay. |
| `TRANSFER_PIN_3` | `25` | GPIO pin for the third transfer relay. |
| `TRANSFER_PIN_4` | `26` | GPIO pin for the fourth transfer relay. |

### Motor Calibration

You must also time your bed's motors to get accurate positions.

1.  Use a stopwatch. Run the "Head Up" command until the bed stops at its maximum height.
2.  Update `HEAD_MAX_SECONDS` in `fs/init.js` with this value (in seconds).
3.  Do the same for the foot and update `FOOT_MAX_SECONDS`.
4.  Re-flash the `init.js` file (`mos put fs/init.js --port ...`).

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.