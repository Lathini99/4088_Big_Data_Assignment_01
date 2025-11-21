Kafka Real-Time Order Processing System
Using Python + Apache Kafka + Avro Serialization

This project implements a complete real-time streaming pipeline using Apache Kafka and Python.
It fulfills all assignment requirements:

✔ Avro serialization
✔ Producer + Consumer
✔ Running average calculation
✔ Retry logic
✔ Dead Letter Queue (DLQ)
✔ Live demonstration support
✔ Full Kafka setup commands
✔ Beginner-friendly structure

Project Structure
kafka-order-system/
│
├── schema/
│   └── order.avsc
│
├── producer.py
├── consumer.py
├── dlq_consumer.py
│
└── README.md

1. How to Install Requirements
Install Kafka-Python and Avro

pip install kafka-python avro-python3

2. Kafka Setup (Windows)
Start ZooKeeper
C:\kafka\bin\windows\zookeeper-server-start.bat C:\kafka\config\zookeeper.properties

Start Kafka Broker

Open a new terminal:

C:\kafka\bin\windows\kafka-server-start.bat C:\kafka\config\server.properties

3. Create Topics


Main Topic
C:\kafka\bin\windows\kafka-topics.bat --create --topic orders --bootstrap-server localhost:9092

Dead Letter Queue (DLQ)
C:\kafka\bin\windows\kafka-topics.bat --create --topic orders-dlq --bootstrap-server localhost:9092

Verify Topics
C:\kafka\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092


Expected output:

orders
orders-dlq

4. Avro Schema (order.avsc)

Inside schema/order.avsc:

{
  "type": "record",
  "name": "OrderRecord",
  "namespace": "order",
  "fields": [
    { "name": "orderId", "type": "string" },
    { "name": "product", "type": "string" },
    { "name": "price", "type": "float" }
  ]
}

5. Producer — producer.py

✔ Sends random orders
✔ Converts messages into Avro format
✔ Retries on failure
✔ Sends failed messages to DLQ

Run with:

python producer.py

6. Consumer — consumer.py

✔ Reads messages from orders topic
✔ Deserializes Avro
✔ Calculates running average price
✔ Sends corrupted messages to DLQ

Run with:

python consumer.py

7. DLQ Consumer — dlq_consumer.py

✔ Reads only failed/bad messages
✔ Helps debugging and validating DLQ logic

Run with:

python dlq_consumer.py

8. How to Run the Entire System

Open three terminals in VS Code or CMD:

Terminal 1 — Consumer
python consumer.py

Terminal 2 — DLQ Consumer
python dlq_consumer.py

Terminal 3 — Producer
python producer.py


You will see:

Producer:
[OK] Sent: {'orderId': '1001', 'product': 'Item2', 'price': 54.12}

Consumer:
Received: {'orderId': '1001', 'product': 'Item2', 'price': 54.12}
Running Average Price = 54.12

DLQ Consumer (only when errors occur):
DLQ Message: { ... }

9. Features Implemented
✔ Avro Serialization

Ensures structured message format.

✔ Retry Logic

Retries 3 times before moving to DLQ.

✔ Dead Letter Queue

Handles corrupted or failed messages.

✔ Real-Time Aggregation

Consumer calculates up-to-date running average.

✔ Fault Tolerance

System keeps running even with failures.