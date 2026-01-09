import sys
import csv
import json
import pickle
from abc import ABC, abstractmethod

# --- Klasy bazowe i pochodne ---

class FileHandler(ABC):
    """Abstrakcyjna klasa bazowa dla obsługi plików."""

    @abstractmethod
    def read(self, filename):
        pass

    @abstractmethod
    def write(self, filename, data):
        pass


class CSVHandler(FileHandler):
    def read(self, filename):
        with open(filename, newline="", encoding="utf-8") as f:
            return [row for row in csv.reader(f)]

    def write(self, filename, data):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)


class JSONHandler(FileHandler):
    def read(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class TXTHandler(FileHandler):
    def read(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip().split(",") for line in f]

    def write(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            for row in data:
                f.write(",".join(map(str, row)) + "\n")


class PickleHandler(FileHandler):
    def read(self, filename):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def write(self, filename, data):
        with open(filename, "wb") as f:
            pickle.dump(data, f)


# --- Fabryka handlerów ---

def get_handler(filename):
    if filename.endswith(".csv"):
        return CSVHandler()
    elif filename.endswith(".json"):
        return JSONHandler()
    elif filename.endswith(".txt"):
        return TXTHandler()
    elif filename.endswith(".pickle"):
        return PickleHandler()
    else:
        raise ValueError("Nieobsługiwany format pliku.")


# --- Główna logika programu ---

def apply_changes(data, changes):
    for zmiana in changes:
        try:
            x, y, value = zmiana.split(",", 2)
            x, y = int(x), int(y)
            data[y][x] = value
        except Exception as e:
            print(f"Niepoprawna zmiana: {zmiana} ({e})")
    return data


def main():
    if len(sys.argv) < 3:
        print("Użycie: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> ... <zmiana_n>")
        sys.exit(1)

    plik_wejsciowy = sys.argv[1]
    plik_wyjsciowy = sys.argv[2]
    zmiany = sys.argv[3:]

    # Wczytaj dane
    handler_in = get_handler(plik_wejsciowy)
    data = handler_in.read(plik_wejsciowy)

    # Upewnij się, że dane są listą list (dla spójności)
    if isinstance(data, dict):
        # JSON może być listą lub dict – tu zakładamy listę list
        data = data["data"] if "data" in data else list(data.values())

    # Wprowadź zmiany
    data = apply_changes(data, zmiany)

    # Wyświetl w terminalu
    print("\nZmodyfikowana zawartość:")
    for row in data:
        print(",".join(map(str, row)))

    # Zapisz wynik
    handler_out = get_handler(plik_wyjsciowy)
    handler_out.write(plik_wyjsciowy, data)

    print(f"\nPlik zapisano jako: {plik_wyjsciowy}")


if __name__ == "__main__":
    main()