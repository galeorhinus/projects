pio run # only build
pio run --target upload
pio run --target uploadfs
pio device monitor
#pio run -t upload && pio device monitor

#pio run -t upload -t uploadfs && pio device monitor
#pio run --target erase #erase Flash (Factory Reset): If you need to wipe WiFi credentials and NVS completely (equivalent to the "Erase" button).
#pio run --target clean #Clean Build: If compilation is acting weird and you want to delete all cached objects.
pio run -t erase -t clean && pio run --target uploadfs && pio run --target upload