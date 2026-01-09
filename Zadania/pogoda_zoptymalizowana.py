Gimport urllib.request
import json
import os

class WeatherForecast:
    # słownik stolic województw z współrzędnymi
    capitals = {
        "Warszawa": (52.2297, 21.0122),
        "Kraków": (50.0647, 19.9450),
        "Łódź": (51.7592, 19.4560),
        "Wrocław": (51.1079, 17.0385),
        "Poznań": (52.4064, 16.9252),
        "Gdańsk": (54.3520, 18.6466),
        "Szczecin": (53.4285, 14.5528),
        "Bydgoszcz": (53.1235, 18.0084),
        "Lublin": (51.2465, 22.5684),
        "Białystok": (53.1325, 23.1688),
        "Katowice": (50.2649, 19.0238),
        "Kielce": (50.8661, 20.6286),
        "Olsztyn": (53.7784, 20.4801),
        "Opole": (50.6751, 17.9213),
        "Rzeszów": (50.0413, 21.9990),
        "Zielona Góra": (51.9390, 15.5050),
        "Gorzów Wielkopolski": (52.7368, 15.2288)
    }

    def __init__(self, city="Kraków", filename="pogoda.json"):
        if city not in self.capitals:
            raise ValueError(f"Nieznane miasto: {city}")
        self.city = city
        self.latitude, self.longitude = self.capitals[city]
        self.filename = filename
        self._data = {}
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4)

    def _fetch_from_api(self, date):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.latitude}&longitude={self.longitude}"
            f"&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon"
            f"&start_date={date}&end_date={date}"
        )
        try:
            with urllib.request.urlopen(url) as response:
                dane = json.load(response)

            rain_sum = None
            if "daily" in dane and "rain_sum" in dane["daily"]:
                rain_sum = dane["daily"]["rain_sum"][0]

            if rain_sum is None or rain_sum < 0:
                wynik = "Nie wiem"
            elif rain_sum == 0.0:
                wynik = "Nie będzie padać"
            else:
                wynik = "Będzie padać"

            self._data[f"{self.city}_{date}"] = wynik
            self._save()
            return wynik
        except Exception as e:
            return f"Błąd: {e}"

    # --- Magic methods ---
    def __getitem__(self, date):
        key = f"{self.city}_{date}"
        if key in self._data:
            return self._data[key]
        return self._fetch_from_api(date)

    def __setitem__(self, date, value):
        key = f"{self.city}_{date}"
        self._data[key] = value
        self._save()

    def __iter__(self):
        # zwraca wszystkie daty dla wybranego miasta
        return (k.split("_")[1] for k in self._data.keys() if k.startswith(self.city))

    def items(self):
        # zwraca generator (data, wynik) dla wybranego miasta
        return ((k.split("_")[1], v) for k, v in self._data.items() if k.startswith(self.city))


# ------------------ Przykładowe użycie ------------------
if __name__ == "__main__":
    from datetime import datetime, timedelta

    print("Dostępne stolice województw:")
    for miasto in WeatherForecast.capitals.keys():
        print(" -", miasto)

    city = input("\nWybierz miasto: ").strip()
    if city not in WeatherForecast.capitals:
        print("Nieznane miasto, używam domyślnie Kraków.")
        city = "Kraków"

    weather_forecast = WeatherForecast(city)

    data = input("Podaj datę (YYYY-mm-dd) lub Enter dla jutra: ").strip()
    if not data:
        data = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"\nPogoda dla {city} w dniu {data}: {weather_forecast[data]}")

    print("\nHistoria zapisanych wyników:")
    for d, wynik in weather_forecast.items():
        print(d, "->", wynik)