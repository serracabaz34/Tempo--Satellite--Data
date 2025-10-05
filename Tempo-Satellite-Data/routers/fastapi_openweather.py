# main.py
from fastapi import APIRouter, HTTPException
from core.database import get_connection, close_connection

router = APIRouter(prefix="/openweather")

# ----------------------------
# Endpoint: Güncel hava durumu
# ----------------------------
@router.get("/weather/{state}")
def get_weather(state: str):
    conn = get_connection()
    if not conn:
        return {"error": "DB bağlantısı sağlanamadı."}

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM weather WHERE state=%s ORDER BY last_updated DESC LIMIT 1", 
        (state,)
    )
    data = cursor.fetchone()
    close_connection(conn, cursor)

    return data or {"error": "Veri bulunamadı."}

# ----------------------------
# Endpoint: Hava kalitesi
# ----------------------------
@router.get("/air_quality/{state}")
def get_air_quality(state: str):
    conn = get_connection()
    if not conn:
        return {"error": "DB bağlantısı sağlanamadı."}

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM air_quality WHERE state=%s ORDER BY last_updated DESC LIMIT 1", 
        (state,)
    )
    data = cursor.fetchone()
    close_connection(conn, cursor)

    return data or {"error": "Veri bulunamadı."}

# ----------------------------
# Endpoint: 3 saatlik tahmin
# ----------------------------
@router.get("/forecast/3h/{state}")
def get_forecast_3h(state: str):
    conn = get_connection()
    if not conn:
        return {"error": "DB bağlantısı sağlanamadı."}

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM weather_3h_forecast WHERE state=%s ORDER BY forecast_time ASC", 
        (state,)
    )
    data = cursor.fetchall()
    close_connection(conn, cursor)

    return data or {"error": "Veri bulunamadı."}

