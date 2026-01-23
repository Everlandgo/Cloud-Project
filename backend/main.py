from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel   
import mysql.connector
from mysql.connector import Error

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 설정을 딕셔너리로 관리
db_config = {
    "host": "10.0.11.26", 
    "port": "3306",
    "user": "root",
    "password": "root",
    "database": "cloud_project"
}

def get_db_connection():
    """DB 연결을 생성하고 반환하는 헬퍼 함수"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

class Visitor(BaseModel):
    text: str

@app.get("/count")
def get_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM visitor_log")
        result = cursor.fetchone()
        return result
    finally:
        cursor.close()
        conn.close() # 요청이 끝나면 반드시 닫기

@app.post("/visit")
def add_visit(visitor: Visitor):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO visitor_log (text) VALUES (%s)"
        cursor.execute(sql, (visitor.text,))
        conn.commit()
        return {"message": "Saved"}
    except Error as e:
        print(f"Insert Error: {e}")
        raise HTTPException(status_code=500, detail="Save failed")
    finally:
        cursor.close()
        conn.close()

@app.get("/visits")
def get_visits():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT text FROM visitor_log ORDER BY id DESC")
        rows = cursor.fetchall()
        return [row["text"] for row in rows]
    finally:
        cursor.close()
        conn.close()