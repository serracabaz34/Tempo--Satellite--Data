'''
import pandas as pd
import mysql.connector
from datetime import datetime
from geopy.distance import geodesic

# --------------------------
# 1️⃣ MySQL Bağlantısı
# --------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Serra133705ç*",  # Şifreni buraya yaz
    database="yeniveritabani"
)
cursor = conn.cursor(dictionary=True)

# --------------------------
# 2️⃣ Eyalet/başkent koordinatlarını çek
#    (latitude, longitude)
# --------------------------
cursor.execute("SELECT city_name, latitude, longitude FROM situation")
all_locations = pd.DataFrame(cursor.fetchall())  # city_name, latitude, longitude

# --------------------------
# 3️⃣ Grid verilerini çek
#    (longitude, latitude, weight)
# --------------------------
cursor.execute("SELECT id, longitude, latitude, timestamp, weight FROM tempo_o3_data")
grid_data = pd.DataFrame(cursor.fetchall())

cursor.close()
conn.close()

# --------------------------
# 4️⃣ Güvenli nearest_state fonksiyonu
# --------------------------
def nearest_state_safe(grid_lon, grid_lat, locations_df):
    """
    Grid noktasını en yakın eyalet/başkente eşleştirir.
    Hatalı koordinatlar veya weight=None ise atlar.
    """
    min_dist = float('inf')
    nearest = None
    for idx, row in locations_df.iterrows():
        try:
            dist = geodesic((grid_lat, grid_lon), (row['latitude'], row['longitude'])).kilometers
        except ValueError:
            continue
        if dist < min_dist:
            min_dist = dist
            nearest = row['city_name']
    return nearest

# --------------------------
# 5️⃣ Grid noktalarını en yakın eyalete ata
#    (weight değeri None olanları atla)
# --------------------------
grid_data = grid_data[grid_data['weight'].notna()]
grid_data['state_name'] = grid_data.apply(
    lambda row: nearest_state_safe(row['longitude'], row['latitude'], all_locations), axis=1
)

# --------------------------
# 6️⃣ Eyalet bazında günlük ortalama O3
# --------------------------
grid_data['date'] = pd.to_datetime(grid_data['timestamp']).dt.date
state_avg_o3 = grid_data.groupby(['state_name', 'date'])['weight'].mean().reset_index()
state_avg_o3.rename(columns={'weight':'avg_o3'}, inplace=True)

# --------------------------
# 7️⃣ Sonucu CSV’ye kaydet
# --------------------------
state_avg_o3.to_csv("state_avg_o3.csv", index=False)
print("✅ Eyalet bazlı O₃ verisi başarıyla oluşturuldu ve kaydedildi.")
'''

import mysql.connector
import pandas as pd
from geopy.distance import geodesic
from math import inf

# --------------------------
# 1) MySQL bağlantısı
# --------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Serra133705ç*",
    database="yeniveritabani"
)
cursor = conn.cursor(dictionary=True)

# --------------------------
# 2) Eğer state_name kolonu yoksa ekle
# --------------------------
cursor.execute("""
    SELECT COUNT(*) AS cnt 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'yeniveritabani' 
    AND TABLE_NAME = 'tempo_o3_data' 
    AND COLUMN_NAME = 'state_name'
""")
result = cursor.fetchone()

if result["cnt"] == 0:
    cursor.execute("ALTER TABLE tempo_o3_data ADD COLUMN state_name VARCHAR(100)")
    conn.commit()
    print("✅ 'state_name' kolonu eklendi.")
else:
    print("ℹ️ 'state_name' kolonu zaten mevcut.")

# --------------------------
# 3) situation (eyalet/başkent) verilerini al
# --------------------------
dict_cursor = conn.cursor(dictionary=True)
dict_cursor.execute("SELECT city_name, latitude, longitude FROM situation")
locations = pd.DataFrame(dict_cursor.fetchall())
dict_cursor.close()

# --------------------------
# 4) state_name olmayan tempo_o3_data verilerini çek
# --------------------------
cursor2 = conn.cursor(dictionary=True)
cursor2.execute("SELECT id, longitude, latitude FROM tempo_o3_data WHERE state_name IS NULL OR state_name = ''")
to_update_df = pd.DataFrame(cursor2.fetchall())
cursor2.close()

if to_update_df.empty:
    print("🔹 Güncellenecek kayıt yok.")
else:
    # --------------------------
    # 5) nearest fonksiyonu
    # --------------------------
    def nearest_state_safe(grid_lon, grid_lat, locations_df):
        if grid_lon is None or grid_lat is None:
            return None
        min_dist = inf
        nearest = None
        for _, row in locations_df.iterrows():
            try:
                dist = geodesic((grid_lat, grid_lon), (row['latitude'], row['longitude'])).kilometers
            except Exception:
                continue
            if dist < min_dist:
                min_dist = dist
                nearest = row['city_name']
        return nearest

    # --------------------------
    # 6) En yakın state hesapla
    # --------------------------
    to_update_df['state_name'] = to_update_df.apply(
        lambda r: nearest_state_safe(r['longitude'], r['latitude'], locations), axis=1
    )

    # --------------------------
    # 7) DB'ye batch halinde update et
    # --------------------------
    update_sql = "UPDATE tempo_o3_data SET state_name = %s WHERE id = %s"
    update_list = [(row['state_name'], int(row['id'])) for _, row in to_update_df.iterrows()]

    batch_size = 2000
    cursor_exec = conn.cursor()
    for i in range(0, len(update_list), batch_size):
        chunk = update_list[i:i+batch_size]
        cursor_exec.executemany(update_sql, chunk)
        conn.commit()
        print(f"✅ Güncellendi {i} - {i+len(chunk)-1}")

    cursor_exec.close()
    print("🎉 Tüm güncellemeler tamamlandı.")

cursor.close()
conn.close()

