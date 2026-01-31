"""
Database connection module for MongoDB.
"""
import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=str(env_path))

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "university_admission_information"
COLLECTION_NAME = "ontario_universities"

# Global client and database instances
_client = None
_database = None


def get_database():
    """
    Get MongoDB database instance. Creates connection if it doesn't exist.
    """
    global _client, _database
    
    if _database is None:
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is not set")
        
        _client = MongoClient(MONGODB_URI)
        _database = _client[DATABASE_NAME]
    
    return _database


def get_universities_collection():
    """
    Get the ontario_universities collection.
    """
    db = get_database()
    return db[COLLECTION_NAME]


def fetch_university_data():
    """
    Fetch all university data from MongoDB and transform it to match the expected structure.
    Returns a dictionary in the same format as the mock data.
    
    Expected MongoDB document structure (same as mock data):
    Each document in the collection should have the structure:
    {
        "University Name": {
            "ec_quality": int,
            "co-op": [...],  # University-level co-op options
            "programs": {
                "Program Name": {
                    "recommended_average": [min, max],
                    "interest_fields": [...],
                    "required_courses": [...]
                }
            }
        }
    }
    
    OR the entire database might be stored as a single document with all universities.
    """
    collection = get_universities_collection()
    
    # Fetch all documents from the collection
    documents = list(collection.find({}))
    
    if not documents:
        raise ValueError("No documents found in the MongoDB collection")
    
    # Transform MongoDB documents to match the expected structure
    university_db = {}
    
    for doc in documents:
        # MongoDB documents have _id, remove it for processing
        doc.pop('_id', None)
        
        # The document structure should match the mock data structure exactly
        # Each document might represent one university or the entire database
        # We'll merge all documents into a single dictionary
        for key, value in doc.items():
            if isinstance(value, dict) and 'ec_quality' in value and 'co-op' in value and 'programs' in value:
                university_db[key] = value
    
    if not university_db:
        raise ValueError("No valid university data found in MongoDB documents. Expected structure: {university_name: {ec_quality: int, co-op: [...], programs: {...}}}")
    
    return university_db


def close_connection():
    """
    Close MongoDB connection.
    """
    global _client, _database
    if _client:
        _client.close()
        _client = None
        _database = None

