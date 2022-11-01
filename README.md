# idb

1. Install raspberrypi using imager
2. Extend wlan config

# Access Raspberry Pi

1. Find IP Address using

   dns-sd -G v4 raspberrypi.local

2. Connect with SSH

   ssh pi@[ipaddress]

   pw: pi

3. Copy files to Raspberry

   scp filename pi@raspberrypi.local:/home/repo/idb

## Humidity Alert

All code is inside code.py

### RaspberryPi Config

- Connect Temp & Humidity Sensor on Port D16
- Connect Ultrasonic Distance on Port D5
- Connect LED on Port PWM

### ThingSpeak Account

Test HTTP POST

curl -v https://api.thingspeak.com/update -d "api_key=MY_WRITE_API_KEY&field1=5&field2=10&field3=20"
