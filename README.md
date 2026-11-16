
# WeatherNow - Live Weather Dashboard

WeatherNow is a professional desktop weather application developed using Python and Tkinter.

## Features

- Search weather by city name
- Live temperature
- Weather conditions and icons
- Feels-like temperature
- Humidity
- Wind speed
- Atmospheric pressure
- Visibility
- Five-day weather forecast
- Error handling
- Secure API key management

## Technologies

- Python
- Tkinter
- Requests
- OpenWeather API
- Python-dotenv

## Installation

1. Clone the repository.

2. Install dependencies:

   py -m pip install -r requirements.txt

3. Create a .env file.

4. Add your OpenWeather API key:

   OPENWEATHER_KEY=your_api_key

5. Run the application:

   py app.py

## API Endpoints

Current Weather:
https://api.openweathermap.org/data/2.5/weather

Five-Day Forecast:
https://api.openweathermap.org/data/2.5/forecast

## Security

The API key is stored in a .env file.
The .env file is excluded from GitHub using .gitignore.

## Developer

Python Programming Internship Project - InternCircle
