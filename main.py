import network
import machine
import time
import dht
import urequests
import json

sensor = dht.DHT22(machine.Pin(22))
switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
red_led = machine.Pin(16, machine.Pin.OUT)  # Punainen LED
red_led.value(False)

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


def get_limit():
    try:
        url = 'https://temperatures.azurewebsites.net/get_limit'  # Limit endpoint
        response = urequests.get(url)
        print("Server response:", response.text)  # Debug-tuloste
        data = json.loads(response.text)  # Varmista, että tämä palauttaa odotettua JSON:ia
        response.close()
        limit = data.get('limit', None)
        if limit is not None:
            print("Current limit:", limit)
            return float(limit)
        else:
            print("Limit not found in response.")
            return None
    except Exception as e:
        print("Error fetching limit:", e)
        return None


def get_timestamp():
    current_time = time.gmtime()
    timestamp = "{}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5]
    )
    return timestamp

switch.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

# Pääsilmukka
while True:
        temp = get_temp()
        limit = get_limit()
        timestamp = get_timestamp
        if limit is not None and temp >= limit:
            red_led.value(True)  # Sytytä LED
        else:
            red_led.value(False)  # Sammuta LED

        # Lähetä lämpötila palvelimelle
        
        url = 'https://temperatures.azurewebsites.net/post_temp'
        headers = {'Content-Type': 'application/json'}
        data = {
            "temp": temp,
            "timestamp": get_timestamp()  # Käytä määriteltyä timestampia
        }
        print("Sending data:", data)  # Debug-tuloste
        try:
            response = urequests.post(url, headers=headers, data=json.dumps(data))
            print("Response status:", response.status_code)
            print("Response text:", response.text)  # Tulosta palvelimen vastaus
            response.close()
        except Exception as e:
            print("Error sending data:", e)