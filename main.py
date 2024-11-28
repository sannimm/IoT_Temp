import machine
import network
import time
import dht
import urequests
import json


sensor = dht.DHT22(machine.Pin(22))
switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Wi-Fi
SSID = 'xx'
PASSWORD = 'xx'

# Initialize the Wi-Fi interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to the Wi-Fi network
wlan.connect(SSID, PASSWORD)

#Wait for the connection
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("Waiting for connection...")
    time.sleep(1)

# Check the connection status
if wlan.status() != 3:
    raise RuntimeError('Connection failed')
else:
    print('Connected')
    ip = wlan.ifconfig()
    print('IP address:', ip)


def button_handler(pin):
    print("Measuring humidity..")
    get_humidity()

# Funktiot
def get_humidity():
        sensor.measure()
        humidity = sensor.humidity()
        print('Humidity: %3.1f %%' % humidity)
        return humidity
    

def get_temp():
        sensor.measure()
        temp = sensor.temperature()
        print("Temperature:", temp)
        return temp    

def get_timestamp():
    current_time = time.gmtime()
    timestamp = "{}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5]
    )
    return timestamp
switch.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

# Pääsilmukka
while True:
    try:
        temp = get_temp()
        db_timestamp = get_timestamp()
        url = 'https://temperatures.azurewebsites.net/post_temp'
        headers = {'Content-Type': 'application/json'}
        data = {
            "temp": temp,
            "timestamp": db_timestamp
        }

        response = urequests.post(url, headers=headers, data=json.dumps(data))
        response.close()
        time.sleep(5)
    except Exception as e:
        print("Error:", e)

