import time
from grove.gpio import GPIO
import seeed_dht as dht
import requests


def usleep(x): return time.sleep(x / 1000000.0)


url = 'https://api.thingspeak.com/update'
api_key = 'S5QBAVI8O1SZI315'


ULTRASONIC_PIN = 5
DHT_PIN = 16
led = GPIO(12, GPIO.OUT)


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


def main():

    # initialize distance and temperatur/humidity sensor
    sonar = GroveUltrasonicRanger(ULTRASONIC_PIN)
    temp_hum_sensor = dht.DHT("11", DHT_PIN)

    print('Detecting distance...')
    while True:
        # read value from distance sensor
        dist = sonar.get_distance()
        # read value form temperatur/humidity sensor
        humi, temp = temp_hum_sensor.read()
        # we are only interested in the humidity
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
        if dist < 20 and humi > 80:
            led.write(True)
        else:
            led.write(False)
        time.sleep(1)


if __name__ == '__main__':
    main()
