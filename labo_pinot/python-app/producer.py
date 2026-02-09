from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import time
import json
import os

app = FastAPI()
while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SERVERS"],
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("✅ Conectado a Kafka")
            break
        except Exception as e:
            print("❌ Kafka no disponible, reintentando...", e)
            time.sleep(5)

TOPIC = "metrics"

class Ont(BaseModel):
    host: str
    cpu: float
    traffic_in: float
    traffic_out: float

@app.post("/ontMetrics")
def send_metric(ont: Ont):
    data = ont.model_dump()
    data["ts"] = int(time.time() * 1000)
    producer.send(TOPIC, data)
    return {"status": "ENVIADO", "topic": TOPIC, "data": data}
