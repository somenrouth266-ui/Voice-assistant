"""
Weather skill using the OpenWeatherMap free API.
Get a key at https://openweathermap.org/api and set WEATHER_API_KEY in config.py
or as an environment variable.
"""
import requests

import config


def get_weather(city: str = None) -> str:
    city = city or config.WEATHER_DEFAULT_CITY
    if not config.WEATHER_API_KEY:
        return "Weather isn't set up yet — add a WEATHER_API_KEY in config.py."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": config.WEATHER_API_KEY, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        desc = data["weather"][0]["description"]
        return f"It's {temp}°C in {city}, feels like {feels}°C, with {desc}."
    except requests.exceptions.HTTPError:
        return f"I couldn't find weather for '{city}'."
    except requests.exceptions.RequestException:
        return "I couldn't reach the weather service — check your internet connection."
