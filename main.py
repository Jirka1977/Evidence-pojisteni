import time
import os
import sqlite3


class Databaze():
    # trida, ktera zpravuje databazi

    def __init__(self):
        self.conn = sqlite3.connect("seznam_pojistenych.db")
        self.cur = self.conn.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS seznam_pojistenych (
        id INTEGER PRIMARY KEY,
        jmeno_prijemni TEXT,
        prijmeni TEXT,
        vek REAL,
        telefonni_cislo REAL)''')
        self.conn.commit()

    def pridani_jmena(self, jmeno):
        # vlozi jmena a prijmeni do seznamu
        self.cur.execute("INSERT INTO seznam_pojistenych (jmeno_prijmeni) VALUES (?)", (jmeno,))
        self.conn.commit()

    def pridani_vek(self, vek):
        # vlozi vek do seznamu
        self.cur.execute("INSERT INTO seznam_pojistenych (vek) VALUES (?)", (vek,))
        self.conn.commit()

    def pridani_telefoni_cislo(self, cislo):
        # vlozi telefoni cislo do seznamu
        self.cur.execute("INSERT INTO seznam_pojistenych (telefonni_cislo) VALUES (?)", (cislo,))
        self.conn.commit()

    def vypis(self):
        return self.seznam_pojistenych

    def close(self):
        self.conn.close()

    def __str__(self):
        return f"Třida pro ukládání a výpis databáze pojištěných"


class Komunikator:
    # hlavni trida aplikace, ktera komunikuje s uzivatelem a ma v sobe logiku

    def __init__(self):
        self.volba = None
        self.databaze = Databaze()  # inicializuje tridu databaze

    def menu(self):
        # vypis hlavniho menu a prijmuti volby uzivatele do promenne volba

        print("""-------------------------
EVIDENCE POJIŠTĚNÝCH
-------------------------

Vyberte si akci:
1 - přidat nového pojištěného
2 - Vypsat všechny pojištěné
3 - vyhledat pojištěného
4 - ukončit program""")

        self.volba = input()
        print("")
        self.rozdelovaci_logika()  # spousti funcki ktera vybira,kterou funkci spustit na zaklade volby uzivatele

    def rozdelovaci_logika(self):
        # sousti jednotlive funckce v tride podle volby v menu

        if self.volba == "1":
            self.pridani_pojistence()

        elif self.volba == "2":
            self.vypsani_pojistenych()

        elif self.volba == "3":
            self.vyhledani_poijisteneho()

        elif self.volba == "4":
            exit()

        else:
            print("Toto volbu neznánm, zvolte znovu prosím")
            time.sleep(2)
            os.system("clear")
            self.menu()

    def pridani_pojistence(self):
        """" tato funkce ziskava informace o novem pojistenci od uzovatele a vyvolava prislusne funkce
        z tridy Databaze, ktera je zapisuje do slovniku seznamu"""

        self.jmeno_prijmeni_funkce("pridani pojistence")  # spusti funkci ktera zpracovava jmeno a prijmeni

        self.databaze.pridani_jmena(
            self.jmeno_prijmeni)  # prida promenou jmeno prijmeni funnkci pro zapis jmena z tridy databze

        print("Zadejte věk pojištěného")
        try:
            vek = int(input())
        except:
            print("Věk musí být číslo")
            print()
            self.pridani_pojistence()

        self.databaze.pridani_vek(vek)  # prida promenou vek funnkci pro zapis veku z tridy databze

        print("Zadejte telefoní číslo pojištěného")
        try:
            cislo = int(input())
        except:
            print("Telefonní číslo musí být číslo")
            print()
            self.pridani_pojistence()

        self.databaze.pridani_telefoni_cislo(
            cislo)  # prida promenou cislo prijmeni funnkci pro zapis cisla z tridy databze

        print("Data byla uložena")
        print()
        self.smycka()

    def kontorla_vyplneni(self, promenna, navratova_fce):
        # funkce která kontroluje vyplneni promenne

        if promenna.isalpha():
            pass

        else:
            print("Zadaná hodnota je chybně, zadej jí prosím znovu")
            print()
            time.sleep(1)

            if navratova_fce == "pridani pojistence":
                self.pridani_pojistence()
            else:
                self.jmeno_prijmeni_funkce()

    def jmeno_prijmeni_funkce(self, navratova_fce=None):
        # funkce prijima od uzivatele jmeno a prijmeni a slucuje je do jedne promenne jmeno_prijmeni
        print("Zadejte jméno pojištěného")
        jmeno = input()

        self.kontorla_vyplneni(jmeno, navratova_fce)  # spusti funkci na kontrolu vyplneni

        print("Zadejte příjmení pojištěného")
        prijmeni = input()

        self.kontorla_vyplneni(prijmeni, navratova_fce)  # spusti funkci na kontrolu vyplneni

        self.jmeno_prijmeni = jmeno + " " + prijmeni

    def vypsani_pojistenych(self, index=None):
        """ funkce ktera iteruje pres jednotlive seznamy ve slovniku a vypisuje je. Pokud je pri folani funkce zadana
        hodnota indexu vypise funkce pouze tuto polozky ze vsech seznamu ve slovniku"""

        self.prijmuti_databaze()

        if index is None:  # pokud neni zadan index urcuje rozmezi iterace pocet polozek ve slovniku
            od = 0
            do = self.pocet_pojistenych

        else:  # pokud je zadany index pri volani funkce zada rozmezi itarace pouze pro tento index
            od = index
            do = index + 1

        for pojistenec in range(od, do):  # itera pres polozky ve slovnicich
            print(self.seznam_pojistenych["jmeno"][pojistenec] + " ", end="")
            print(self.seznam_pojistenych["vek"][pojistenec] + " ", end="")
            print(self.seznam_pojistenych["telefoni cislo"][pojistenec])

        self.smycka()

    def prijmuti_databaze(self):
        # funkce, ktera nacita databazi ze tridy databze a pocita, kolik polozek je v seznamu "jmeno" a tudiz celkem
        self.seznam_pojistenych = self.databaze.vypis()
        self.pocet_pojistenych = len(self.seznam_pojistenych["jmeno"])

    def vyhledani_poijisteneho(self):
        # funkce ktera zkousi zda je zadane jmeno a prijmeni uz v databazi obsazeno a zjistuje na ktere pozici je v seznamu "jmeno"

        self.jmeno_prijmeni_funkce()
        self.prijmuti_databaze()

        try:
            pozice_v_seznamu = self.seznam_pojistenych["jmeno"].index(self.jmeno_prijmeni)
            self.vypsani_pojistenych(pozice_v_seznamu)
        except:
            print("Zadané jméno není v seznamu")

        self.smycka()

    def smycka(self):
        # ceka na pokyn od uzivatele a znovu spusti funkci hlavniho menu
        print("Pokračujte stisknutím klávesy Enter")
        pokracovani = input()

        os.system("clear")
        self.menu()

    def __str__(self):
        return f"Třída uživatelského rozhraní"


kom = Komunikator()
kom.menu()
