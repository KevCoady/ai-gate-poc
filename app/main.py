from fastapi import FastAPI, HTTPException
from app.database import get_db_connection

app = FastAPI(title="User API Microservice")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/users/{username}")
def get_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {"id": row[0], "username": row[1], "email": row[2], "role": row[3]}