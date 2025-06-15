import time
import os
import sqlite3


# trida, ktera zpravuje databazi
class Databaze():

    # funkce, která načítá databázi seznam_pojistenych a kdyz ji nenajde tak jí vytvoří
    def __init__(self):
        self.conn = sqlite3.connect("seznam_pojistenych.db")
        self.cur = self.conn.cursor()

        # struktura databáze
        self.cur.execute('''CREATE TABLE IF NOT EXISTS seznam_pojistenych (
        id INTEGER PRIMARY KEY,
        jmeno TEXT,
        prijmeni TEXT,
        vek TEXT,
        telefonni_cislo TEXT)''')
        self.conn.commit()

    # funkce, která přidá nového pojištěnného do databáze
    def pridani_pojistence(self, jmeno, prijmeni, vek, telefonni_cislo):
        # přidá nového pojištěnce do seznamu
        self.cur.execute("""
        INSERT INTO seznam_pojistenych (jmeno, prijmeni, vek, telefonni_cislo)
        VALUES (?, ?, ?, ?)""", (jmeno, prijmeni, vek, telefonni_cislo))
        self.conn.commit()

    # funkce, která vypíše celou databázi
    def vypis(self):
        self.cur.execute("SELECT * FROM seznam_pojistenych")
        zaznamy = self.cur.fetchall()
        return zaznamy

    # funkce, která vyhledá v databázi pojištěnce podle jména a příjmení
    def vyhledani_pojistence(self, jmeno, prijmeni):
        self.cur.execute("SELECT * FROM seznam_pojistenych WHERE jmeno = ? AND prijmeni = ?", (jmeno, prijmeni))
        zaznamy = self.cur.fetchall()
        return zaznamy

    # funkce, ukončí spojení s databází
    def close(self):
        self.conn.close()

    def __str__(self):
        return f"Třida pro ukládání a výpis databáze pojištěných"


# hlavni trida aplikace, ktera komunikuje s uzivatelem a obsahuje v sobě rozdělovacé logiku
class Komunikator:

    def __init__(self):
        self.volba = None
        self.databaze = Databaze()  # inicializuje tridu databaze

    # vypis hlavniho menu a prijmuti volby uzivatele do promenne volba
    def menu(self):

        print("""-------------------------
EVIDENCE POJIŠTĚNÝCH
-------------------------

Vyberte si akci:
1 - přidat nového pojištěného
2 - vypsat všechny pojištěné
3 - vyhledat pojištěného
4 - ukončit program""")

        self.volba = input()
        print("")
        self.rozdelovaci_logika()  # spousti funcki ktera vybira,kterou funkci spustit na zaklade volby uzivatele

    # funkce, která spouští jednotlivé funkce podle volby v menu
    def rozdelovaci_logika(self):

        if self.volba == "1":
            self.pridani_pojistence()

        elif self.volba == "2":
            self.vypsani_pojistenych()

        elif self.volba == "3":
            self.vyhledani_pojisteneho()

        elif self.volba == "4":
            self.databaze.close()
            exit()

        else:
            print("Toto volbu neznám, zvolte znovu prosím")
            time.sleep(2)
            self.smycka()

    # funkce, která se spustí v okamžiku, kdy proměná která má být INT není uživatelem zadaná jako INT
    def kontrola_cisla(self, neni_cislo):
        print(f"{neni_cislo} musí být číslo")
        print()

        if neni_cislo == "Věk":
            self.zadani_vek()

        else:
            self.zadani_cislo()

    # funkce, která řídí přidání nového pojištěnce
    def pridani_pojistence(self):
        """" tato funkce ziskava informace o novem pojistenci od uzovatele a vyvolava prislusnou funkci
        z tridy Databaze, ktera je zapisuje do slovniku seznamu"""

        self.jmeno_prijmeni_funkce()  # spusti funkci ktera zpracovava jmeno a prijmeni
        self.zadani_vek()

    # funkce na zadání věku pojištěnce
    def zadani_vek(self):
        print("Zadejte věk pojištěného")

        self.vek = input().strip()  # načteme jako string a odstraníme bílé znak

        if self.vek.isdigit():  # zkontrolujeme, zda jsou tam jen číslice
            self.zadani_cislo()  # spustí funkci na zadání telefonního čísla

        else:
            self.kontrola_cisla("Věk")

    # funkce na zadání telefonního čísla pojištěnce
    def zadani_cislo(self):
        print("Zadejte telefonní číslo pojištěného")
        telefonni_cislo = input().strip()  # načteme jako string a odstraníme bílé znaky

        if telefonni_cislo.isdigit():  # zkontrolujeme, zda jsou tam jen číslice
            if len(telefonni_cislo) == 9:  # minimálně 9 číslic
                self.telefonni_cislo = telefonni_cislo
                self.databaze.pridani_pojistence(self.jmeno, self.prijmeni, self.vek, self.telefonni_cislo)
                print(f"Zadávám {self.jmeno} {self.prijmeni} {self.vek} {self.telefonni_cislo}")
                print("Data byla uložena\n")
                self.smycka()
            else:
                print("Číslo je příliš krátké nebo dlouhé\n")
                self.zadani_cislo()
        else:
            print("Telefonní číslo musí obsahovat pouze číslice\n")
            self.zadani_cislo()

    # funkce která přijímá od uživatele jméno a příjmení
    def jmeno_prijmeni_funkce(self):
        while True:
            print("Zadejte jméno pojištěného")
            self.jmeno = input().strip()
            if self.jmeno.isalpha():
                break
            else:
                print("Zadané jméno je chybné, zadejte prosím znovu\n")
                time.sleep(1)

        while True:
            print("Zadejte příjmení pojištěného")
            self.prijmeni = input().strip()
            if self.prijmeni.isalpha():
                break
            else:
                print("Zadané příjmení je chybné, zadejte prosím znovu\n")
                time.sleep(1)

    # funkce pro výpis všech pojištěných v databázi
    def vypsani_pojistenych(self):
        self.vypis = None
        self.vypis = self.databaze.vypis()

        self.vypis_seznamu("Databáze neobsahuje žádné pojištěnce")

    # funkce pro vyhledání pojištěnce v databázi
    def vyhledani_pojisteneho(self):
        self.vypis = None

        self.jmeno_prijmeni_funkce()  # odkaz na funkci, která si od užvatele nechá zadat jméno a příjmení pojištěnce
        self.vypis = self.databaze.vyhledani_pojistence(self.jmeno, self.prijmeni)

        self.vypis_seznamu("Zadaný pojištěnec není v databázi")

    # funkce na výpis zápisů z databáze
    def vypis_seznamu(self, navratova_veta):
        if not self.vypis:  # pokud je seznam prázdný
            print(navratova_veta)
            print()
        else:
            for zaznam in self.vypis:
                print(f"{zaznam[1]} {zaznam[2]} {zaznam[3]} {zaznam[4]}")
        self.smycka()

    # čeká na pokyn od uživatele a znovu spustí hlavní menu
    def smycka(self):
        print("Pokračujte stisknutím klávesy Enter")
        pokracovani = input()

        if os.name == "nt":
            os.system('cls')  # smaže obrazovku pro windows
        else:
            os.system("clear")  # smaže obrazovku pro mac a linux

        self.menu()

    def __str__(self):
        return f"Třída uživatelského rozhraní"


# inicializace třídy Komunikator
kom = Komunikator()
kom.menu()