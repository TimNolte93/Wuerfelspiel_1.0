import random
import json
import os
from datetime import datetime

EXTENSION = ".json"

def validiere_anzahl():
    while True:
        eingabe = input("\nWie viele Personen spielen mit? (1-99): ")
        if eingabe.isdigit():
            anzahl = int(eingabe)
            if 1 <= anzahl <= 99:
                return anzahl
        print("Ungültige Eingabe! Bitte eine Zahl zwischen 1 und 99 eingeben.")

def validiere_runden():
    while True:
        eingabe = input("Wie viele Runden sollen gespielt werden? (1-100): ")
        if eingabe.isdigit():
            runden = int(eingabe)
            if 1 <= runden <= 100:
                return runden
        print("Bitte gib eine Rundenzahl zwischen 1 und 100 ein.")

def validiere_name(index):
    while True:
        name = input(f"Name für Spieler*in {index}: ").strip()
        if name.isalpha():
            return name
        print("Ungültiger Name! Nur Buchstaben erlaubt.")

def hole_spielstaende():
    return sorted([f for f in os.listdir('.') if f.endswith(EXTENSION) and f.startswith('save_')], reverse=True)

def lade_spielstand():
    dateien = hole_spielstaende()
    print("\n---Verfügbare Spielstände ---")
    print("0: Neues Spiel starten")
    for i, datei in enumerate(dateien, 1):
        print(f"{i}: {datei}")
    
    wahl = input("\nWelche Nummer laden? (Enter für Neues Spiel): ")
    
    if not wahl or wahl == '0':
        anzahl = validiere_anzahl()
        runden_limit = validiere_runden() # Neu: Rundenlimit beim Start festlegen
        spieler = {}
        for i in range(1, anzahl + 1):
            name = validiere_name(i)
            spieler[name] = {"statistik": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, "gesamt": 0}
        return spieler, runden_limit, 1 # Spieler, Limit, Startrunde
    
    try:
        index = int(wahl) - 1
        with open(dateien[index], "r", encoding="utf-8") as f:
            daten = json.load(f)
            print(f"Spielstand {dateien[index]} geladen!")
            limit = daten.get("runden_limit", 10)
            aktuelle_runde = daten.get("aktuelle_runde", 1)
            return daten["spieler"], limit, aktuelle_runde
    except Exception as e:
        print(f"Fehler beim Laden: {e}")
        return {validiere_name(1): {"statistik": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, "gesamt": 0}}, 5, 1

def speichere_spielstand(spieler_daten, limit, runde):
    zeit = datetime.now().strftime("%Y%m%d_%H%M%S")
    dateiname = f"save_{zeit}{EXTENSION}"
    speicher_objekt = {
        "spieler": spieler_daten,
        "runden_limit": limit,
        "aktuelle_runde": runde
    }
    with open(dateiname, "w", encoding="utf-8") as f:
        json.dump(speicher_objekt, f, indent=4)
    print(f"Fortschritt gespeichert als: {dateiname}")

def wuerfel_spiel():
    spieler_daten, runden_limit, start_runde = lade_spielstand()
    print(f"\n---Das Spiel beginnt! Ziel: {runden_limit} Runden ---")
    for runde in range(start_runde, runden_limit + 1):
        print(f"\n============================")
        print(f"   SPIELRUNDE {runde} von {runden_limit}")
        print(f"============================")

        for name, daten in spieler_daten.items():
            print(f"\n>>> {name} ist an der Reihe!")
            input(f"    [Drücke ENTER zum Würfeln...]") 
            
            ergebnis = random.randint(1, 6)

            stats = {int(k): v for k, v in daten["statistik"].items()}
            stats[ergebnis] += 1
            daten["statistik"] = stats
            daten["gesamt"] += 1
            
            print(f"    Ergebnis: {ergebnis}")

        if runde < runden_limit:
            entscheidung = input("\nNächste Runde starten? (j) oder Spiel pausieren & speichern? (s): ").lower()
            if entscheidung == 's':
                speichere_spielstand(spieler_daten, runden_limit, runde + 1)
                return

    print("\n DAS SPIEL IST BEENDET!")
    speichere_spielstand(spieler_daten, runden_limit, runden_limit)

if __name__ == "__main__":
    wuerfel_spiel()