from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://mongodb:27017"
DB_NAME = "metabolite-separation-api"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Acceso directo a las colecciones
evaluates = db["evaluates"]
predicts = db["predicts"]
recommendfamilies = db["recommendfamilies"]
experiments = db["experiments"]
families = db["families"]
feedbacks = db["feedbacks"]
