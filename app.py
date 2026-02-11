from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import os
import traceback

#################################
# Load Environment Variables FIRST
#################################
load_dotenv()

#################################
# Create Flask App
#################################
app = Flask(__name__)
CORS(app)

#################################
# Mongo Config
#################################
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise Exception("❌ MONGO_URI not found in .env")

app.config["MONGO_URI"] = mongo_uri

#################################
# Initialize PyMongo
#################################
mongo = PyMongo(app)

# Test connection at startup
try:
    mongo.cx.server_info()
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed:")
    print(e)

#################################
# Routes
#################################

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        data = request.get_json(force=True)

        print("Incoming Data:", data)  # Debug

        item_name = data.get("itemName")
        item_description = data.get("itemDescription")

        if not item_name or not item_description:
            return jsonify({"error": "Both fields required"}), 400

        result = mongo.db.todos.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        print("✅ Inserted ID:", result.inserted_id)

        return jsonify({
            "message": "Todo added successfully!"
        }), 201

    except Exception as e:
        print("🔥 FULL ERROR BELOW 🔥")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@app.route("/gettodos", methods=["GET"])
def get_todos():
    todos = []
    for todo in mongo.db.todos.find():
        todos.append({
            "id": str(todo["_id"]),
            "itemName": todo["itemName"],
            "itemDescription": todo["itemDescription"]
        })
    return jsonify(todos)



#################################
# Run Server
#################################
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
