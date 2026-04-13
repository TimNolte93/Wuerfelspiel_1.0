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

def validiere_name(index):
    while True:
        name = input(f"Name für Spieler*in {index}: ").strip()
        if name.isalpha():
            return name
        print("❌ Ungültiger Name! Nur Buchstaben (A-Z) erlaubt.")

def hole_spielstaende():
    return sorted([f for f in os.listdir('.') if f.endswith(EXTENSION) and f.startswith('save_')], reverse=True)

def lade_spielstand():
    dateien = hole_spielstaende()
    print("\n---Verfügbare Spielstände ---")
    print("0: Neues Spiel mit neuen Spielern")
    for i, datei in enumerate(dateien, 1):
        print(f"{i}: {datei}")
    
    wahl = input("\nWelche Nummer laden? (Enter für Neues Spiel): ")
    
    if not wahl or wahl == '0':
        anzahl = validiere_anzahl()
        spieler = {}
        for i in range(1, anzahl + 1):
            name = validiere_name(i)
            spieler[name] = {"statistik": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, "gesamt": 0}
        return spieler
    
    try:
        index = int(wahl) - 1
        with open(dateien[index], "r", encoding="utf-8") as f:
            daten = json.load(f)
            print(f"✅ Spielstand {dateien[index]} geladen!")
            return daten
    except Exception as e:
        print(f"Fehler beim Laden: {e}. Starte neues Spiel.")
        return {validiere_name(1): {"statistik": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, "gesamt": 0}}

def speichere_spielstand(spieler_daten):
    zeit = datetime.now().strftime("%Y%m%d_%H%M%S")
    dateiname = f"save_{zeit}{EXTENSION}"
    with open(dateiname, "w", encoding="utf-8") as f:
        json.dump(spieler_daten, f, indent=4)
    print(f"Fortschritt gespeichert als: {dateiname}")

def wuerfel_spiel():
    spieler_daten = lade_spielstand()
    print("\n---Das Spiel beginnt! ---")

    while True:
        for name, daten in spieler_daten.items():
            input(f"\n[{name}] - Bitte Enter zum Würfeln drücken...")
            ergebnis = random.randint(1, 6)

            stats = {int(k): v for k, v in daten["statistik"].items()}
            stats[ergebnis] += 1
            daten["statistik"] = stats
            daten["gesamt"] += 1
            
            print(f"{name} hat eine {ergebnis} gewürfelt!")
            print(f"Statistik {name}: {stats}")
        
        if input("\nNächste Runde für alle? (j/n): ").lower() != 'j':
            speichere_spielstand(spieler_daten)
            break

if __name__ == "__main__":
    wuerfel_spiel()