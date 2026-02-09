import json
import random
import time
import os
from kafka import KafkaProducer

def main():
    BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    TOPIC = os.getenv("KAFKA_TOPIC", "metrics")
    INTERVAL = float(os.getenv("INTERVAL_SECONDS", "1"))

    HOSTS = [
        "ONT6_PRUEBA",
        "ONT2_PRUEBA",
        "ONT3_PRUEBA",
    ]

    while True:
            try:
                producer = KafkaProducer(
                    bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SERVERS"],
                    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                )
                print("Conectado a Kafka")
                break
            except Exception as e:
                print("❌ Kafka no disponible, reintentando...", e)
                time.sleep(5)

    print(f"Produciendo en topic '{TOPIC}' contra {BOOTSTRAP_SERVERS}")

    try:
        while True:
            payload = {
                "ts": int(time.time() * 1000),              # timestamp real
                "host": random.choice(HOSTS),
                "cpu": round(random.uniform(5, 95), 2),
                "traffic_in": random.randint(1_000, 500_000),
                "traffic_out": random.randint(1_000, 500_000)
            }

            producer.send(TOPIC, payload)
            print(payload)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("Producer detenido")

    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main()