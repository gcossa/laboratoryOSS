import os
import json
import time
from kafka import KafkaConsumer
from influxdb import InfluxDBClient

def main():
    KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    INFLUX_HOST = os.getenv("INFLUXDB_HOST", "influxdb")
    INFLUX_PORT = int(os.getenv("INFLUXDB_PORT", 8086))
    INFLUX_DB = os.getenv("INFLUXDB_DB", "metrics")

    print("Esperando Kafka...")

    while True:
        try:
            consumer = KafkaConsumer(
                "metrics",
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="metrics-consumer",
                enable_auto_commit=True
            )
            print("✅ Conectado a Kafka")
            break
        except Exception as e:
            print("❌ Kafka no disponible, reintentando...", e)
            time.sleep(5)

    print("Conectando a InfluxDB...")

    influx = InfluxDBClient(
        host=INFLUX_HOST,
        port=INFLUX_PORT,
        database=INFLUX_DB
    )

    print("✅ Consumer listo. Esperando mensajes...")

    for msg in consumer:
        data = msg.value
        print("RECIBIDO:", data)

        point = [{
            "measurement": "cpu_usage",
            "tags": {
                "host": data["host"]
            },
            "fields": {
                "cpu": float(data["cpu"]),
                "traffic_in": float(data["traffic"].get("traffic_in", 0)),
                "traffic_out": float(data["traffic"].get("traffic_out", 0))
            }
        }]

        influx.write_points(point)
        print("ESCRITO EN INFLUXDB:", point)
    return 1
if __name__ == "__main__":
    main()
