import sys
import csv

# Sprawdzenie liczby argumentów
if len(sys.argv) < 3:
    print("Użycie: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> ... <zmiana_n>")
    sys.exit(1)

plik_wejsciowy = sys.argv[1]
plik_wyjsciowy = sys.argv[2]
zmiany = sys.argv[3:]  # lista zmian w formacie "x,y,wartosc"

# Wczytanie pliku CSV
with open(plik_wejsciowy, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    dane = [row for row in reader]

# Wprowadzenie zmian
for zmiana in zmiany:
    try:
        x, y, wartosc = zmiana.split(",", 2)
        x = int(x)
        y = int(y)
        dane[y][x] = wartosc
    except Exception as e:
        print(f"Niepoprawna zmiana: {zmiana} ({e})")

# Wyświetlenie zmodyfikowanej zawartości w terminalu
print("\nZmodyfikowany plik CSV:")
for row in dane:
    print(",".join(row))

# Zapis do pliku wyjściowego
with open(plik_wyjsciowy, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(dane)

print(f"\nPlik zapisano jako: {plik_wyjsciowy}")