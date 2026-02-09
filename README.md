# Laboratorio ETL – Pinot + Kafka

Este laboratorio permite probar un flujo **end‑to‑end de ingestión y consulta de datos** utilizando Docker, Kafka y Apache Pinot.

El objetivo es:

* Generar métricas (producer)
* Ingerirlas en Pinot (realtime table)
* Consultarlas vía SQL

---

## Tecnologías
* Docker
* Docker Compose
* Python
* PowerShell (para los ejemplos de comandos)
* Kafka
* Pinot
* Superset

---

## 1) Levantar el laboratorio

### Desde el directorio raíz del proyecto:

```
docker compose up -d
```

>  Nota: si algún contenedor queda en estado `Exited`, levantarlo manualmente.

---

###  Verificar contenedores

```
docker compose ps
```

Asegurarse de que estén activos:

* Kafka
* Zookeeper / KRaft
* Pinot Controller
* Pinot Broker
* Pinot Server
* Producer

---

## 2) Configuración de Pinot

### Crear el **Schema**
---
* Ejecutar el siguiente comando desde PowerShell para definir la estructura del mensaje que Pinot espera recibir.

---
```
Invoke-WebRequest `
  -Method POST `
  -Uri http://localhost:9000/schemas `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body (Get-Content ./schema/ont_metrics_schema.json -Raw)
```


---
### Crear la **Tabla Realtime**
---

```powershell
Invoke-WebRequest `
  -Method POST `
  -Uri http://localhost:9000/tables `
  -Headers @{ "Content-Type" = "application/json" } `
  -InFile ./table/ont_metrics_realtime.json `
  -UseBasicParsing
```



## 3) Enviar datos al Producer. Ejemplo de payload que acepta el producer
```
{
  "host": "ONT3_PRUEBA",
  "cpu": 90.0,
  "traffic_in": 150.0,
  "traffic_out": 150.0
}
```

> NOTA: El producer se encarga de agregar el timestamp y enviar el mensaje a Kafka.

---

## 4) Validación: Desde la consola SQL de Pinot (UI o API), ejecutar:

```
SELECT * FROM ont_metrics;
```




