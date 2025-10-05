
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import os

# Routers
from routers import fastapi_tempo
from routers import fastapi_openweather


# from routers import fastapi_predict  # istersen açabilirsin

# -------------------------------
# 🚀 FastAPI Uygulaması
# -------------------------------
app = FastAPI()

# -------------------------------
# 📌 CORS Middleware
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # test için tüm originler, prod’da frontend URL yaz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 📌 Frontend Static Dosyaları
# -------------------------------
# HTML dosyalarının bulunduğu klasör
app.mount("/static", StaticFiles(directory="C:/Users/serra/luck"), name="static")

# -------------------------------
# 📌 Router’ları ekle
# -------------------------------
app.include_router(fastapi_tempo.router)
app.include_router(fastapi_openweather.router)
# app.include_router(fastapi_predict.router)


# -------------------------------
# 📌 MySQL Bağlantısı
# -------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Serra133705ç*",
        database="yeniveritabani"
    )

# -------------------------------
# 📌 Kullanıcı Modelleri
# -------------------------------
class User(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str
    password: str | None = None  # şifre unutma için None olabilir

class ForgotPasswordRequest(BaseModel):
    username: str

class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str
    confirm_password: str

# -------------------------------
# 📌 Signup Endpoint
# -------------------------------
@app.post("/signup")
async def signup(user: User):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO users (first_name, last_name, username, password)
        VALUES (%s, %s, %s, %s)
        """
        values = (user.name, user.surname, user.username, user.password)
        cursor.execute(sql, values)
        conn.commit()
        return {"message": "Kayıt başarılı"}
    except Error as e:
        print("DB Error:", e)
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten var olabilir.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# -------------------------------
# 📌 Login Endpoint
# -------------------------------
@app.post("/login")
async def login(user: User):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (user.username, user.password))
        db_user = cursor.fetchone()
        if not db_user:
            raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre yanlış!")
        return {
            "success": True,
            "user_id": db_user["id"],
            "name": db_user["first_name"],
            "surname": db_user["last_name"],
            "username": db_user["username"]
        }
    except Error as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Veritabanı hatası!")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# -------------------------------
# 📌 Forgot Password Endpoint
# -------------------------------
@app.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (data.username,))
        db_user = cursor.fetchone()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User found"}
    except Error as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Veritabanı hatası!")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# -------------------------------
# 📌 Reset Password Endpoint
# -------------------------------
@app.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(sql, (data.new_password, data.username))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "Password updated successfully"}
    except Error as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Veritabanı hatası!")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()