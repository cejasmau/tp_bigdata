# Introducción

El objetivo de este trabajo es diseñar e implementar un clúster virtualizado que permita simular una infraestructura Big Data orientada al análisis de datos del mercado financiero. Para ello, se utilizó Docker como tecnología de virtualización liviana, desplegando un clúster compuesto por tres nodos que integran Apache Spark, Apache Kafka y Apache Zookeeper.

# Versiones

- Docker desktop 4.58.0
- WSL: 2.6.3.0
- Docker: 29.1.3
- Docker-compose: 5.0.1
- Kafka: 7.0.1
- Kafka-python: 2.3.0
- Zookeeper: 

# Setup

(ünicamente para entorno local)

Para ejecutar este proyecto, será necesario tener previamente instaladas las versiones de las tecnologías descriptas arriba. Puede ser instalado usando:

```
$ git clone "url de este repositorio"
```

Una vez dentro del directorio \tp_bigdata será necesario tipear las siguientes líneas para configurar Kafka y Zookeeper:

```
$ sudo docker-compose up
```

Luego, será necesario abrir tres terminales separadas para ejecutar tres aplicaciones en paralelo (el productor de Spark, el consumidor de Kafka y el streaming de Spark ????). Para ello, será necesario tipear los siguientes comandos:

Primer terminal:
```
$ python producer_simulado.py
```

Segunda terminal:
```
$ docker exec -it node2-kafka bash
$ kafka-console-consumer \
$  --bootstrap-server localhost:9092 \
$  --topic market-data \
$  --from-beginning
``` 

Tercer terminal:
```
$ docker exec -it node1-spark-master bash
$ /spark/bin/spark-submit \
$  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
$  /spark/jobs/streaming_kafka.py
```

Para detener el contenedor de docker, es necesario tipear:

```
$ ./stop.sh ?????
```

Para eliminar los tópicos de Kafka, podemos escribir:

```
$ ./removeTopic.sh ?????
```