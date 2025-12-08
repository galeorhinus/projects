# Enabling Matter in this project

Follow these steps when you want Matter builds again. These assume network access to download managed components.

1) **Add the esp-matter dependency**  
   In `main/idf_component.yml` restore the entry (no `path:` override unless you keep a local copy):  
   ```yaml
   dependencies:
     idf: ">=5.1.0"
     esp-matter: "~1.4.2"
     espressif/mdns: "^1.2.5"
   ```
   If you prefer a local repo, clone/restore `components/esp-matter` and set `path: ../components/esp-matter` instead.

2) **Allow the component in CMake**  
   Remove the `idf_build_set_property(EXCLUDE_COMPONENTS "esp-matter" APPEND)` line from the top-level `CMakeLists.txt`.

3) **Enable Matter in Kconfig**  
   Set `CONFIG_APP_ENABLE_MATTER=y` (via `idf.py menuconfig` or add to `sdkconfig.defaults`). Ensure Bluetooth/NimBLE are enabled if your board needs BLE commissioning.

4) **Clean and reconfigure**  
   ```sh
   rm -rf build sdkconfig dependencies.lock managed_components/.idf_component_manager
   source $IDF_PATH/export.sh
   idf.py reconfigure
   ```
   This will download esp-matter into `managed_components/` (or use your local path).

5) **Build/flash**  
   ```sh
   idf.py build flash monitor
   ```

Notes:
- Matter commissioning uses its own mDNS; when Matter is off the app falls back to esp_mdns for `homeyantric-XX.local`.
- Flash size: dual-OTA images generally need 8 MB; on 4 MB devices expect single-OTA.
