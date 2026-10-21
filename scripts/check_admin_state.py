"""Read-only report of bootstrap state, with no user fields or secrets."""
import os

from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_URI"], serverSelectionTimeoutMS=5000)
try:
    db = client[os.environ["MONGODB_DATABASE"]]
    print(f"admin_users={db['admin_users'].count_documents({})}")
    print(f"roles={db['roles'].count_documents({})}")
finally:
    client.close()
