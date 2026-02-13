# Introducción

El objetivo de este trabajo es diseñar e implementar un clúster virtualizado que permita simular una infraestructura orientada al análisis de grandes volúmenes de datos del mercado financiero. Para ello, se utilizó Docker como tecnología de virtualización liviana, desplegando un clúster compuesto por nodos que integran Spark, Kafka y Zookeeper.

# Versiones

- Docker desktop 4.58.0
- Zookeeper: 7.0.1
- Docker: 29.1.3
- Docker-compose: 5.0.1
- Kafka: 7.0.1
- Python: 3
- Pyspark: 3.3.0


# Setup

(ünicamente para entorno local en Windows)

Para ejecutar este proyecto, será necesario tener previamente instaladas las versiones de las tecnologías descriptas anteriormente. Puede ser replicado usando:

```
git clone "url de este repositorio"
```

Una vez abierto Docker Desktop, dentro del directorio \tp_bigdata será necesario tipear en la primer terminal la siguiente línea para iniciar el clúster:

```
docker-compose up -d
```
Luego, será necesario crear el tópico manualmente, para evitar errores:

```
docker exec -it kafka kafka-topics --create --topic precios_mercado --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Posteriormente, en una segunda terminal, vamos a ejecutar el productor de los datos financieros:

```
python producer_financiero.py
```

Finalmente, en una tercer terminal, para ejecutar Spark dentro del clúster:

```
docker cp procesamiento_spark.py spark-master:/procesamiento_spark.py

docker exec -it spark-master /spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 --master spark://spark-master:7077 /procesamiento_spark.py
```

Para detener el contenedor de docker, es necesario tipear:

```
docker-compose stop
```

Para detener y eliminar todo:

```
docker-compose down
```