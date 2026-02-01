import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.matcher import UniversityMatcher
from services.chatbot import get_chat_response

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure CORS from environment variables
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:8080,http://localhost:3000").split(",")
CORS(app, origins=cors_origins)

@app.route("/")
def home():
    return "<p>Hello from Flask via uv!</p>"

@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    POST endpoint to get ranked university program recommendations.
    
    Expected JSON payload:
    {
        "grade_level": int,
        "average": float,
        "wants_coop": bool,
        "extra_curriculars": [("name", level), ...],
        "major_interests": ["interest1", "interest2", ...],
        "courses_taken": [("course_code", grade), ...]
    }
    """
    try:
        # Get JSON payload
        student_profile = request.get_json()
        
        # Validate required fields
        required_fields = ['grade_level', 'average', 'wants_coop', 'extra_curriculars', 
                          'major_interests', 'courses_taken']
        missing_fields = [field for field in required_fields if field not in student_profile]
        
        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing": missing_fields
            }), 400
        
        # Instantiate matcher and get rankings
        matcher = UniversityMatcher(student_profile)
        rankings = matcher.get_ranked_programs()
        
        return jsonify({
            "success": True,
            "rankings": rankings,
            "total_programs": len(rankings)
        }), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "message": str(e),
            "trace": traceback.format_exc()
        }), 500
    
@app.route("/api/db-health", methods=["GET"])
def db_health():
    from services.database import fetch_university_data
    doc = fetch_university_data()
    return jsonify({"ok": True, "keys": list(doc.keys())[:10]})

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        # 1. Get the message from the Frontend
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "I didn't hear anything!"}), 400

        # 2. Get the answer from the 'Brain' (chatbot.py)
        bot_reply = get_chat_response(user_message)

        # 3. Send the answer back to the Frontend
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Chat Error: {e}")
        return jsonify({"reply": "Server error."}), 500

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5001))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host=host, port=port, debug=debug)
