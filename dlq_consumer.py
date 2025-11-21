from kafka import KafkaConsumer
from avro.io import DatumReader, BinaryDecoder
import avro.schema
import io

schema = avro.schema.Parse(open("avro/order.avsc").read())

consumer = KafkaConsumer(
    "orders-dlq",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest"
)

def from_avro(binary_message):
    bytes_reader = io.BytesIO(binary_message)
    decoder = BinaryDecoder(bytes_reader)
    reader = DatumReader(schema)
    return reader.read(decoder)

print("DLQ Consumer started...\n")

for msg in consumer:
    try:
        order = from_avro(msg.value)
        print("DLQ Message:", order)
    except:
        print("Bad DLQ message encountered.")
