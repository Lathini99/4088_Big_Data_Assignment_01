from kafka import KafkaProducer
from avro.io import DatumWriter, BinaryEncoder
import avro.schema
import io
import random
import time


schema = avro.schema.Parse(open("avro/order.avsc").read())

producer = KafkaProducer(bootstrap_servers="localhost:9092")


def to_avro(data):
    writer = DatumWriter(schema)
    bytes_writer = io.BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(data, encoder)
    return bytes_writer.getvalue()


def send_with_retry(topic, message, retries=3):
    for attempt in range(retries):
        try:
            producer.send(topic, to_avro(message))
            producer.flush()
            print(f"[OK] Sent: {message}")
            return True
        except Exception as e:
            print(f"[Retry {attempt+1}] Failed to send → {e}")
            time.sleep(1)

    print("[DLQ] Message failed permanently")
    return False

print("Producer started...\n")

i = 1001

PRODUCT_LIST = [
    "Samsung Galaxy A55",
    "iPhone 13 Pro",
    "Sony Bluetooth Headphones",
    "Logitech Wireless Mouse",
    "Dell 24-inch Monitor",
    "HP Laptop Charger",
    "Apple AirPods",
    "Nike Running Shoes",
    "Adidas Backpack",
    "Wooden Study Table",
    "LED Desk Lamp",
    "Electric Kettle",
    "Philips Hair Dryer",
    "JBL Portable Speaker",
    "Casio Wrist Watch",
    "Puma Sports Cap",
    "USB-C Fast Charger",
    "32GB Pendrive",
    "Office Chair",
    "Steel Water Bottle"
]

while True:
    order = {
        "orderId": str(i),
        "product": random.choice(PRODUCT_LIST),
        "price": round(random.uniform(10, 500), 2)
    }

    if not send_with_retry("orders", order):
        
        producer.send("orders-dlq", to_avro(order))

    i += 1
    time.sleep(2)
