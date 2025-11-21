from kafka import KafkaConsumer, KafkaProducer
from avro.io import DatumReader, BinaryDecoder
import avro.schema
import io

schema = avro.schema.Parse(open("avro/order.avsc").read())

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

dlq_producer = KafkaProducer(bootstrap_servers="localhost:9092")

total_price = 0.0
count = 0

def from_avro(binary_message):
    bytes_reader = io.BytesIO(binary_message)
    decoder = BinaryDecoder(bytes_reader)
    reader = DatumReader(schema)
    return reader.read(decoder)

print("Consumer started...\n")

for msg in consumer:
    try:
        order = from_avro(msg.value)
        print("Received:", order)

        
        total_price += order["price"]
        count += 1
        avg = total_price / count
        print(f"Running Average Price = {avg:.2f}\n")

    except Exception as e:
        print("FAILED on consumer → sending to DLQ:", e)
        dlq_producer.send("orders-dlq", msg.value)
