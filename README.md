# Laboratorio ETL – Pinot + Kafka + Superset

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

## 4) Validación. Desde la consola SQL de Pinot (UI o API), ejecutar:

```
SELECT * FROM ont_metrics;
```
## 5) Configurar Superset. Desde la UI (http://localhost:8088):

### Conectar datasource **Superset con Pinot**
 **NAME:** 
 ```
 Apache Pinot
 ```
**URI:**
```
pinot://pinot-broker:8099/query?controller=http://pinot-controller:9000
```
<img width="631" height="850" alt="image" src="https://github.com/user-attachments/assets/8ea54451-0b3e-48ee-92ab-ade9f955d55b" />

* DATASET: Source 
<img width="1093" height="845" alt="image" src="https://github.com/user-attachments/assets/4d9ff400-c8c5-4998-8243-7bb9d64f40ab" />

* DATASET: Metricas
<img width="1087" height="444" alt="image" src="https://github.com/user-attachments/assets/9816e97d-4539-4233-a210-5cc4880eb1c6" />

* DATASET: Columns
<img width="1079" height="649" alt="image" src="https://github.com/user-attachments/assets/3d4437ff-2e7b-4396-95ad-6480390ebc2c" />


### Crear chart

<img width="1892" height="802" alt="image" src="https://github.com/user-attachments/assets/3a570b85-57d5-4bcd-979b-24e604f92b42" />


