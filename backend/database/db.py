from pymongo import MongoClient
import os
client = MongoClient(os.getenv("MONGO_URI"))

try:
    client.admin.command("ping")
    print("✅ MongoDB Atlas Connected")
except Exception as e:
    print("❌ MongoDB Error:", e)

db = client["resume_ai"]

scores = db["scores"]