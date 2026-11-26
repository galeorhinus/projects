# Bed RF lab

These are independent ESP-IDF projects for investigating the handheld bed remote. Build from the app directory to select its own main program, components, and ESP32 configuration.

| App | Hardware and behavior |
| --- | --- |
| [sniffer](sniffer/) | Reads the receiver data line on GPIO 18, holds the transmitter line on GPIO 19 low, and prints captured pulse durations as a C array. |
| [transmitter](transmitter/) | Drives the transmitter on GPIO 19. After boot it cycles through 16 candidate commands automatically. Run on an isolated bench with the bed out of range or its actuator power disconnected. |

With ESP-IDF activated, run the following from either app directory:

```sh
idf.py build
```

To capture the handheld remote, connect the sniffer board and run `idf.py -p <port> flash monitor` from the sniffer directory.

The transmitter source labels command 4 as the head-up reference. Other button mappings and the bed's response when transmission ceases still need hardware verification. Keep the automatic scan in this lab; any future controller integration should send individual, verified commands.
