konto = 0
magazyn = {}   # {produkt: {"cena": cena, "ilosc": ilosc}}
historia = []  # lista zapisanych operacji

print("\nDostępne komendy:")
print("saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")

while True:
    komenda = input("\nPodaj komendę: ").strip().lower()

    if komenda == "saldo":
        try:
            kwota = float(input("Podaj kwotę (może być dodatnia lub ujemna): "))
            konto += kwota
            historia.append(("saldo", kwota))
        except ValueError:
            print("Niepoprawna kwota.")

    elif komenda == "sprzedaż":
        produkt = input("Podaj nazwę produktu: ").strip()
        try:
            cena = float(input("Podaj cenę sprzedaży: "))
            ilosc = int(input("Podaj liczbę sztuk: "))
        except ValueError:
            print("Niepoprawne dane.")
            continue

        if produkt not in magazyn or magazyn[produkt]["ilosc"] < ilosc:
            print("Brak wystarczającej ilości produktu w magazynie.")
        else:
            magazyn[produkt]["ilosc"] -= ilosc
            konto += cena * ilosc
            historia.append(("sprzedaż", produkt, cena, ilosc))

    elif komenda == "zakup":
        produkt = input("Podaj nazwę produktu: ").strip()
        try:
            cena = float(input("Podaj cenę zakupu: "))
            ilosc = int(input("Podaj liczbę sztuk: "))
        except ValueError:
            print("Niepoprawne dane.")
            continue

        if cena <= 0 or ilosc <= 0:
            print("Cena i ilość muszą być dodatnie.")
            continue

        koszt = cena * ilosc
        if konto - koszt < 0:
            print("Nie można wykonać zakupu – saldo byłoby ujemne.")
        else:
            konto -= koszt
            if produkt in magazyn:
                magazyn[produkt]["ilosc"] += ilosc
                magazyn[produkt]["cena"] = cena
            else:
                magazyn[produkt] = {"cena": cena, "ilosc": ilosc}
            historia.append(("zakup", produkt, cena, ilosc))

    elif komenda == "konto":
        print(f"Stan konta: {konto:.2f} zł")

    elif komenda == "lista":
        if not magazyn:
            print("Magazyn jest pusty.")
        else:
            print("Stan magazynu:")
            for produkt, dane in magazyn.items():
                print(f"{produkt}: {dane['ilosc']} szt., cena {dane['cena']} zł")

    elif komenda == "magazyn":
        produkt = input("Podaj nazwę produktu: ").strip()
        if produkt in magazyn:
            dane = magazyn[produkt]
            print(f"{produkt}: {dane['ilosc']} szt., cena {dane['cena']} zł")
        else:
            print("Produkt nie znajduje się w magazynie.")

    elif komenda == "przegląd":
        try:
            od = input("Podaj indeks początkowy (lub Enter): ").strip()
            do = input("Podaj indeks końcowy (lub Enter): ").strip()

            od = int(od) if od else 0
            do = int(do) if do else len(historia)

            if od < 0 or do > len(historia):
                print(f"Zakres poza granicami. Liczba zapisanych komend: {len(historia)}")
            else:
                for i, akcja in enumerate(historia[od:do], start=od):
                    print(f"{i}: {akcja}")
        except ValueError:
            print("Niepoprawne dane zakresu.")

    elif komenda == "koniec":
        print("Zakończono działanie programu.")
        break

    else:
        print("Nieznana komenda.")

    print("\nDostępne komendy:")
    print("saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")