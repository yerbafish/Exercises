# Baza danych
uczniowie = []     # lista słowników: {"imie": ..., "klasa": ...}
nauczyciele = []   # lista słowników: {"imie": ..., "przedmiot": ..., "klasy": [...]}
wychowawcy = []    # lista słowników: {"imie": ..., "klasa": ...}

print("Dostępne komendy: utwórz, zarządzaj, koniec")

while True:
    komenda = input("\nPodaj komendę: ").strip().lower()

    if komenda == "utwórz":
        while True:
            print("\nOpcje tworzenia: uczeń, nauczyciel, wychowawca, koniec")
            opcja = input("Podaj opcję: ").strip().lower()

            if opcja == "uczeń":
                imie = input("Podaj imię i nazwisko ucznia: ").strip()
                klasa = input("Podaj klasę ucznia (np. 3C): ").strip()
                uczniowie.append({"imie": imie, "klasa": klasa})
                print("Dodano ucznia.")

            elif opcja == "nauczyciel":
                imie = input("Podaj imię i nazwisko nauczyciela: ").strip()
                przedmiot = input("Podaj przedmiot: ").strip()
                klasy = []
                print("Podaj klasy prowadzone przez nauczyciela (Enter kończy):")
                while True:
                    klasa = input()
                    if klasa == "":
                        break
                    klasy.append(klasa)
                nauczyciele.append({"imie": imie, "przedmiot": przedmiot, "klasy": klasy})
                print("Dodano nauczyciela.")

            elif opcja == "wychowawca":
                imie = input("Podaj imię i nazwisko wychowawcy: ").strip()
                klasa = input("Podaj klasę prowadzoną przez wychowawcę: ").strip()
                wychowawcy.append({"imie": imie, "klasa": klasa})
                print("Dodano wychowawcę.")

            elif opcja == "koniec":
                break
            else:
                print("Nieznana opcja.")

    elif komenda == "zarządzaj":
        while True:
            print("\nOpcje zarządzania: klasa, uczeń, nauczyciel, wychowawca, koniec")
            opcja = input("Podaj opcję: ").strip().lower()

            if opcja == "klasa":
                klasa = input("Podaj klasę: ").strip()
                print(f"\nUczniowie klasy {klasa}:")
                for uczen in uczniowie:
                    if uczen["klasa"] == klasa:
                        print(f" - {uczen['imie']}")
                for wych in wychowawcy:
                    if wych["klasa"] == klasa:
                        print(f"Wychowawca: {wych['imie']}")

            elif opcja == "uczeń":
                imie = input("Podaj imię i nazwisko ucznia: ").strip()
                # znajdź klasę ucznia
                klasa_ucznia = None
                for uczen in uczniowie:
                    if uczen["imie"] == imie:
                        klasa_ucznia = uczen["klasa"]
                        break
                if klasa_ucznia:
                    print(f"\nLekcje ucznia {imie} (klasa {klasa_ucznia}):")
                    for nauczyciel in nauczyciele:
                        if klasa_ucznia in nauczyciel["klasy"]:
                            print(f" - {nauczyciel['przedmiot']} (prowadzi {nauczyciel['imie']})")
                else:
                    print("Nie znaleziono ucznia.")

            elif opcja == "nauczyciel":
                imie = input("Podaj imię i nazwisko nauczyciela: ").strip()
                for nauczyciel in nauczyciele:
                    if nauczyciel["imie"] == imie:
                        print(f"\nNauczyciel {imie} prowadzi klasy: {', '.join(nauczyciel['klasy'])}")
                        break
                else:
                    print("Nie znaleziono nauczyciela.")

            elif opcja == "wychowawca":
                imie = input("Podaj imię i nazwisko wychowawcy: ").strip()
                for wych in wychowawcy:
                    if wych["imie"] == imie:
                        print(f"\nWychowawca {imie} prowadzi klasę {wych['klasa']}")
                        print("Uczniowie tej klasy:")
                        for uczen in uczniowie:
                            if uczen["klasa"] == wych["klasa"]:
                                print(f" - {uczen['imie']}")
                        break
                else:
                    print("Nie znaleziono wychowawcy.")

            elif opcja == "koniec":
                break
            else:
                print("Nieznana opcja.")

    elif komenda == "koniec":
        print("Zakończono działanie programu.")
        break

    else:
        print("Nieznana komenda.")