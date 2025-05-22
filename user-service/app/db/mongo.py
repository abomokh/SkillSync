from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


###############
# db = client.userdb
# users_collection = db.users
db = client.draft_db
users_collection = db['user_collection']