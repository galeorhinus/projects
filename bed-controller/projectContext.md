### Project Briefing: Wi-Fi Adjustable Bed Controller

**Project Goal:** To create a Wi-Fi-enabled controller for an adjustable bed using an ESP32 running Mongoose OS. The primary control interface is a mobile-first web app served directly from the ESP32.

**Core Architecture:**
* **Platform:** ESP32 (Mongoose OS)
* **Backend:** `fs/init.js` (mJS/JavaScript). Manages all GPIO logic and state.
* **Frontend:** A single-page application split into `fs/index.html`, `fs/style.css`, and `fs/app.js`.
* **API:** Mongoose OS RPC (not a custom `Net.serve` or `Net.listen`). The `http-server` library automatically exposes RPC handlers at `/rpc/Handler.Name`.
* **Server Port:** Configured to `8080` in `mos.yml`.

**Key Hardware Feature (Dual-Control):**
The system is designed to run in parallel with the original wired remote.
* **Relays 1-4:** Motor control (Head Up/Down, Foot Up/Down).
* **Relays 5-8:** These are wired as a 4-pole transfer switch, controlled by 4 separate GPIO pins (`TRANSFER_PIN_1` to `_4`).
* **Default State:** On boot, the transfer switch is OFF (`RELAY_OFF`), giving control to the wired remote.
* **ESP32 Control:** Before any motor command (e.g., `HEAD_UP` or `ZERO_G`), the backend *must* call `activateTransferSwitch()` to set all 4 transfer relays to `RELAY_ON`.
* **Release Control:** In the `stopMovement()` function, the backend *must* call `deactivateTransferSwitch()` to set all 4 transfer relays to `RELAY_OFF`, returning control to the wired remote.

**Key Files & Purpose:**

1.  **`mos.yml` (Config File):**
    * Manages all libraries (e.g., `http-server`, `rpc-common`, `rpc-service-config`).
    * Sets `http.port: 8080`.
    * Defines the config schema (`config_schema:`) for saving positions.
    * **Stores all 5 preset positions AND labels with their factory defaults** (e.g., `state.zg_head: 10000`, `state.zg_label: "Zero G"`).

2.  **`fs/init.js` (Backend Server Logic):**
    * Defines all 10 GPIO pins (4 motor, 1 light, 4 transfer, 1 unused).
    * Defines `RELAY_ON = 0` and `RELAY_OFF = 1` (active-low).
    * Contains the core motor logic (`executePositionPreset`, `stopMovement`, `updatePosition`).
    * Contains the `calculateLivePositions()` helper to get real-time, in-motion positions.
    * **Registers two main RPC handlers:**
        * `RPC.addHandler('Bed.Command', ...)`: Handles all actions (buttons, presets, saving presets).
        * `RPC.addHandler('Bed.Status', ...)`: A read-only handler for polling.
    * Includes `SET_P1`, `SET_P2`, `SET_ZG`, etc. logic to overwrite presets.
    * Includes a `RESET_PRESETS` command to restore `mos.yml` defaults.

3.  **`fs/index.html` (Frontend HTML):**
    * Contains the HTML "skeleton" for the page.
    * Links to `style.css` and `app.js`.
    * Defines the SVG container (`<div class="svg-container">`) which holds the bed visualizer.
    * Defines the "rocker buttons" (`<div class="rocker-btn">`).
    * Defines all 5 preset buttons with dynamic IDs (e.g., `id="zg-label-text"`).
    * Defines the "Set..." button and the hidden modal (`<div id="set-modal">`).
    * The modal includes 5 "Save to..." buttons and the "Reset All Presets" button.

4.  **`fs/style.css` (Frontend Styles):**
    * Contains all styling for the page, buttons, and visualizer.
    * `.visualizer-line` defines the mattress style (olive green, 36px thick, rounded).
    * `#bed-base-line` and `.bed-leg-line` define the frame style (gray, 12px thick).
    * Defines the modal styles (`.modal-backdrop`, etc.) and the "Set" button (`.util-btn`).

5.  **`fs/app.js` (Frontend JavaScript):**
    * `pollStatus()`: Runs every 1 second, calls `Bed.Status` RPC.
    * `updateStatusDisplay(data)`: The main rendering function.
        * Updates the "Up since" and "Duration" text.
        * Updates the floating "0s" text on the visualizer and hides it at 0.
        * Calculates all SVG `points` for the mattress line (`#mattress-line`) to animate the bed shape.
    * `isFirstPoll`: A boolean flag. On the first poll, it calls `updatePresetButton()` for all 5 presets to draw their initial labels and icons.
    * `sendCmd(cmd, btn, label)`: Sends all commands to the `Bed.Command` RPC.
        * Handles preset button pulsing.
        * If the server response includes a `saved` or `reset` flag, it calls `updatePresetButton()` to *instantly* update the UI.
    * `stopCmd(isManual)`: Sends the `STOP` command.
    * `updatePresetButton(slot, ...)`: Updates a specific preset button's label and icon shape.
    * `calculateIconPoints(...)`: Helper function to draw the mini SVG icons.
    * `openSetModal()`: Reads the *current* labels from the 5 preset buttons to dynamically create the "Save to..." button text in the modal.
    * `savePreset(slot)`: Reads the text input and calls `sendCmd` (e.g., `sendCmd('SET_P1', null, 'My Label')`).
    * `resetPresets()`: Asks for confirmation, then calls `sendCmd('RESET_PRESETS')`.

6.  **`fs/utils.js` (Utility):**
    * Contains `numToStrJS()`. This is **critical** because mJS crashes on `print("string" + number)` (implicit type conversion error). All `print` statements in `init.js` that mix strings and numbers *must* use this.