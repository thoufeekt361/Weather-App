import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from datetime import datetime
from weather import WeatherClient, WeatherAPIError

BG = "#0B1220"
SIDEBAR = "#111C2F"
PANEL = "#17243A"
PANEL_LIGHT = "#1D2D46"
HERO = "#193653"
TEXT = "#F4F7FB"
MUTED = "#A8B5C8"
ACCENT = "#55B7FF"
ORANGE = "#FFBE6B"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WeatherNow | Live Weather")
        self.root.geometry("1120x760")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG)
        self.city_var = tk.StringVar()
        self.status_var = tk.StringVar(
            value="Search for a city to see live weather."
        )
        self.city_title_var = tk.StringVar(value="Welcome to WeatherNow")
        self.temp_var = tk.StringVar(value="--°C")
        self.condition_var = tk.StringVar(value="Your weather, at a glance")
        self.feels_var = tk.StringVar(value="Feels like --°C")
        self.icon_var = tk.StringVar(value="☀")
        self.humidity_var = tk.StringVar(value="--%")
        self.wind_var = tk.StringVar(value="-- m/s")
        self.pressure_var = tk.StringVar(value="-- hPa")
        self.visibility_var = tk.StringVar(value="-- km")
        self.current_data = None
        self.forecast_data = []
        self.active_page = "Overview"
        self.nav_buttons = {}
        self.forecast_widgets = []
        self._build_styles()
        self._build_ui()
        self.show_page("Overview")

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TEntry",
            fieldbackground="#22334D",
            foreground=TEXT,
            insertcolor=TEXT,
            borderwidth=0,
            padding=10
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            background=ACCENT,
            foreground="#07111F",
            borderwidth=0,
            padding=(16, 10)
        )
        style.map(
            "TButton",
            background=[("active", "#8ACFFF"), ("disabled", "#52647A")]
        )

    def _label(self, parent, text, size=10, color=TEXT,
               weight="normal", **kwargs):
        bg = kwargs.pop("bg", parent.cget("bg"))
        return tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=color,
            font=("Segoe UI", size, weight),
            **kwargs
        )

    def _card(self, parent, bg=PANEL):
        return tk.Frame(
            parent,
            bg=bg,
            highlightthickness=1,
            highlightbackground="#263751"
        )

    def _build_ui(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(28, 34))
        self._label(brand, "◉  WEATHER", 17, ACCENT, "bold").pack(anchor="w")
        self._label(brand, "NOW", 17, TEXT, "bold").pack(
            anchor="w", padx=(27, 0)
        )
        self._label(
            self.sidebar, "YOUR WEATHER SPACE", 8, MUTED, "bold"
        ).pack(anchor="w", padx=22)
        nav = tk.Frame(self.sidebar, bg=SIDEBAR)
        nav.pack(fill="x", padx=14, pady=14)
        navigation = [
            ("Overview", "⌂"),
            ("Current Weather", "☼"),
            ("5-Day Forecast", "▦")
        ]
        for name, symbol in navigation:
            button = tk.Button(
                nav,
                text=f"{symbol}   {name}",
                command=lambda page=name: self.show_page(page),
                anchor="w",
                bg=SIDEBAR,
                fg=MUTED,
                activebackground="#20334D",
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                padx=12,
                pady=15,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2"
            )
            button.pack(fill="x", pady=4)
            self.nav_buttons[name] = button
        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=22, pady=24)
        self._label(bottom, "POWERED BY", 8, MUTED, "bold").pack(anchor="w")
        self._label(bottom, "OpenWeather API", 10, TEXT, "bold").pack(
            anchor="w", pady=(5, 0)
        )
        self._label(bottom, "Python • Tkinter", 9, MUTED).pack(
            anchor="w", pady=(3, 0)
        )
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self._build_header(self.main)
        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=28, pady=(4, 22))
        self.pages = {}
        self._build_overview_page()
        self._build_current_page()
        self._build_forecast_page()
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=BG)
        header.pack(fill="x", padx=28, pady=(24, 12))
        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side="left")
        self._label(title_box, "Good day!", 20, TEXT, "bold").pack(anchor="w")
        self._label(
            title_box,
            "Check the weather anywhere in the world.",
            9,
            MUTED
        ).pack(anchor="w", pady=(3, 0))
        search = tk.Frame(header, bg="#22334D", padx=5, pady=5)
        search.pack(side="right")
        entry = ttk.Entry(
            search,
            textvariable=self.city_var,
            width=23,
            font=("Segoe UI", 10)
        )
        entry.pack(side="left", padx=(4, 7))
        entry.bind("<Return>", lambda event: self.search_weather())
        ttk.Button(
            search, text="Search", command=self.search_weather
        ).pack(side="left")
        tk.Label(
            parent,
            textvariable=self.status_var,
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
            anchor="w"
        ).pack(fill="x", padx=29, pady=(0, 8))

    def _page_heading(self, parent, title, subtitle=None):
        self._label(parent, title.upper(), 10, MUTED, "bold").pack(
            anchor="w", pady=(4, 10)
        )
        if subtitle:
            self._label(parent, subtitle, 9, MUTED).pack(
                anchor="w", pady=(0, 14)
            )

    def _build_overview_page(self):
        page = tk.Frame(self.content, bg=BG)
        self.pages["Overview"] = page
        self._page_heading(page, "Weather Overview")
        hero = self._card(page, bg=HERO)
        hero.pack(fill="x")
        hero.configure(padx=24, pady=20)
        top = tk.Frame(hero, bg=HERO)
        top.pack(fill="x")
        left = tk.Frame(top, bg=HERO)
        left.pack(side="left", fill="both", expand=True)
        self._label(left, "CURRENT WEATHER", 9, "#B7D8F2", "bold").pack(
            anchor="w"
        )
        tk.Label(
            left, textvariable=self.city_title_var, bg=HERO, fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(9, 2))
        tk.Label(
            left, textvariable=self.condition_var, bg=HERO, fg="#D6E7F6",
            font=("Segoe UI", 11)
        ).pack(anchor="w")
        tk.Label(
            left, textvariable=self.feels_var, bg=HERO, fg="#B7D8F2",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(8, 0))

        right = tk.Frame(top, bg=HERO)
        right.pack(side="right", padx=10)
        tk.Label(
            right, textvariable=self.icon_var, bg=HERO, fg="#FFD27A",
            font=("Segoe UI Symbol", 42)
        ).pack()
        tk.Label(
            right, textvariable=self.temp_var, bg=HERO, fg=TEXT,
            font=("Segoe UI", 34, "bold")
        ).pack()
        self._label(page, "WEATHER DETAILS", 9, MUTED, "bold").pack(
            anchor="w", pady=(22, 10)
        )
        metrics = tk.Frame(page, bg=BG)
        metrics.pack(fill="x")
        self._metric_card(metrics, "HUMIDITY", self.humidity_var,
                          "Relative moisture")
        self._metric_card(metrics, "WIND SPEED", self.wind_var,
                          "Current wind")
        self._metric_card(metrics, "PRESSURE", self.pressure_var,
                          "Atmospheric pressure")
        self._metric_card(metrics, "VISIBILITY", self.visibility_var,
                          "Viewing distance")
        forecast_header = tk.Frame(page, bg=BG)
        forecast_header.pack(fill="x", pady=(22, 10))
        self._label(
            forecast_header, "5-DAY FORECAST", 9, MUTED, "bold"
        ).pack(side="left")
        self._label(
            forecast_header, "Daily outlook", 9, MUTED
        ).pack(side="right")
        preview = tk.Frame(page, bg=BG)
        preview.pack(fill="x")
        self.overview_forecast_widgets = []
        for i in range(5):
            self._make_forecast_card(preview, i, self.overview_forecast_widgets)
        self._label(
            page,
            "Select Current Weather or 5-Day Forecast from the sidebar "
            "to view more details.",
            9,
            MUTED
        ).pack(anchor="w", pady=(16, 0))

    def _build_current_page(self):
        page = tk.Frame(self.content, bg=BG)
        self.pages["Current Weather"] = page
        self._page_heading(
            page, "Current Weather",
            "Live weather conditions for your searched city."
        )
        hero = self._card(page, bg=HERO)
        hero.pack(fill="x", pady=(0, 18))
        hero.configure(padx=25, pady=24)
        top = tk.Frame(hero, bg=HERO)
        top.pack(fill="x")
        left = tk.Frame(top, bg=HERO)
        left.pack(side="left", fill="both", expand=True)
        self._label(left, "LIVE CONDITIONS", 9, "#B7D8F2", "bold").pack(
            anchor="w"
        )
        tk.Label(
            left, textvariable=self.city_title_var, bg=HERO, fg=TEXT,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", pady=(12, 4))
        tk.Label(
            left, textvariable=self.condition_var, bg=HERO, fg="#D6E7F6",
            font=("Segoe UI", 14)
        ).pack(anchor="w")
        tk.Label(
            left, textvariable=self.feels_var, bg=HERO, fg="#B7D8F2",
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(10, 0))
        right = tk.Frame(top, bg=HERO)
        right.pack(side="right", padx=15)
        tk.Label(
            right, textvariable=self.icon_var, bg=HERO, fg="#FFD27A",
            font=("Segoe UI Symbol", 54)
        ).pack()
        tk.Label(
            right, textvariable=self.temp_var, bg=HERO, fg=TEXT,
            font=("Segoe UI", 42, "bold")
        ).pack()
        self._label(page, "WEATHER INFORMATION", 10, MUTED, "bold").pack(
            anchor="w", pady=(4, 12)
        )
        details = tk.Frame(page, bg=BG)
        details.pack(fill="x")
        self._metric_card(details, "HUMIDITY", self.humidity_var,
                          "Relative humidity")
        self._metric_card(details, "WIND SPEED", self.wind_var,
                          "Meters per second")
        self._metric_card(details, "PRESSURE", self.pressure_var,
                          "Atmospheric pressure")
        self._metric_card(details, "VISIBILITY", self.visibility_var,
                          "Visibility distance")
        note = self._card(page, bg=PANEL_LIGHT)
        note.pack(fill="x", pady=(20, 0))
        note.configure(padx=18, pady=15)
        self._label(
            note,
            "Tip: Search another city using the search box above. "
            "This page will update with the latest available weather data.",
            9,
            MUTED,
            wraplength=760,
            justify="left"
        ).pack(anchor="w")

    def _build_forecast_page(self):
        page = tk.Frame(self.content, bg=BG)
        self.pages["5-Day Forecast"] = page
        self._page_heading(
            page, "5-Day Forecast",
            "Daily weather outlook based on the latest forecast data."
        )
        self.forecast_page_frame = tk.Frame(page, bg=BG)
        self.forecast_page_frame.pack(fill="x", pady=(4, 15))
        self.forecast_page_widgets = []
        for i in range(5):
            self._make_forecast_card(
                self.forecast_page_frame, i, self.forecast_page_widgets,
                large=True
            )
        self.forecast_city_label = self._label(
            page, "Search for a city to load its forecast.",
            10, MUTED
        )
        self.forecast_city_label.pack(anchor="w", pady=(10, 0))
        self._label(
            page,
            "Forecast information is provided by OpenWeatherMap.",
            9,
            MUTED
        ).pack(anchor="w", pady=(18, 0))

    def _metric_card(self, parent, title, variable, subtitle):
        card = self._card(parent)
        card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        card.configure(padx=14, pady=14)
        self._label(card, title, 8, MUTED, "bold").pack(anchor="w")
        tk.Label(
            card, textvariable=variable, bg=PANEL, fg=TEXT,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w", pady=(9, 3))
        self._label(card, subtitle, 8, MUTED).pack(anchor="w")

    def _make_forecast_card(self, parent, index, target_list, large=False):
        card = self._card(parent, bg=PANEL)
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0 if index == 0 else 8, 0),
            pady=3
        )
        card.configure(
            padx=12 if large else 9,
            pady=20 if large else 13
        )
        day = tk.Label(
            card, text="--", bg=PANEL, fg=MUTED,
            font=("Segoe UI", 10 if large else 9, "bold")
        )
        day.pack()
        icon = tk.Label(
            card, text="·", bg=PANEL, fg=ORANGE,
            font=("Segoe UI Symbol", 34 if large else 25)
        )
        icon.pack(pady=9)
        temp = tk.Label(
            card, text="--°C", bg=PANEL, fg=TEXT,
            font=("Segoe UI", 21 if large else 15, "bold")
        )
        temp.pack()
        desc = tk.Label(
            card, text="Forecast", bg=PANEL, fg=MUTED,
            font=("Segoe UI", 9 if large else 8),
            wraplength=125,
            justify="center"
        )
        desc.pack(pady=(7, 0))

        target_list.append((day, icon, temp, desc))

    def show_page(self, page_name):
        if page_name not in self.pages:
            return
        for frame in self.pages.values():
            frame.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)
        self.active_page = page_name
        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(bg="#20334D", fg=TEXT)
            else:
                button.configure(bg=SIDEBAR, fg=MUTED)
                
    def search_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showinfo("City Required", "Please enter a city name.")
            return
        self.status_var.set(f"Fetching live weather for {city} ...")
        Thread(
            target=self._load_weather,
            args=(city,),
            daemon=True
        ).start()

    def _load_weather(self, city):
        try:
            client = WeatherClient()
            current = client.get_current_weather(city)
            forecast = client.get_forecast(city)
            self.root.after(
                0,
                lambda c=current, f=forecast: self._update_dashboard(c, f)
            )
        except WeatherAPIError as error:
            message = str(error)
            self.root.after(0, lambda msg=message: self._show_error(msg))
        except Exception as error:
            message = f"Unexpected error: {error}"
            self.root.after(0, lambda msg=message: self._show_error(msg))

    def _show_error(self, message):
        self.status_var.set("Could not update weather.")
        messagebox.showerror("Weather Request Failed", message)

    def _update_dashboard(self, current, forecast):
        self.current_data = current
        self.forecast_data = forecast or []
        name = current.get("name", "Unknown city")
        country = current.get("sys", {}).get("country", "")
        main = current.get("main", {})
        weather = (current.get("weather") or [{}])[0]
        wind = current.get("wind", {})
        visibility = current.get("visibility")
        self.city_title_var.set(
            f"{name}, {country}" if country else name
        )
        self.temp_var.set(f"{round(main.get('temp', 0))}°C")
        self.condition_var.set(
            weather.get("description", "Weather information").title()
        )
        self.feels_var.set(
            f"Feels like {round(main.get('feels_like', main.get('temp', 0)))}°C"
        )
        self.icon_var.set(self._weather_symbol(weather.get("main", "")))
        self.humidity_var.set(f"{main.get('humidity', '--')}%")
        self.wind_var.set(f"{wind.get('speed', '--')} m/s")
        self.pressure_var.set(f"{main.get('pressure', '--')} hPa")
        if visibility is not None:
            self.visibility_var.set(f"{visibility / 1000:.1f} km")
        else:
            self.visibility_var.set("-- km")
        self._update_forecast_cards(
            self.overview_forecast_widgets, self.forecast_data
        )
        self._update_forecast_cards(
            self.forecast_page_widgets, self.forecast_data
        )
        self.forecast_city_label.configure(
            text=f"Forecast for {name}"
        )
        self.status_var.set(
            "Last updated: " + datetime.now().strftime("%d %b %Y, %I:%M %p")
        )

    def _update_forecast_cards(self, widgets, forecast):
        for i, card_widgets in enumerate(widgets):
            day_label, icon_label, temp_label, desc_label = card_widgets
            if i < len(forecast):
                item = forecast[i]
                day_label.config(text=item.get("date", "--"))
                icon_label.config(
                    text=self._weather_symbol(item.get("main", ""))
                )
                temp_label.config(
                    text=f"{round(item.get('temp', 0))}°C"
                )
                desc_label.config(
                    text=item.get("description", "Forecast").title()
                )
            else:
                day_label.config(text="--")
                icon_label.config(text="·")
                temp_label.config(text="--°C")
                desc_label.config(text="No data")
    @staticmethod
    def _weather_symbol(condition):
        symbols = {
            "Clear": "☀",
            "Clouds": "☁",
            "Rain": "☂",
            "Drizzle": "☂",
            "Thunderstorm": "ϟ",
            "Snow": "❄",
            "Mist": "≋",
            "Smoke": "≋",
            "Haze": "≋",
            "Dust": "≋",
            "Fog": "≋",
            "Squall": "≋",
            "Tornado": "↝"
        }
        return symbols.get(condition, "☼")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
