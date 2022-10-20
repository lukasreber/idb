import time
import math
import grove.grove_temperature_humidity_sensor as dht

DHT_PIN = 16  # rasperry pi Pin16, Grove D16


def main():

    sensor = dht.DHT("11", DHT_PIN)

    while True:
        humi, temp = sensor.read()
        if not humi is None:
            h = int(round(humi))
            t = int(round(temp))
            print(f'DHT{sensor.dht_type}, humidity: {h}, temperatur: {t}')
        else:
            print('DHT{0}, humidity & temperature: {1}'.format(
                sensor.dht_type, temp))

        time.sleep(1)


if __name__ == '__main__':
    main()
