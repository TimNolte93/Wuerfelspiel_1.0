import random
import json
import os
from datetime import datetime 

def hole_spielstaende():
    dateien = [f for f in os.listdir('.') if f.endswith('.json') and f.startswith('save_')]
    return sorted(dateien, reverse=True) # Neueste zuerst

def lade_spielstand():
    dateien = hole_spielstaende()
    
    print("\n--- Verfügbare Spielstände ---")
    print("0: Neues Spiel starten")
    for i, datei in enumerate(dateien, 1):
        print(f"{i}: {datei}")
    
    wahl = input("\nWelchen Spielstand laden? (Nummer oder Enter für Neu): ")
    
    if not wahl or wahl == '0':
        print("Starte neues Spiel.")
        return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 0
    
    try:
        index = int(wahl) - 1
        gewaehlte_datei = dateien[index]
        with open(gewaehlte_datei, "r", encoding="utf-8") as f:
            daten = json.load(f)
            statistik = {int(k): v for k, v in daten["verteilung"].items()}
            print(f"--- Spielstand {gewaehlte_datei} geladen! ---")
            return statistik, daten["gesamt_anzahl"]
    except (ValueError, IndexError):
        print("Ungültige Wahl. Starte neues Spiel.")
        return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 0

def speichere_spielstand(statistik, gesamt):
    zeitstempel = datetime.now().strftime("%Y%m%d_%H%M%S")
    dateiname = f"save_{zeitstempel}.json"
    
    daten = {"gesamt_anzahl": gesamt, "verteilung": statistik}
    
    with open(dateiname, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4)
    print(f"\nSpielstand gespeichert als: {dateiname}")

def wuerfel_spiel():
    statistik, gesamt_anzahl = lade_spielstand()

    while True:
        ergebnis = random.randint(1, 6)
        statistik[ergebnis] += 1
        gesamt_anzahl += 1
        
        print(f"\nWürfel: {ergebnis} | Gesamt: {gesamt_anzahl}")
        print(f"Statistik: {statistik}")
        
        nochmal = input("Erneut würfeln? (j/n): ").lower()
        if nochmal != 'j':
            speichere_spielstand(statistik, gesamt_anzahl)
            break

if __name__ == "__main__":
    wuerfel_spiel()