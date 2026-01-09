# Pobranie liczby elementów
try:
    liczba_elementow = int(input("Ile elementów chcesz wysłać? "))
except ValueError:
    print("Podano niepoprawną liczbę.")
    exit()

paczki = []          # lista paczek (każda paczka to lista wag)
aktualna_paczka = [] # paczka, do której aktualnie dodajemy
aktualna_waga = 0    # suma wag w bieżącej paczce

for i in range(liczba_elementow):
    try:
        waga = int(input(f"Podaj wagę elementu {i+1}: "))
    except ValueError:
        print("Podano niepoprawną wagę.")
        break

    # Sprawdzenie restrykcji
    if waga < 1 or waga > 10:
        print("Podano wagę spoza zakresu (1-10). Kończę dodawanie paczek.")
        break

    # Jeśli element zmieści się w bieżącej paczce
    if aktualna_waga + waga <= 20:
        aktualna_paczka.append(waga)
        aktualna_waga += waga
    else:
        # Zapisz bieżącą paczkę i rozpocznij nową
        paczki.append(aktualna_paczka)
        aktualna_paczka = [waga]
        aktualna_waga = waga

# Dodaj ostatnią paczkę, jeśli nie jest pusta
if aktualna_paczka:
    paczki.append(aktualna_paczka)

# Podsumowanie
liczba_paczek = len(paczki)
suma_kg = sum(sum(paczka) for paczka in paczki)
suma_pustych = liczba_paczek * 20 - suma_kg

# Znalezienie paczki z największą liczbą pustych kg
pustki = [20 - sum(paczka) for paczka in paczki]
max_pustki = max(pustki)
nr_paczki = pustki.index(max_pustki) + 1

# Wyświetlenie podsumowania
print("\n--- Podsumowanie ---")
print(f"Wysłano {liczba_paczek} paczkę/paczki:")
for idx, paczka in enumerate(paczki, start=1):
    print(f"  Paczka {idx}: {paczka} (suma {sum(paczka)} kg)")
print(f"Wysłano {suma_kg} kg")
print(f"Suma pustych kilogramów: {suma_pustych} kg")
print(f"Najwięcej pustych kilogramów ma paczka {nr_paczki} ({max_pustki} kg)")