import json
import time
import paho.mqtt.client as mqttclient
import geocoder
import random
import serial.tools.list_ports

mess = ''
bbc_port = 'COM4'
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)
    
temp = 30
humi = 50
light_intesity = 100
counter = 0
    
def processData(data):
    data = data.replace('!', '')
    data = data.replace('#', '')
    splitData = data.split(':')
    print(splitData)
    collect_data = {}
    # TODO: Add your source code to publish data to the server
    tmp = splitData[2]
    global temp, light
    if splitData[1] == 'TEMP':
        collect_data['temperature'] = tmp
    if splitData[1] == 'LIGHT':
        collect_data['light'] = tmp
        
    # collect_data = {'temperature': temp,
    #                 'light': light }
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)

    
    
def readSerial():
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        global mess
        mess = mess + ser.read(bytesToRead).decode('utf-8')
        while ('#' in mess) and ('!' in mess):
            start = mess.find('!')
            end = mess.find('#')
            processData(mess[start:end + 1])
            mess = mess[end+1:]
        

print("Xin chào ThingsBoard")

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "aUvhtB7AvpawBJb59Gkp"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    cmd = 0
    # TODO: Update the cmd to control 2 devices
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setLED":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/BUTTON_LED', json.dumps(temp_data), 1)
            cmd = cmd + int(temp_data['value'])
            
        if jsonobj['method'] == "setPUMP":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/BUTTON_PUMP', json.dumps(temp_data), 1)
            cmd = cmd + 2 + int(temp_data['value'])
    except:
        pass
    
    if len(bbc_port) > 0:
        ser.write((str(cmd) + "#").encode())


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

# longitude = 106.7
# latitude = 10.6
geo = geocoder.ip('me')
latitude, longitude = geo.latlng
# print(latitude, longitude)

while True:
    # collect_data = {'temperature': temp, 'humidity': humi,
    #                 'light': light_intesity, 'longitude': longitude, 'latitude': latitude}
    # temp = random.randint(20, 92)
    # humi = random.randint(0, 100)
    # light_intesity += 1
    # client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    # time.sleep(5)
    if len(bbc_port) > 0:
        readSerial()
        
    time.sleep(1)
