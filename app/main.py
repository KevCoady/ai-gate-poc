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

@app.get("/search")
def search_users(q: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Flaw: raw string interpolation (direct SQL injection vulnerability)
    query = f"SELECT id, username, email FROM users WHERE username = '{q}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "username": r[1], "email": r[2]} for r in results]