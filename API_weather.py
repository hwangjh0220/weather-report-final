# GitHub: https://github.com/hwangjh0220/weather-report-final
import requests
from datetime import datetime

WMO_WEATHER_CODES = {
    0: "맑음", 1: "대체로 맑음", 2: "주로 맑음", 3: "흐림",
    45: "안개", 61: "약한 비", 63: "보통 비", 71: "약한 눈",
}

def get_weather_desc(code):
    return WMO_WEATHER_CODES.get(code, "정보 없음")

def fetch_weather_data(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Asia/Tokyo",
        "forecast_days": 3,
    }
    return requests.get(url, params=params).json()

def format_forecast_display(data, city="서울"):
    hourly = data.get("hourly", {})
    daily = data.get("daily", {})
    day_labels = ["오늘", "내일", "모레"]
    
    print("\n" + "=" * 50)
    print(f"[{city} 지역 날씨 리포트 (3일 예보)]")
    print("=" * 50)

    for i in range(3):
        label = day_labels[i]
        date_str = daily["time"][i]
        min_temp = round(daily["temperature_2m_min"][i])
        max_temp = round(daily["temperature_2m_max"][i])
        
        print(f"\n🗓️  {label} ({date_str})")
        print("-" * 45)
        print(f"  🌅 오전 06:00: {hourly['temperature_2m'][i*24+6]}℃ / {get_weather_desc(hourly['weather_code'][i*24+6])}")
        print(f"  ☀️  오후 15:00: {hourly['temperature_2m'][i*24+15]}℃ / {get_weather_desc(hourly['weather_code'][i*24+15])}")
        print(f"  🏷️  일일 기온: 최저 {min_temp}℃ / 최고 {max_temp}℃")

if __name__ == "__main__":
    data = fetch_weather_data(37.5665, 126.9780)
    format_forecast_display(data)