from netCDF4 import Dataset, num2date
import numpy as np
import mysql.connector
from datetime import datetime, timezone

# --------------------------
# NetCDF dosyasını aç
# --------------------------
file_path = "TEMPO_NO2_L3_V04_20251004T213103Z_S012.nc"
dataset = Dataset(file_path, "r")

# Koordinatları ve NO2 verisini al
latitudes = dataset.variables['latitude'][:]
longitudes = dataset.variables['longitude'][:]
no2_data = dataset.variables['weight'][:, :]  # NO2 verisi

print("Latitude örnekleri:", latitudes[:10])
print("Longitude örnekleri:", longitudes[:10])

# --------------------------
# Örnekleme adımı (sample step)
# --------------------------
sample_step = 300
lat_sampled = latitudes[::sample_step]
lon_sampled = longitudes[::sample_step]
no2_sampled = no2_data[::sample_step, ::sample_step]

# Grid oluştur
lon_grid, lat_grid = np.meshgrid(lon_sampled, lat_sampled)

# --------------------------
# Zaman damgası
# --------------------------
time_var = dataset.variables.get('time')
if time_var is not None:
    times = num2date(time_var[:], units=time_var.units)
    timestamp = datetime(times[0].year, times[0].month, times[0].day,
                         times[0].hour, times[0].minute, times[0].second, tzinfo=timezone.utc)
else:
    timestamp = datetime.now(timezone.utc)

# --------------------------
# Helper: masked veya NaN değerleri None yap
# --------------------------
def safe_value(x):
    if np.ma.is_masked(x) or np.isnan(x):
        return None
    return float(x)

# --------------------------
# Insert için veri hazırlama
# --------------------------
data_to_insert = [
    (timestamp,
     float(lon_grid[i, j]),
     float(lat_grid[i, j]),
     safe_value(no2_sampled[i, j]))
    for i in range(lat_grid.shape[0])
    for j in range(lon_grid.shape[1])
    if not np.ma.is_masked(no2_sampled[i, j]) and not np.isnan(no2_sampled[i, j])
]

# --------------------------
# MySQL bağlantısı
# --------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Serra133705ç*",           
    database="yeniveritabani"
)
cursor = conn.cursor()

# --------------------------
# Batch insert (5000 kayıtlık gruplar)
# --------------------------
batch_size = 5000
for k in range(0, len(data_to_insert), batch_size):
    batch = data_to_insert[k:k + batch_size]
    cursor.executemany(
        "INSERT IGNORE INTO tempodata (timestamp, longitude, latitude, no2) VALUES (%s, %s, %s, %s)",
        batch
    )

conn.commit()
cursor.close()
conn.close()

print(f"✅ NetCDF verisi başarıyla tempodata tablosuna kaydedildi. Toplam {len(data_to_insert)} kayıt eklendi.")
