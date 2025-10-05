import requests
from datetime import datetime
from core.database import get_connection, close_connection
import time
from core.config import settings

OPENWEATHER_API_KEY = settings.OPENWEATHER_API_KEY 

# --------------------------
# Eyaletler / Bölgeler
# --------------------------
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
]

def update_forecast():
    """
    3 saatlik / 5 günlük tahmin verilerini çeker ve DB'ye kaydeder.
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    
    for state in states:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={state['lat']}&lon={state['lon']}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
            response = requests.get(url).json()
            
            for forecast in response['list']:
                forecast_time = datetime.utcfromtimestamp(forecast['dt'])
                temp = forecast['main']['temp']
                feels_like = forecast['main']['feels_like']
                temp_min = forecast['main']['temp_min']
                temp_max = forecast['main']['temp_max']
                pressure = forecast['main']['pressure']
                humidity = forecast['main']['humidity']
                weather_main = forecast['weather'][0]['main']
                weather_desc = forecast['weather'][0]['description']
                weather_icon = forecast['weather'][0]['icon']
                clouds = forecast['clouds']['all']
                wind_speed = forecast['wind']['speed']
                wind_deg = forecast['wind'].get('deg', 0)
                wind_gust = forecast['wind'].get('gust', 0.0)
                visibility = forecast.get('visibility', 0)
                pop = forecast.get('pop', 0.0)
                rain_3h = forecast.get('rain', {}).get('3h', 0.0)
                snow_3h = forecast.get('snow', {}).get('3h', 0.0)
                pod = 'd'  # default day/night placeholder
                
                cursor.execute("""
                    INSERT INTO weather_3h_forecast
                    (state, country, lat, lon, forecast_time, temp, feels_like, temp_min, temp_max, pressure, humidity,
                     weather_main, weather_description, weather_icon, clouds, wind_speed, wind_deg, wind_gust,
                     visibility, pop, rain_3h, snow_3h, pod)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE 
                        temp=%s, feels_like=%s, temp_min=%s, temp_max=%s, pressure=%s, humidity=%s,
                        weather_main=%s, weather_description=%s, weather_icon=%s, clouds=%s, wind_speed=%s,
                        wind_deg=%s, wind_gust=%s, visibility=%s, pop=%s, rain_3h=%s, snow_3h=%s
                """, (
                    state['state'], state['country'], state['lat'], state['lon'], forecast_time, temp, feels_like,
                    temp_min, temp_max, pressure, humidity, weather_main, weather_desc, weather_icon, clouds,
                    wind_speed, wind_deg, wind_gust, visibility, pop, rain_3h, snow_3h, pod,
                    temp, feels_like, temp_min, temp_max, pressure, humidity, weather_main, weather_desc,
                    weather_icon, clouds, wind_speed, wind_deg, wind_gust, visibility, pop, rain_3h, snow_3h
                ))
            conn.commit()
            time.sleep(1)

    close_connection(conn, cursor) 
if __name__ == "__main__":
    print("AQI update başlıyor...")
    update_forecast()
    print("AQI update tamamlandı!")