import os
import json

class Manager:
    def __init__(self, filename="baza.txt"):
        self.filename = filename
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                dane = json.load(f)
                self.konto = dane["konto"]
                self.magazyn = dane["magazyn"]
                self.historia = dane["historia"]
        else:
            self.konto = 0
            self.magazyn = {}
            self.historia = []

        # mapa komend
        self.commands = {}

    def assign(self, name, func):
        """Przypisz funkcję do komendy"""
        self.commands[name] = func

    def execute(self, name):
        """Wykonaj komendę"""
        if name in self.commands:
            self.commands[name]()
        else:
            print("Nieznana komenda.")

    # --- Implementacje komend ---
    def saldo(self):
        try:
            kwota = float(input("Podaj kwotę (może być dodatnia lub ujemna): "))
            self.konto += kwota
            self.historia.append(("saldo", kwota))
        except ValueError:
            print("Niepoprawna kwota.")

    def sprzedaz(self):
        produkt = input("Podaj nazwę produktu: ").strip()
        try:
            cena = float(input("Podaj cenę sprzedaży: "))
            ilosc = int(input("Podaj liczbę sztuk: "))
        except ValueError:
            print("Niepoprawne dane.")
            return

        if produkt not in self.magazyn or self.magazyn[produkt]["ilosc"] < ilosc:
            print("Brak wystarczającej ilości produktu w magazynie.")
        else:
            self.magazyn[produkt]["ilosc"] -= ilosc
            self.konto += cena * ilosc
            self.historia.append(("sprzedaż", produkt, cena, ilosc))

    def zakup(self):
        produkt = input("Podaj nazwę produktu: ").strip()
        try:
            cena = float(input("Podaj cenę zakupu: "))
            ilosc = int(input("Podaj liczbę sztuk: "))
        except ValueError:
            print("Niepoprawne dane.")
            return

        if cena <= 0 or ilosc <= 0:
            print("Cena i ilość muszą być dodatnie.")
            return

        koszt = cena * ilosc
        if self.konto - koszt < 0:
            print("Nie można wykonać zakupu – saldo byłoby ujemne.")
        else:
            self.konto -= koszt
            if produkt in self.magazyn:
                self.magazyn[produkt]["ilosc"] += ilosc
                self.magazyn[produkt]["cena"] = cena
            else:
                self.magazyn[produkt] = {"cena": cena, "ilosc": ilosc}
            self.historia.append(("zakup", produkt, cena, ilosc))

    def konto_cmd(self):
        print(f"Stan konta: {self.konto:.2f} zł")

    def lista(self):
        if not self.magazyn:
            print("Magazyn jest pusty.")
        else:
            print("Stan magazynu:")
            for produkt, dane in self.magazyn.items():
                print(f"{produkt}: {dane['ilosc']} szt., cena {dane['cena']} zł")

    def magazyn_cmd(self):
        produkt = input("Podaj nazwę produktu: ").strip()
        if produkt in self.magazyn:
            dane = self.magazyn[produkt]
            print(f"{produkt}: {dane['ilosc']} szt., cena {dane['cena']} zł")
        else:
            print("Produkt nie znajduje się w magazynie.")

    def przeglad(self):
        try:
            od = input("Podaj indeks początkowy (lub Enter): ").strip()
            do = input("Podaj indeks końcowy (lub Enter): ").strip()

            od = int(od) if od else 0
            do = int(do) if do else len(self.historia)

            if od < 0 or do > len(self.historia):
                print(f"Zakres poza granicami. Liczba zapisanych komend: {len(self.historia)}")
            else:
                for i, akcja in enumerate(self.historia[od:do], start=od):
                    print(f"{i}: {akcja}")
        except ValueError:
            print("Niepoprawne dane zakresu.")

    def koniec(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump({"konto": self.konto, "magazyn": self.magazyn, "historia": self.historia}, f, ensure_ascii=False, indent=4)
        print("Stan konta, magazyn i historia zapisane do pliku. Zakończono działanie programu.")
        exit()


# --- Uruchomienie programu ---
if __name__ == "__main__":
    manager = Manager()

    # przypisanie komend
    manager.assign("saldo", manager.saldo)
    manager.assign("sprzedaż", manager.sprzedaz)
    manager.assign("zakup", manager.zakup)
    manager.assign("konto", manager.konto_cmd)
    manager.assign("lista", manager.lista)
    manager.assign("magazyn", manager.magazyn_cmd)
    manager.assign("przegląd", manager.przeglad)
    manager.assign("koniec", manager.koniec)

    print("\nDostępne komendy:")
    print("saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")

    while True:
        komenda = input("\nPodaj komendę: ").strip().lower()
        manager.execute(komenda)

        print("\nDostępne komendy:")
        print("saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")