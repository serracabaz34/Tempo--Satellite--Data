
# routers/tempo.py
from fastapi import APIRouter, HTTPException
from core.database import get_connection, close_connection
from core.config import settings

router = APIRouter(prefix="/tempo")

def get_data_by_state(table_name: str, state_name: str, value_col: str = "weight"):
    """
    Belirli tablo ve state_name için veriyi döner.
    value_col ile hangi kolon çekileceğini belirleyebilirsin.
    """
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB bağlantısı sağlanamadı.")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"""
        SELECT timestamp, {value_col} AS value
        FROM {table_name}
        WHERE state_name=%s
        ORDER BY timestamp ASC
        """,
        (state_name,)
    )
    data = cursor.fetchall()
    close_connection(conn, cursor)

    if not data:
        raise HTTPException(status_code=404, detail="Veri bulunamadı.")
    
    return {"state_name": state_name, "data": data}

# O3
@router.get("/o3/state/{state_name}")
def get_o3_by_state(state_name: str):
    return get_data_by_state("tempo_o3_data", state_name, value_col="weight")

# NO2
@router.get("/no2/state/{state_name}")
def get_no2_by_state(state_name: str):
    return get_data_by_state("tempodata", state_name, value_col="no2")

# HCHO
@router.get("/hcho/state/{state_name}")
def get_hcho_by_state(state_name: str):
    return get_data_by_state("tempo_hcho_data", state_name, value_col="weight")

# O2O2
@router.get("/o2o2/state/{state_name}")
def get_o2o2_by_state(state_name: str):
    return get_data_by_state("tempo_o2o2_data", state_name, value_col="weight")