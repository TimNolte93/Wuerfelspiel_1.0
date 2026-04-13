import random
import os
import yaml 

FILENAME = "spielstand.yaml"

def lade_spielstand():

    if not os.path.exists(FILENAME):
        print(f"--- Info: Keine Datei '{FILENAME}' gefunden. Neues Spiel beginnt bei 0. ---")
        return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 0
    
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            daten = yaml.safe_load(f)

            if not daten:
                return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 0

            statistik = {int(k): v for k, v in daten["verteilung"].items()}
            gesamt = daten["gesamt_anzahl"]
            
            print(f"--- Spielstand aus YAML geladen! (Bisherige Würfe: {gesamt}) ---")
            return statistik, gesamt
            
    except Exception as e:
        print(f"Fehler beim Laden der YAML-Datei: {e}")
        print("Starte mit leerem Spielstand.")
        return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 0

def speichere_spielstand(statistik, gesamt):

    daten = {
        "gesamt_anzahl": gesamt,
        "verteilung": statistik
    }
    
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            yaml.dump(daten, f, default_flow_style=False, sort_keys=True)
        print(f"\nFortschritt in '{FILENAME}' gespeichert. Bis zum nächsten Mal!")
    except Exception as e:
        print(f"\nFehler beim Speichern: {e}")

def wuerfel_spiel():
    # 1. Spielstand beim Start laden
    statistik, gesamt_anzahl = lade_spielstand()

    print("\n--- Willkommen beim Profi-Würfelspiel (YAML-Edition) ---")
    
    while True:
        ergebnis