import random
from threading import Thread
from paho.mqtt import client as mqtt_client
import time
import logging
#import datetime

thread_running = True
broker = "broker.hivemq.com"
port = 1883
#topic = "ENG1419_2024-1/mqtt"
topic_publish =   "ENG1419_2024-1/mqtt/pais"
topic_subscribe = "ENG1419_2024-1/mqtt/filho"
client_id = f'publish-{random.randint(0, 1000)}'

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60



def connect_mqtt():
    #def on_connect(client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    #client = mqtt_client.Client(client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_disconnect(cliente, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            cliente.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)




def mensagem(cliente):
    subscribe(cliente)
    while True:
        time.sleep(3)
        msg = input()
        #tempo = datetime.datetime.now()
        #msg = str(tempo) + '\n' + msg
        result = cliente.publish(topic_publish, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic_publish}`")
        else:
            print(f"Failed to send message to topic {topic_publish}")
            
def enviar_mensagem(msg):
    global cliente
    result = cliente.publish(topic_publish, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_publish}`")
    else:
        print(f"Failed to send message to topic {topic_publish}")

def subscribe(cliente: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    cliente.subscribe(topic_subscribe)
    cliente.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    mensagem(client)
    client.loop_forever()
    
def cliente_background(cliente):
    subscribe(cliente)
    cliente.loop_forever()


if __name__ == '__main__':
    run()
    tempo = millis()
    while True:
        if millis() > tempo + 3000:
            tempo = millis()
            result = cliente.publish(topic_publish, "p")
            status = result[0]
            if status == 0:
                print(f"Send \"p\" to topic `{topic_publish}`")
            else:
                print(f"Failed to send message to topic {topic_publish}")
else:
    cliente = connect_mqtt()
    threadBG = Thread(target = cliente_background, args=(cliente,))