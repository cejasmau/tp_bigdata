import time
import random
import json
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_nombre = "precios_mercado"
acciones = ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'MSFT']
precios = {
    "AAPL": 275.0,
    "MSFT": 393.0,
    "GOOG": 331.0,
    "AMZN": 222.0,
    "TSLA": 397.0
}

print(f" Iniciando envío de datos al tópico: {topic_nombre}")

try:
    while True:
        for accion in acciones:
            variacion = precios[accion] * random.uniform(-0.001, 0.001)
            precios[accion] += variacion
            
            mensaje = {
                'timestamp': time.time(),
                'simbolo': accion,
                'precio': round(precios[accion], 2)            }
            
            producer.send(topic_nombre, value=mensaje)
            print(f"Enviado: {mensaje}")
            
        time.sleep(5)  
        
except KeyboardInterrupt:
    print("\n Simulación detenida por el usuario.")
finally:
    producer.close()
