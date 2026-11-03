from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from mqtt_manager import mqtt_manager
from database import listar_leituras

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print()
    print("===================")
    print(" API IOT Vetallis ")

    mqtt_manager.start()

    print()
    print("================================")
    print("SISTEMA INICIALIZADO")
    print("================================")

    print()
    print("FastAPI: OK")
    print("MySQL:   OK")
    print("MQTT:    iniciando")

    print()
    print(
        "Aguardando dados dos sensores..."
    )

    yield

    print()
    print("Encerrando sistema...")

    mqtt_manager.stop()

    print(
        "Sistema encerrado."
    )

app = FastAPI(

    title="API IoT Vetallis",

    description=(
        "API para monitoramento dos sensores "
        "DHT11, LDR e MFRC522."
    ),

    version="1.0.0",

    lifespan=lifespan
)

# Permite que a tela do Vetallis (Flask) leia esta API pelo navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "online",

        "projeto": "IoT SENAI",

        "mqtt": "ativo",

        "sensores": [
            "DHT11",
            "HC-SR04",
            "MFRC522"
        ]
    }

@app.get("/leituras")
def get_leituras(device_id: str = None, sensor: str = None, limite: int = Query( default=100, ge=1, le=1000 )):
    
    resultado = listar_leituras(device_id = device_id, sensor = sensor, limite = limite)

    return {
        "quantidade": len(resultado),

        "filtros": {

            "device_id": device_id,

            "sensor": sensor,

            "limite": limite

        },

        "leituras": resultado
    }

@app.get("/sensores/dht11")
def get_dht11(device_id: str = None, limite: int = Query( default=100, ge=1, le=1000 )):

    resultado = listar_leituras( 

        device_id = device_id,

        sensor = "DHT11",

        limite = limite

    )

    return {

        "sensor": "DHT11",

        "quantidade": len(resultado),

        "leituras": resultado

    }


@app.get("/sensores/ldr")
def get_ldr(device_id: str = None, limite: int = Query( default=100, ge=1, le=1000 )):
    
    resultado = listar_leituras(

        device_id = device_id,

        sensor = "LDR",

        limite = limite

    )


    return {

        "sensor": "LDR",

        "quantidade": len(resultado),

        "leituras": resultado

    }

@app.get("/sensores/mfrc522")
def get_mfrc522(device_id: str = None, limite: int = Query( default=100, ge=1, le=1000 )):

    resultado = listar_leituras(
        device_id = device_id,

        sensor = "MFRC522",

        limite = limite
    )

    return{
        "sensor": "MFRC522",
        "quantidade": len(resultado),
        "leituras": resultado
    }

@app.get("/sensor/dht11/ultima")
def get_ultima_dht11(device_id: str = None):
    
    resultado = listar_leituras(

        device_id=device_id,

        sensor="DHT11",

        limite=1

    )


    if not resultado:

        return {

            "sensor": "DHT11",

            "leitura": None

        }


    return {

        "sensor": "DHT11",

        "leitura": resultado[0]

    }

@app.get("/sensores/ldr/ultima")
def get_ldr_ultima( device_id: str = None):
    
    resultado = listar_leituras(

        device_id=device_id,

        sensor="LDR",

        limite=1

    )


    if not resultado:

        return {

            "sensor": "LDR",

            "leitura": None

        }


    return {

        "sensor": "LDR",

        "leitura": resultado[0]

    }

@app.get("/sensores/mfrc522/ultima")
def get_mfrc522_ultima( device_id: str = None):

    resultado = listar_leituras(

        device_id=device_id,

        sensor="MFRC522",

        limite=1

    )


    if not resultado:

        return {

            "sensor": "MFRC522",

            "leitura": None

        }


    return {

        "sensor": "MFRC522",

        "leitura": resultado[0]

    }