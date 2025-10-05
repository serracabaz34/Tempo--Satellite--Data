import requests
from datetime import datetime
from core.database import get_connection, close_connection
import time
from core.config import settings

OPENWEATHER_API_KEY = settings.OPENWEATHER_API_KEY 


states = [
    # --- ABD 50 eyalet ---
    {"state": "Alabama", "country": "US", "lat": 32.3777, "lon": -86.3000},
    {"state": "Alaska", "country": "US", "lat": 58.3019, "lon": -134.4197},
    {"state": "Arizona", "country": "US", "lat": 33.4484, "lon": -112.0740},
    {"state": "Arkansas", "country": "US", "lat": 34.7465, "lon": -92.2896},
    {"state": "California", "country": "US", "lat": 38.5816, "lon": -121.4944},
    {"state": "Colorado", "country": "US", "lat": 39.7392, "lon": -104.9903},
    {"state": "Connecticut", "country": "US", "lat": 41.7658, "lon": -72.6734},
    {"state": "Delaware", "country": "US", "lat": 39.1582, "lon": -75.5244},
    {"state": "Florida", "country": "US", "lat": 30.4383, "lon": -84.2807},
    {"state": "Georgia", "country": "US", "lat": 33.7490, "lon": -84.3880},
    {"state": "Hawaii", "country": "US", "lat": 21.3069, "lon": -157.8583},
    {"state": "Idaho", "country": "US", "lat": 43.6150, "lon": -116.2023},
    {"state": "Illinois", "country": "US", "lat": 39.7817, "lon": -89.6501},
    {"state": "Indiana", "country": "US", "lat": 39.7684, "lon": -86.1581},
    {"state": "Iowa", "country": "US", "lat": 41.5868, "lon": -93.6250},
    {"state": "Kansas", "country": "US", "lat": 39.0489, "lon": -95.6780},
    {"state": "Kentucky", "country": "US", "lat": 38.2009, "lon": -84.8733},
    {"state": "Louisiana", "country": "US", "lat": 30.4515, "lon": -91.1871},
    {"state": "Maine", "country": "US", "lat": 44.3106, "lon": -69.7795},
    {"state": "Maryland", "country": "US", "lat": 38.9784, "lon": -76.4922},
    {"state": "Massachusetts", "country": "US", "lat": 42.3601, "lon": -71.0589},
    {"state": "Michigan", "country": "US", "lat": 42.7325, "lon": -84.5555},
    {"state": "Minnesota", "country": "US", "lat": 44.9537, "lon": -93.0900},
    {"state": "Mississippi", "country": "US", "lat": 32.2988, "lon": -90.1848},
    {"state": "Missouri", "country": "US", "lat": 38.5767, "lon": -92.1735},
    {"state": "Montana", "country": "US", "lat": 46.5884, "lon": -112.0245},
    {"state": "Nebraska", "country": "US", "lat": 40.8136, "lon": -96.7026},
    {"state": "Nevada", "country": "US", "lat": 39.1638, "lon": -119.7674},
    {"state": "New Hampshire", "country": "US", "lat": 43.2081, "lon": -71.5376},
    {"state": "New Jersey", "country": "US", "lat": 40.2206, "lon": -74.7699},
    {"state": "New Mexico", "country": "US", "lat": 35.6870, "lon": -105.9378},
    {"state": "New York", "country": "US", "lat": 42.6526, "lon": -73.7562},
    {"state": "North Carolina", "country": "US", "lat": 35.7796, "lon": -78.6382},
    {"state": "North Dakota", "country": "US", "lat": 46.8083, "lon": -100.7837},
    {"state": "Ohio", "country": "US", "lat": 39.9612, "lon": -82.9988},
    {"state": "Oklahoma", "country": "US", "lat": 35.4676, "lon": -97.5164},
    {"state": "Oregon", "country": "US", "lat": 44.9429, "lon": -123.0351},
    {"state": "Pennsylvania", "country": "US", "lat": 40.2732, "lon": -76.8867},
    {"state": "Rhode Island", "country": "US", "lat": 41.8236, "lon": -71.4222},
    {"state": "South Carolina", "country": "US", "lat": 34.0007, "lon": -81.0348},
    {"state": "South Dakota", "country": "US", "lat": 44.3683, "lon": -100.3510},
    {"state": "Tennessee", "country": "US", "lat": 36.1627, "lon": -86.7816},
    {"state": "Texas", "country": "US", "lat": 30.2672, "lon": -97.7431},
    {"state": "Utah", "country": "US", "lat": 40.7608, "lon": -111.8910},
    {"state": "Vermont", "country": "US", "lat": 44.2601, "lon": -72.5754},
    {"state": "Virginia", "country": "US", "lat": 37.5407, "lon": -77.4360},
    {"state": "Washington", "country": "US", "lat": 47.0379, "lon": -122.9007},
    {"state": "West Virginia", "country": "US", "lat": 38.3498, "lon": -81.6326},
    {"state": "Wisconsin", "country": "US", "lat": 43.0731, "lon": -89.4012},
    {"state": "Wyoming", "country": "US", "lat": 41.1400, "lon": -104.8202},

    # --- Kanada 13 eyalet/bölge ---
    {"state": "Alberta", "country": "CA", "lat": 53.5461, "lon": -113.4938},
    {"state": "British Columbia", "country": "CA", "lat": 48.4284, "lon": -123.3656},
    {"state": "Northwest Territories", "country": "CA", "lat": 62.4540, "lon": -114.3718},
    {"state": "Manitoba", "country": "CA", "lat": 49.8951, "lon": -97.1384},
    {"state": "New Brunswick", "country": "CA", "lat": 45.9636, "lon": -66.6431},
    {"state": "Newfoundland and Labrador", "country": "CA", "lat": 47.5615, "lon": -52.7126},
    {"state": "Nunavut", "country": "CA", "lat": 63.7467, "lon": -68.5169},
    {"state": "Ontario", "country": "CA", "lat": 43.6532, "lon": -79.3832},
    {"state": "Quebec", "country": "CA", "lat": 46.8139, "lon": -71.2080},
    {"state": "Prince Edward Island", "country": "CA", "lat": 46.2382, "lon": -63.1311},
    {"state": "Saskatchewan", "country": "CA", "lat": 50.4452, "lon": -104.6189},
    {"state": "Nova Scotia", "country": "CA", "lat": 44.6488, "lon": -63.5752},
    {"state": "Yukon", "country": "CA", "lat": 60.7212, "lon": -135.0568},

    # --- Meksika 32 eyalet ---
    {"state": "Aguascalientes", "country": "MX", "lat": 21.8853, "lon": -102.2916},
    {"state": "Baja California", "country": "MX", "lat": 32.6245, "lon": -115.4523},
    {"state": "Baja California Sur", "country": "MX", "lat": 24.1426, "lon": -110.3128},
    {"state": "Campeche", "country": "MX", "lat": 19.8301, "lon": -90.5349},
    {"state": "Chiapas", "country": "MX", "lat": 16.7597, "lon": -93.1131},
    {"state": "Ciudad de México", "country": "MX", "lat": 19.4326, "lon": -99.1332},
    {"state": "Chihuahua", "country": "MX", "lat": 28.6320, "lon": -106.0691},
    {"state": "Coahuila", "country": "MX", "lat": 25.4232, "lon": -100.9930},
    {"state": "Colima", "country": "MX", "lat": 19.2433, "lon": -103.7250},
    {"state": "Durango", "country": "MX", "lat": 24.0277, "lon": -104.6532},
    {"state": "Guanajuato", "country": "MX", "lat": 21.0190, "lon": -101.2574},
    {"state": "Guerrero", "country": "MX", "lat": 17.5506, "lon": -99.5058},
    {"state": "Hidalgo", "country": "MX", "lat": 20.1011, "lon": -98.7591},
    {"state": "Jalisco", "country": "MX", "lat": 20.6597, "lon": -103.3496},
    {"state": "México", "country": "MX", "lat": 19.3574, "lon": -99.6664},
    {"state": "Michoacán", "country": "MX", "lat": 19.5665, "lon": -101.7068},
    {"state": "Morelos", "country": "MX", "lat": 18.6813, "lon": -99.1013},
    {"state": "Nayarit", "country": "MX", "lat": 21.7514, "lon": -104.8455},
    {"state": "Nuevo León", "country": "MX", "lat": 25.6866, "lon": -100.3161},
    {"state": "Oaxaca", "country": "MX", "lat": 17.0594, "lon": -96.7216},
    {"state": "Puebla", "country": "MX", "lat": 19.0414, "lon": -98.2063},
    {"state": "Querétaro", "country": "MX", "lat": 20.5888, "lon": -100.3899},
    {"state": "Quintana Roo", "country": "MX", "lat": 18.5100, "lon": -88.3030},
    {"state": "San Luis Potosí", "country": "MX", "lat": 22.1565, "lon": -100.9855},
    {"state": "Sinaloa", "country": "MX", "lat": 24.8091, "lon": -107.3940},
    {"state": "Sonora", "country": "MX", "lat": 29.0729, "lon": -110.9559},
    {"state": "Tabasco", "country": "MX", "lat": 17.9892, "lon": -92.9475},
    {"state": "Tamaulipas", "country": "MX", "lat": 23.7417, "lon": -99.1450},
    {"state": "Tlaxcala", "country": "MX", "lat": 19.3139, "lon": -98.2416},
    {"state": "Veracruz", "country": "MX", "lat": 19.1738, "lon": -96.1342},
    {"state": "Yucatán", "country": "MX", "lat": 20.9674, "lon": -89.5926},
    {"state": "Zacatecas", "country": "MX", "lat": 22.7709, "lon": -102.5832},
]

def update_weather():
    """
    Güncel hava durumu verilerini çeker ve DB'ye kaydeder.
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    
    for state in states:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={state['lat']}&lon={state['lon']}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
        response = requests.get(url).json()
        
        # API yanıtından verileri çek
        temp = response['main']['temp']
        feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']
        pressure = response['main']['pressure']
        weather_main = response['weather'][0]['main']
        weather_desc = response['weather'][0]['description']
        wind_speed = response['wind']['speed']
        cloudiness = response['clouds']['all']
        rain_1h = response.get('rain', {}).get('1h', 0.0)
        last_updated = datetime.utcfromtimestamp(response['dt'])
        
        # DB’ye ekle / güncelle
        cursor.execute("""
            INSERT INTO weather
            (state, country, lat, lon, temp, feels_like, humidity, pressure, weather_main, weather_desc, wind_speed, cloudiness, rain_1h, last_updated)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE 
                temp=%s, feels_like=%s, humidity=%s, pressure=%s, weather_main=%s, weather_desc=%s, wind_speed=%s, cloudiness=%s, rain_1h=%s, last_updated=%s
        """, (
            state['state'], state['country'], state['lat'], state['lon'],
            temp, feels_like, humidity, pressure, weather_main, weather_desc,
            wind_speed, cloudiness, rain_1h, last_updated,
            temp, feels_like, humidity, pressure, weather_main, weather_desc,
            wind_speed, cloudiness, rain_1h, last_updated
        ))
        conn.commit()
        time.sleep(1)  # API rate limit için

    close_connection(conn, cursor)

# --------------------------
# MAIN BLOĞU
# --------------------------
if __name__ == "__main__":
    print("Weather update başlıyor...")
    update_weather()
    print("Weather update tamamlandı!")
