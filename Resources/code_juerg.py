import time
import sys

from grove.grove_led import GroveLed
import grove.grove_temperature_humidity_sensor as dht


def setup():
    # DHT
    DHT_PIN = 16
    my_dht = dht.DHT("11", DHT_PIN)
    # LED
    LED_PIN = 5
    my_led = GroveLed(LED_PIN)

    return my_dht, my_led


def main(my_dht, my_led):
    status = False

    while True:
        # read value form temperatur/humidity sensor
        humi, temp = my_dht.read()
        # we are only interested in the humidity
        if not humi is None:
            h = int(round(humi))
            print(f'humidity: {h}')
            if h > 60:
                my_led.on()
            else:
                my_led.off()

        status = not status
        time.sleep(2)


if __name__ == '__main__':
    try:
        act_dht, act_led = setup()
        main(act_dht, act_led)
    except KeyboardInterrupt:
        sys.exit(0)