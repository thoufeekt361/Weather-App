
import os
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent / ".env")

# OpenWeatherMap API Base URL
BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPIError(Exception):
    """Custom error for weather API problems."""


class WeatherClient:

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_KEY", "").strip()

        if not self.api_key:
            raise WeatherAPIError(
                "API Key missing!\n"
                "Please add OPENWEATHER_KEY to your .env file."
            )

    def _request(self, endpoint, city):

        params = {
            "q": city.strip(),
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(
                f"{BASE_URL}/{endpoint}",
                params=params,
                timeout=10
            )

        except requests.exceptions.Timeout:
            raise WeatherAPIError(
                "Request timed out. Please try again."
            )

        except requests.exceptions.ConnectionError:
            raise WeatherAPIError(
                "Internet connection problem."
            )

        except requests.exceptions.RequestException as error:
            raise WeatherAPIError(
                f"Network error: {error}"
            )

        # Handle API response errors
        if response.status_code == 401:
            raise WeatherAPIError(
                "Invalid API Key. Please check your .env file. "
                "A new API key may take some time to activate."
            )

        elif response.status_code == 404:
            raise WeatherAPIError(
                f"City '{city}' not found. Please check the city name."
            )

        elif response.status_code == 429:
            raise WeatherAPIError(
                "API request limit reached. Try again later."
            )

        elif response.status_code != 200:
            raise WeatherAPIError(
                f"API Error: {response.status_code}"
            )

        try:
            return response.json()

        except ValueError:
            raise WeatherAPIError(
                "Invalid response received from weather server."
            )

    # Get current weather
    def get_current_weather(self, city):
        return self._request("weather", city)

    # Get 5-day forecast
    def get_forecast(self, city):

        data = self._request("forecast", city)

        entries = data.get("list", [])
        daily = {}

        for entry in entries:

            dt = datetime.fromtimestamp(entry["dt"])
            date_key = dt.date()

            # Select forecast closest to 12 PM
            distance = abs(dt.hour - 12)

            if (
                date_key not in daily
                or distance < daily[date_key]["distance"]
            ):

                weather = (entry.get("weather") or [{}])[0]

                daily[date_key] = {
                    "distance": distance,
                    "date": dt.strftime("%a"),
                    "temp": entry.get("main", {}).get("temp", 0),
                    "main": weather.get("main", ""),
                    "description": weather.get(
                        "description", "Forecast"
                    )
                }

        forecast = []

        for _, item in sorted(daily.items()):

            forecast.append({
                "date": item["date"],
                "temp": item["temp"],
                "main": item["main"],
                "description": item["description"]
            })

        return forecast[:5]
