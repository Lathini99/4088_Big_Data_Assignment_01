# Kafka Real-Time Order Processing System

A complete real-time streaming pipeline using Apache Kafka and Python with Avro serialization.

##  Features

- ✅ Avro serialization for structured message format
- ✅ Producer + Consumer architecture
- ✅ Real-time running average calculation
- ✅ Retry logic with exponential backoff
- ✅ Dead Letter Queue (DLQ) for error handling
- ✅ Fault-tolerant design
- ✅ Live demonstration support

##  Project Structure

```
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
```

##  Getting Started

### Prerequisites

- Python 3.7+
- Apache Kafka installed on Windows
- Basic understanding of message queues

### Installation

Install required Python packages:

```bash
pip install kafka-python avro-python3
```

##  Kafka Setup (Windows)

### Step 1: Start ZooKeeper

Open a terminal and run:

```bash
C:\kafka\bin\windows\zookeeper-server-start.bat C:\kafka\config\zookeeper.properties
```

### Step 2: Start Kafka Broker

Open a **new terminal** and run:

```bash
C:\kafka\bin\windows\kafka-server-start.bat C:\kafka\config\server.properties
```

### Step 3: Create Topics

Create the main orders topic:

```bash
C:\kafka\bin\windows\kafka-topics.bat --create --topic orders --bootstrap-server localhost:9092
```

Create the Dead Letter Queue topic:

```bash
C:\kafka\bin\windows\kafka-topics.bat --create --topic orders-dlq --bootstrap-server localhost:9092
```

### Step 4: Verify Topics

```bash
C:\kafka\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Expected output:
```
orders
orders-dlq
```

##  Avro Schema

Create `schema/order.avsc`:

```json
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
```

## 🔧 Components

### Producer (`producer.py`)

**Features:**
- Sends random orders to Kafka
- Converts messages to Avro format
- Retries on failure (3 attempts)
- Sends failed messages to DLQ

**Run:**
```bash
python producer.py
```

### Consumer (`consumer.py`)

**Features:**
- Reads messages from `orders` topic
- Deserializes Avro messages
- Calculates running average price
- Handles corrupted messages → sends to DLQ

**Run:**
```bash
python consumer.py
```

### DLQ Consumer (`dlq_consumer.py`)

**Features:**
- Monitors failed/corrupted messages
- Helps with debugging
- Validates DLQ logic

**Run:**
```bash
python dlq_consumer.py
```

## 🎯 Running the System

Open **three terminals** and run each component:

### Terminal 1: Start Consumer
```bash
python consumer.py
```

### Terminal 2: Start DLQ Consumer
```bash
python dlq_consumer.py
```

### Terminal 3: Start Producer
```bash
python producer.py
```

## 📊 Expected Output

**Producer:**
```
[OK] Sent: {'orderId': '1001', 'product': 'Item2', 'price': 54.12}
[OK] Sent: {'orderId': '1002', 'product': 'Item5', 'price': 89.45}
```

**Consumer:**
```
Received: {'orderId': '1001', 'product': 'Item2', 'price': 54.12}
Running Average Price = 54.12

Received: {'orderId': '1002', 'product': 'Item5', 'price': 89.45}
Running Average Price = 71.79
```

**DLQ Consumer (when errors occur):**
```
DLQ Message: {'orderId': 'corrupted', 'error': 'deserialization_failed'}
```

