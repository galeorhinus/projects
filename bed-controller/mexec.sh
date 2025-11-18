#rm -rf deps/ 
#mos build --local
mos build
mos flash --port /dev/tty.usbserial-1410
mos wifi RPIOT_2G rrppiioott --port /dev/tty.usbserial-1410
#mos put fs/init.js --port /dev/tty.usbserial-1410 
#mos call Sys.Reboot --port /dev/tty.usbserial-1410 
mos console --port /dev/tty.usbserial-1410
