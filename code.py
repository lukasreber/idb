import time
import sys
from grove.gpio import GPIO
from grove.grove_led import GroveLed
import grove.grove_temperature_humidity_sensor as dht
import requests


def usleep(x): return time.sleep(x / 1000000.0)


# ThingSpeak API
url = 'https://api.thingspeak.com/update'
api_key = 'S5QBAVI8O1SZI315'

# GrovePi pins
ULTRASONIC_PIN = 5
DHT_PIN = 16
LED_PIN = 12

# Thresholds
t_humidity = 60
t_distance = 20

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000


class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio = GPIO(pin)

    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)

        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance

    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist


Grove = GroveUltrasonicRanger


def initial():
    # setup led
    led = GroveLed(LED_PIN)
    # setup dht
    my_dht = dht.DHT("11", DHT_PIN)
    # initialize distance and temperatur/humidity sensor
    sonar = GroveUltrasonicRanger(ULTRASONIC_PIN)

    return my_dht, led, sonar


def main(my_dht, led, sonar):
    while True:
        # read value from distance sensor
        dist = sonar.get_distance()
        # read value form temperatur/humidity sensor
        humi, temp = my_dht.read()
        # submit data to ThingSpeak
        if not humi is None:
            h = int(round(humi))
            t = int(round(temp))
            params = {
                'api_key': api_key,
                'field1': t,
                'field2': h
            }
            try:
                r = requests.get(url, params=params)
                r.raise_for_status()
            except:
                print('API Request failed')
        else:
            h = 1000000

        print(f'distance: {dist}, humidity: {h}')
        # turn on/off led depending on values
        if dist < t_distance and humi > t_humidity:
            led.write(True)
        else:
            led.write(False)
        time.sleep(2)


if __name__ == '__main__':
    try:
        my_dht, led, sonar = initial()
        main(my_dht, led, sonar)
    except KeyboardInterrupt:
        sys.exit(0)
