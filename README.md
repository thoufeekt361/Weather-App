# 🌦️ WeatherNow – Live Weather Dashboard

A professional desktop weather application built using **Python and Tkinter**, integrated with the OpenWeatherMap API to provide real-time weather information and a 5-day weather forecast for cities around the world.

WeatherNow features a modern dark-themed dashboard with interactive navigation, city search, current weather information, and detailed weather forecasts.

---

## 📌 Project Overview

WeatherNow is a Python-based desktop application designed to help users quickly access weather information for any supported city.

The application retrieves live weather data through the OpenWeatherMap API and displays it in an easy-to-use graphical interface built entirely with Python Tkinter.

## ✨ Features

- 🌍 **Global City Search** – Search weather information for cities around the world.
- 🌡️ **Current Weather** – View real-time temperature and weather conditions.
- ☀️ **Weather Icons** – Visual representation of different weather conditions.
- 💧 **Humidity Information** – Check the current humidity percentage.
- 💨 **Wind Speed** – View current wind speed.
- 🌡️ **Atmospheric Pressure** – Display atmospheric pressure in hPa.
- 👁️ **Visibility** – Check visibility distance in kilometers.
- 📅 **5-Day Weather Forecast** – View daily temperature, weather conditions, and icons.
- 📊 **Interactive Dashboard** – Navigate between Overview, Current Weather, and 5-Day Forecast.
- ⚠️ **Error Handling** – Handles invalid cities, API errors, and network problems.
- 🎨 **Modern UI** – Professional dark-themed interface using Tkinter.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| Tkinter | Desktop graphical user interface |
| OpenWeatherMap API | Live weather data |
| Requests | HTTP API communication |
| python-dotenv | Environment variable management |
| Threading | Background API requests |

## 📁 Project Structure

```text
WeatherNow/
│
├── app.py                  # Main Tkinter application
├── weather.py              # Weather API integration
├── requirements.txt        # Python dependencies
├── .env                    # API key configuration
├── .env.example            # Environment variable template
├── .gitignore              # Git ignored files
└── README.md               # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone [YOUR_GITHUB_REPOSITORY_URL](https://github.com/thoufeekt361/Weather-App)
```

Navigate to the project folder:

```bash
cd WeatherNow
```

### 2. Install Dependencies

Make sure Python 3.12 or a compatible Python version is installed.

Install the required packages:

```bash
py -3.12 -m pip install -r requirements.txt
```

Alternatively:

```bash
py -3.12 -m pip install requests python-dotenv
```

### 3. Get an OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api).
2. Create an account or sign in.
3. Navigate to the API Keys section.
4. Generate or copy your API key.

### 4. Configure Environment Variables

Create a `.env` file in the root project directory.

Add the following:

```env
OPENWEATHER_KEY=your_actual_api_key
```

Replace `your_actual_api_key` with your OpenWeatherMap API key.

**Important:** Never upload your `.env` file or expose your API key publicly.

### 5. Run the Application

Execute the following command:

```bash
py -3.12 app.py
```

The WeatherNow desktop dashboard will open.

## 🖥️ Application Navigation

WeatherNow provides three main sections:

### 1. Overview
Displays a summary of current weather conditions, important weather measurements, and a 5-day forecast preview.

### 2. Current Weather
Displays detailed live weather information, including:
- City and country
- Current temperature
- Weather condition
- Feels-like temperature
- Humidity
- Wind speed
- Atmospheric pressure
- Visibility

### 3. 5-Day Forecast
Displays daily weather information, including:
- Day of the week
- Weather icon
- Forecast temperature
- Weather condition

## 🌐 API Integration

WeatherNow uses the OpenWeatherMap API to retrieve weather information.

**Current Weather Endpoint:**

```text
https://api.openweathermap.org/data/2.5/weather
```

**5-Day Forecast Endpoint:**

```text
https://api.openweathermap.org/data/2.5/forecast
```

The application uses metric units for temperature and weather measurements.

## 🧪 Testing

The application can be tested using different city names.

| Test Case | Expected Result |
|---|---|
| Search Kochi | Display Kochi weather |
| Search London | Display London weather |
| Search Dubai | Display Dubai weather |
| Search Tokyo | Display Tokyo weather |
| Empty city search | Show city-required message |
| Invalid city name | Display city-not-found error |
| Invalid API key | Display API authentication error |
| No internet connection | Display connection error |

## 🔒 Security

- API keys are stored in environment variables.
- The `.env` file is excluded from Git using `.gitignore`.
- The `.env.example` file provides a configuration template.
- API credentials should never be committed to a public repository.

## 🚀 Future Enhancements

- Weather maps and location-based weather.
- Hourly weather forecast.
- Sunrise and sunset information.
- Temperature charts and weather trends.
- Improved weather animations.
- Celsius and Fahrenheit unit selection.

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Python application development.
- Building desktop applications using Tkinter.
- Integrating third-party REST APIs.
- Handling JSON responses.
- Managing environment variables securely.
- Exception handling and error management.
- Using threading for background API requests.
- Designing a professional graphical user interface.

## 👨‍💻 Developer

**Thoufeek T.**

B.Tech Computer Science and Engineering Student

**Project:** WeatherNow – Live Weather Dashboard

**Internship Domain:** Python Programming

---

## 📜 License

This project is created for educational and internship purposes. You are welcome to explore and learn from the source code.

---

⭐ If you find this project useful, consider giving the repository a star!
