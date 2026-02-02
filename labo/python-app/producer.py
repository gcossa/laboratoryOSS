import time
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
from typing import Dict, List
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
    cpu: int
    traffic: Dict[str, float]

class Onts(BaseModel):
    List[Ont]

@app.post("/ont")
def send_metric(ont: Ont):
    producer.send(TOPIC, ont.dict())
    return {"status": "sent", "data": ont}

@app.post("/onts")
def send_metrics(onts: Onts):
    for ont in onts:
        producer.send(TOPIC, ont.dict())
    return {"status": "sent", "data": onts}