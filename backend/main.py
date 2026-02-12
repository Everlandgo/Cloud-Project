from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiomysql
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 환경변수 필수 체크 함수
def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Environment variable '{key}' is not set")
    return value


# 🔹 DB 설정 (환경변수 기반)
db_config = {
    "host": get_env("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),  # 기본 3306
    "user": get_env("DB_USER"),
    "password": get_env("DB_PASSWORD"),
    "db": get_env("DB_NAME"),
}


# 🔹 전역 Connection Pool
pool = None


@app.on_event("startup")
async def startup():
    global pool
    pool = await aiomysql.create_pool(
        minsize=1,
        maxsize=50,
        autocommit=True,   # commit 누락 방지
        **db_config
    )


@app.on_event("shutdown")
async def shutdown():
    global pool
    if pool:
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
            return await cursor.fetchone()


# 🔹 방문 기록 추가
@app.post("/visit")
async def add_visit(visitor: Visitor):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute(
                    "INSERT INTO visitor_log (text) VALUES (%s)",
                    (visitor.text,)
                )
                return {"message": "Saved"}
            except Exception:
                raise HTTPException(status_code=500, detail="Save failed")


# 🔹 방문 기록 조회
@app.get("/visits")
async def get_visits():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT text FROM visitor_log ORDER BY id DESC"
            )
            rows = await cursor.fetchall()
            return [row["text"] for row in rows]
