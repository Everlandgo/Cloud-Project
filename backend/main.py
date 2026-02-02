from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiomysql

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 설정
db_config = {
    "host": "172.16.1.2",
    #"10.0.11.25",
    "port": 3306,
    "user": "root",
    "password": "root",
    "db": "cloud_project",
}

# 🔹 MySQL Connection Pool
pool: aiomysql.Pool = None


@app.on_event("startup")
async def startup():
    global pool
    pool = await aiomysql.create_pool(
        minsize=1,
        maxsize=50,
        **db_config
    )


@app.on_event("shutdown")
async def shutdown():
    pool.close()
    await pool.wait_closed()


class Visitor(BaseModel):
    text: str


# 🔹 방문자 수 조회
@app.get("/count")
async def get_count():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT COUNT(*) AS count FROM visitor_log")
            result = await cursor.fetchone()
            return result


# 🔹 방문 기록 추가
@app.post("/visit")
async def add_visit(visitor: Visitor):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                sql = "INSERT INTO visitor_log (text) VALUES (%s)"
                await cursor.execute(sql, (visitor.text,))
                await conn.commit()
                return {"message": "Saved"}
            except Exception as e:
                print(f"Insert Error: {e}")
                raise HTTPException(status_code=500, detail="Save failed")


# 🔹 방문 기록 조회
@app.get("/visits")
async def get_visits():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT text FROM visitor_log ORDER BY id DESC")
            rows = await cursor.fetchall()
            return [row["text"] for row in rows]