project:
  title: "Kafka Real-Time Order Processing System"
  description: |
    Using Python + Apache Kafka + Avro Serialization.
    This project implements a complete real-time streaming pipeline using Apache Kafka and Python.
    It fulfills all assignment requirements:
      - Avro serialization
      - Producer + Consumer
      - Running average calculation
      - Retry logic
      - Dead Letter Queue (DLQ)
      - Live demonstration support
      - Full Kafka setup commands
      - Beginner-friendly structure

project_structure:
  root: "kafka-order-system/"
  files:
    - "README.md"
    - producer: "producer.py"
    - consumer: "consumer.py"
    - dlq_consumer: "dlq_consumer.py"
    - schema:
        - "order.avsc"

installation:
  dependencies:
    - "kafka-python"
    - "avro-python3"
  command: "pip install kafka-python avro-python3"

kafka_setup:
  zookeeper:
    description: "Start ZooKeeper"
    command: "C:\\kafka\\bin\\windows\\zookeeper-server-start.bat C:\\kafka\\config\\zookeeper.properties"
  broker:
    description: "Start Kafka Broker"
    command: "C:\\kafka\\bin\\windows\\kafka-server-start.bat C:\\kafka\\config\\server.properties"

topics:
  - name: "orders"
    description: "Main topic"
    create_command: "C:\\kafka\\bin\\windows\\kafka-topics.bat --create --topic orders --bootstrap-server localhost:9092"
  - name: "orders-dlq"
    description: "Dead Letter Queue (DLQ)"
    create_command: "C:\\kafka\\bin\\windows\\kafka-topics.bat --create --topic orders-dlq --bootstrap-server localhost:9092"
  - verify_command: "C:\\kafka\\bin\\windows\\kafka-topics.bat --list --bootstrap-server localhost:9092"
  - expected_output:
      - "orders"
      - "orders-dlq"

avro_schema:
  file: "schema/order.avsc"
  content: |
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

components:
  producer:
    file: "producer.py"
    description:
      - "Sends random orders"
      - "Converts messages into Avro format"
      - "Retries on failure"
      - "Sends failed messages to DLQ"
    run_command: "python producer.py"
  consumer:
    file: "consumer.py"
    description:
      - "Reads messages from orders topic"
      - "Deserializes Avro"
      - "Calculates running average price"
      - "Sends corrupted messages to DLQ"
    run_command: "python consumer.py"
  dlq_consumer:
    file: "dlq_consumer.py"
    description:
      - "Reads only failed/bad messages"
      - "Helps debugging and validating DLQ logic"
    run_command: "python dlq_consumer.py"

run_system:
  terminals:
    - terminal_1: "python consumer.py"
    - terminal_2: "python dlq_consumer.py"
    - terminal_3: "python producer.py"
  example_output:
    producer: "[OK] Sent: {'orderId': '1001', 'product': 'Item2', 'price': 54.12}"
    consumer:
      - "Received: {'orderId': '1001', 'product': 'Item2', 'price': 54.12}"
      - "Running Average Price = 54.12"
    dlq_consumer: "DLQ Message: { ... }"

features_implemented:
  - "Avro Serialization: Ensures structured message format"
  - "Retry Logic: Retries 3 times before moving to DLQ"
  - "Dead Letter Queue: Handles corrupted or failed messages"
  - "Real-Time Aggregation: Consumer calculates up-to-date running average"
  - "Fault Tolerance: System keeps running even with failures"
