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

def zeige_rangliste(spieler_daten):
    print("\n--- AKTUELLE RANGLISTE ---")    
    rangliste = []
    for name, daten in spieler_daten.items():
        punkte = sum(int(zahl) * anzahl for zahl, anzahl in daten["statistik"].items())
        rangliste.append((name, punkte))    
    rangliste.sort(key=lambda x: x[1], reverse=True)
    for platz, (name, punkte) in enumerate(rangliste, 1):
        print(f"Platz {platz}: {name} mit {punkte} Punkten")
    print("----------------------------")

def hole_spielstaende():
    return sorted([f for f in os.listdir('.') if f.endswith(EXTENSION) and f.startswith('save_')], reverse=True)

def lade_spielstand():
    dateien = hole_spielstaende()
    print("\n--- Verfügbare Spielstände ---")
    print("0: Neues Spiel starten")
    for i, datei in enumerate(dateien, 1):
        print(f"{i}: {datei}")
    
    wahl = input("\nWelche Nummer laden? (Enter für Neues Spiel): ")
    
    if not wahl or wahl == '0':
        anzahl = validiere_anzahl()
        runden_limit = validiere_runden()
        spieler_namen = [validiere_name(i) for i in range(1, anzahl + 1)]
        spieler_daten = {name: {"statistik": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}, "gesamt": 0} for name in spieler_namen}
        return spieler_daten, runden_limit, 1, 0 # spieler, limit, runde, start_spieler_index
    
    try:
        index = int(wahl) - 1
        with open(dateien[index], "r", encoding="utf-8") as f:
            daten = json.load(f)
            print(f"Spielstand {dateien[index]} geladen!")
            return daten["spieler"], daten["runden_limit"], daten["aktuelle_runde"], daten.get("naechster_spieler_index", 0)
    except:
        print("Fehler beim Laden. Starte neu.")
        return {}, 5, 1, 0

def speichere_spielstand(spieler_daten, limit, runde, spieler_index, automatisch=False):
    zeit = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = "auto_save" if automatisch else "save"
    dateiname = f"{prefix}_{zeit}{EXTENSION}"
    
    speicher_objekt = {
        "spieler": spieler_daten,
        "runden_limit": limit,
        "aktuelle_runde": runde,
        "naechster_spieler_index": spieler_index
    }
    
    with open(dateiname, "w", encoding="utf-8") as f:
        json.dump(speicher_objekt, f, indent=4)
    
    if automatisch:
        print(f"\n[System] Runde abgeschlossen. Automatischer Zwischenstand gespeichert: {dateiname}")
    else:
        print(f"Manuell gespeichert als: {dateiname}")

def wuerfel_spiel():
    spieler_daten, runden_limit, start_runde, start_spieler_idx = lade_spielstand()
    if not spieler_daten: return

    spieler_namen = list(spieler_daten.keys())

    for runde in range(start_runde, runden_limit + 1):
        if runde > 1 and start_spieler_idx == 0:
            zeige_rangliste(spieler_daten)

        print(f"\n============================")
        print(f"   SPIELRUNDE {runde} von {runden_limit}")
        print(f"============================")
        for i in range(start_spieler_idx, len(spieler_namen)):
            name = spieler_namen[i]
            print(f"\n>>> {name} ist an der Reihe!")
            
            aktion = input(f"    [ENTER zum Würfeln | 's' zum Speichern & Beenden]: ").lower()
            
            if aktion == 's':
                speichere_spielstand(spieler_daten, runden_limit, runde, i)
                return

            ergebnis = str(random.randint(1, 6))
            daten = spieler_daten[name]
            daten["statistik"][ergebnis] += 1
            daten["gesamt"] += 1
            print(f"   Ergebnis: {ergebnis}")

        start_spieler_idx = 0
        
        speichere_spielstand(spieler_daten, runden_limit, runde + 1, 0, automatisch=True)

    print("\nDAS SPIEL IST BEENDET!")
    zeige_rangliste(spieler_daten)
    speichere_spielstand(spieler_daten, runden_limit, runden_limit, 0)

if __name__ == "__main__":
    wuerfel_spiel()