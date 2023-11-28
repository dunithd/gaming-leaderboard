from kafka import KafkaProducer
import json
import random
from datetime import datetime, timedelta
import time
import uuid

# Kafka broker settings
bootstrap_servers = 'localhost:19092'
topic = 'gameplays'

# Create 20 player names 
player_names = [
    "ShadowBladeX",
    "NovaGamer88",
    "QuantumSniper",
    "BlazeMaster3000",
    "FrostByte64",
    "PhantomStriker",
    "CyberSpectre",
    "VortexPilot",
    "IronPhoenix76",
    "StealthNinja21",
    "GalacticJester",
    "TitanReaperX",
    "MysticWraith97",
    "InfernoKnight45",
    "NeonSpecter99",
    "ThunderFury23",
    "StarlightRanger",
    "CrystalSorcerer",
    "ZeroGravityX",
    "CelestialRebel"
]

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to generate random JSON messages
def generate_random_message():
    event_id = str(uuid.uuid4()) 
    game_id = 1
    player = random.choice(player_names)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    score = random.randint(0, 100)

    message = {
        "event_id": event_id,
        "game_id": game_id,
        "player": player,
        "created_at": created_at,
        "score": score
    }

    return message

# Produce random messages to the Kafka topic
try:
    while True:
        # Generate a random JSON message
        message = generate_random_message()

        # Produce the message to the "gameplays" topic
        producer.send(topic, value=message)

        # Print the produced message
        print(f"Produced message: {message}")

        # Sleep for a while before producing the next message
        # Adjust the sleep time as needed
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    # Close the Kafka producer
    producer.close()
