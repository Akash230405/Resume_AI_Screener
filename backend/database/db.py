from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://resumeadmin:ResumeAI123@cluster0resumeaicluster.wwfdp72.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0ResumeAICluster"
)

try:
    client.admin.command("ping")
    print("✅ MongoDB Atlas Connected")
except Exception as e:
    print("❌ MongoDB Error:", e)

db = client["resume_ai"]

scores = db["scores"]