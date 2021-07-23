from machine import Pin
import time
from network import LoRa
import socket
import ubinascii
import pycom

def setup_ttn_region(ttn_region):
    lora = LoRa(mode=LoRa.LORAWAN, region=ttn_region)
    # Remove unused channels
    # leave channels 8-15 and 65
    for index in range(0, 8):
        lora.remove_channel(index)  # remove 0-7
    for index in range(16, 65):
        lora.remove_channel(index)  # remove 16-64
    for index in range(66, 72):
        lora.remove_channel(index)   # remove 66-71
    return lora

def join_ttn(ttn_app_eui, ttn_app_key, ttn_dev_eui, lora):
    print("Joining The Things Network")
    # create OTAA authentication parameters
    app_eui = ubinascii.unhexlify(ttn_app_eui)
    app_key = ubinascii.unhexlify(ttn_app_key)
    dev_eui = ubinascii.unhexlify(ttn_dev_eui)
    # join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
    # wait until the module has joined the network
    while not lora.has_joined():
        time.sleep(2.5)
        print('Not yet joined...')
    print('Joined')
    pycom.rgbled(0x001000) #Set LED to Green
    time.sleep(5)

def check_lamp_states():
    lamp_change = False
    for i in range(0, len(lamp_list)):
        if lamp_state[lamp_list[i]] == lamp_pin_map[lamp_list[i]].value():# Port is False when lamp is on
            lamp_change = True
            time.sleep(0.10) #Debounce
            lamp_state[lamp_list[i]] = not lamp_pin_map[lamp_list[i]].value()
    return lamp_change

def send_lamp_states():
    comms_led.value(0) # Set Comms LED to On
    decimal_lamp_state = 0
    for i in range(0, len(lamp_list)):
        print(lamp_list[i], lamp_state[lamp_list[i]])
        decimal_lamp_state = decimal_lamp_state + lamp_state[lamp_list[i]] * 2 ** i
        hex_lamp_state = hex(decimal_lamp_state)[2:].upper()
        if len(hex_lamp_state) < 2:
            hex_lamp_state = "0" + hex_lamp_state
    print (hex_lamp_state)
    s.setblocking(True)
    # send data
    print('Sending ' + hex_lamp_state + ' Message to TTN')
    s.send(ubinascii.unhexlify(hex_lamp_state))
    # make the socket non-blocking
    s.setblocking(False)
    comms_led.value(1) # Set Comms LED to Off

print("Northcliff Fan Monitor V0.1")
# Set up TTN Access
ttn_app_eui = '<Your TTN App EUI>'
ttn_app_key = '<Your TTN App Key>'
ttn_dev_eui = '<Your TTN Device EUI>'

# Disable LED heartbeat (so we can control the LED)
pycom.heartbeat(False)
# Set LED to red while attempting to join LoraWAN
pycom.rgbled(0x100000)
lora = setup_ttn_region(LoRa.AU915)
join_ttn(ttn_app_eui, ttn_app_key, ttn_dev_eui, lora)
# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# Set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# Set up lamp state detectors
exhaust_fault = Pin('P13', mode=Pin.IN, pull=Pin.PULL_UP) #Set up Exhaust Fault Lamp
exhaust_run = Pin('P14', mode=Pin.IN, pull=Pin.PULL_UP) #Set up Exhaust Run Lamp
outside_fault = Pin('P15', mode=Pin.IN, pull=Pin.PULL_UP) #Set up Outside Fault Lamp
outside_run = Pin('P16', mode=Pin.IN, pull=Pin.PULL_UP) #Set up Outside Run Lamp
garage_fault = Pin('P17', mode=Pin.IN, pull=Pin.PULL_UP) #Set up Garage Fault Lamp
garage_run = Pin('P18', mode=Pin.IN, pull=Pin.PULL_UP) #Set up Garage Run Lamp
comms_led = Pin('P9', mode=Pin.OUT) # Set up Comms LED. 0=On, 1=Off
comms_led.value(1) # Set Comms LED to Off
# Set up Lamp types and start-up states
lamp_list = ["Exhaust Fault", "Exhaust Run", "Outside Fault", "Outside Run", "Garage Fault", "Garage Run"]
lamp_state = {"Exhaust Fault": False, "Exhaust Run": False, "Outside Fault": False, "Outside Run": False, "Garage Fault": False, "Garage Run": False}
lamp_pin_map = {"Exhaust Fault": exhaust_fault, "Exhaust Run": exhaust_run, "Outside Fault": outside_fault, "Outside Run": outside_run,
 "Garage Fault": garage_fault, "Garage Run": garage_run}
heartbeat_counter = 0
while True:
    lamp_changed = check_lamp_states()
    if lamp_changed or heartbeat_counter > 3600:
        heartbeat_counter = 0
        send_lamp_states() # Capture and send lamp states
    else:
        print(heartbeat_counter)
        time.sleep(1)
        heartbeat_counter += 1
