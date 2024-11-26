import machine
import machine
import network
import time
import dht


sensor = dht.DHT22(machine.Pin(22))
switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)


# Funktiot
def get_humidity():
    try:
        sensor.measure()
        hum = sensor.humidity()
        print('Humidity: %3.1f %%' % hum)
    except Exception as e:
        print("Error reading sensor:", e)

def get_temp():
    try:
        sensor.measure()
        temp = sensor.temperature()
        print("Temperature:", temp)
        return temp
    except Exception as e:
        print("Error measuring temperature:", e)
        return None

def button_handler(pin):
    print("Measuring humidity..")
    get_humidity()


switch.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

# Pääsilmukka
while True:
    try:
        temp = get_temp()
        time.sleep(2)
    except Exception as e:
        print("Error:", e)