import tkinter as tk
import paho.mqtt.client as mqtt
import ssl

# HiveMQ Cloud Credentials
MQTT_BROKER = "1b29169c90f24560b78dea233a792d18.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  # Secure MQTT port
MQTT_USER = "nielit212"
MQTT_PASSWORD = "iloveMqtt212"
MQTT_TOPIC = "212"
CLIENT_ID = "Python_Tkinter_Client"

# MQTT Client Setup
client = mqtt.Client(CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Disable certificate verification
client.tls_insecure_set(True)  # Allow insecure TLS connection

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        status_label.config(text="✅ Connected to HiveMQ Cloud!", fg="green")
    else:
        status_label.config(text=f"❌ Connection failed (Code {rc})", fg="red")

def on_disconnect(client, userdata, rc):
    status_label.config(text="🔴 Disconnected", fg="red")

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# GUI Functions
def connect_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        status_label.config(text=f"❌ Connection Error: {e}", fg="red")

def disconnect_mqtt():
    client.disconnect()
    client.loop_stop()
    status_label.config(text="🔴 Disconnected", fg="red")

def publish_message():
    message = message_entry.get()
    if message:
        client.publish(MQTT_TOPIC, message)
        status_label.config(text=f"📤 Sent: {message}", fg="blue")
    else:
        status_label.config(text="⚠️ Enter a message", fg="orange")

# GUI Setup
root = tk.Tk()
root.title("MQTT Publisher")
root.geometry("400x300")
root.configure(bg="white")

tk.Label(root, text="MQTT Publisher", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

status_label = tk.Label(root, text="🔴 Disconnected", font=("Arial", 12), bg="white", fg="red")
status_label.pack()

message_entry = tk.Entry(root, font=("Arial", 12), width=30)
message_entry.pack(pady=10)

send_button = tk.Button(root, text="📤 Publish", font=("Arial", 12), command=publish_message, bg="blue", fg="white")
send_button.pack(pady=5)

connect_button = tk.Button(root, text="✅ Connect", font=("Arial", 12), command=connect_mqtt, bg="green", fg="white")
connect_button.pack(pady=5)

disconnect_button = tk.Button(root, text="🔴 Disconnect", font=("Arial", 12), command=disconnect_mqtt, bg="red", fg="white")
disconnect_button.pack(pady=5)

# Run GUI
root.mainloop()
