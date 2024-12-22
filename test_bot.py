import os
from typing import Dict, Any, List
import json

import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

# # Database Configuration
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "root",
#     "database": "mybd"
# }


# def get_db_connection():
#     """Establish and return a database connection"""
#     return mysql.connector.connect(**DB_CONFIG)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mybd")


def init_database():
    """Initialize database and create table if it doesn't exist"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS conversations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Database initialized successfully")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
        raise


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json"""
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def load_conversations() -> List[Dict[str, str]]:
    """Load all conversations from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all conversations
        cursor.execute(
            "SELECT question as user, response as model FROM conversations ORDER BY id")
        conversations = cursor.fetchall()

        cursor.close()
        connection.close()

        return conversations if conversations else []

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []


def save_conversation(question: str, response: str):
    """Save a single conversation to the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = "INSERT INTO conversations (question, response) VALUES (%s, %s)"
        values = (question, response)
        cursor.execute(sql, values)

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        raise


# Initialize database
init_database()

# Initialize Gemini model
config = load_config()
genai.configure(api_key=config['gemini_api_key'])
model = genai.GenerativeModel("gemini-1.5-flash")

# FastAPI application
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model


class MessageRequest(BaseModel):
    message: str


@app.post("/msg")
async def send_message(request: MessageRequest):
    try:
        # Load conversation history
        conversations = load_conversations()

        # Prepare chat history
        chat_history = [
            {"role": "user", "parts": json.dumps(config)}
        ]

        # Add previous conversations to chat history
        for conv in conversations:
            chat_history.append({"role": "user", "parts": conv['user']})
            chat_history.append({"role": "model", "parts": conv['model']})

        # Start chat with full history
        chat = model.start_chat(history=chat_history)

        # Send new message
        response = chat.send_message(request.message)

        # Save conversation to database
        save_conversation(request.message, response.text)

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_conversations():
    """Clear all conversations from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("TRUNCATE TABLE conversations")

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Conversation history reset"}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9091)
