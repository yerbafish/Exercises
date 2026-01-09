from datetime import datetime

# Pobieranie danych od użytkownika
imie_odbiorcy = input("Podaj imię odbiorcy: ")
rok_urodzenia = int(input("Podaj rok urodzenia odbiorcy: "))
wiadomosc = input("Podaj spersonalizowaną wiadomość: ")
imie_nadawcy = input("Podaj swoje imię: ")

# Obliczanie wieku
obecny_rok = datetime.now().year
wiek = obecny_rok - rok_urodzenia

# Generowanie kartki
print(f"{imie_odbiorcy}, wszystkiego najlepszego z okazji {wiek} urodzin!")
print(f"\n{wiadomosc}\n")
print(f"{imie_nadawcy}")