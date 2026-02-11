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
def submit_todo():

    data = request.get_json()

    mongo.db.todos.insert_one({
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription"),
        "itemId": data.get("itemId"),
        "itemUUID": data.get("itemUUID"),
        "itemHash": data.get("itemHash")
    })

    return jsonify({"message":"Todo added"})

 
    
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
