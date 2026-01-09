import urllib.request
import json
import os
from datetime import datetime, timedelta

# Plik cache
plik = "pogoda.json"

# Wczytaj dane z pliku, jeśli istnieje
if os.path.exists(plik):
    with open(plik, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

# Stolice województw z współrzędnymi
stolice = {
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

# Wybór miasta
print("Dostępne stolice województw:")
for miasto in stolice.keys():
    print(" -", miasto)

miasto = input("\nPodaj miasto: ").strip()
if miasto not in stolice:
    print("Nieznane miasto, używam domyślnie Kraków.")
    miasto = "Kraków"

latitude, longitude = stolice[miasto]

# Pobierz datę
data = input("Podaj datę (YYYY-mm-dd) lub Enter dla jutra: ").strip()
if not data:
    data = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# Klucz do cache
klucz = f"{miasto}_{data}"

# Jeśli wynik dla tej daty i miasta jest już w pliku – użyj go
if klucz in cache:
    wynik = cache[klucz]
    print(f"Wynik dla {miasto} w dniu {data}: {wynik}")
else:
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon"
        f"&start_date={data}&end_date={data}"
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

        cache[klucz] = wynik
        with open(plik, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)

        print(f"Wynik dla {miasto} w dniu {data}: {wynik}")

    except Exception as e:
        print("Błąd podczas pobierania danych:", e)