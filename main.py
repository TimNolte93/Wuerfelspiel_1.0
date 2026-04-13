import random
import json

def speichere_json(daten):
    try:
        with open("spielstand.json", "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=4)
        print("\nSpielstand erfolgreich in 'spielstand.json' gespeichert!")
    except Exception as e:
        print(f"\n❌ Fehler beim Speichern: {e}")

def wuerfel_spiel():
    statistik = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    gesamt_anzahl = 0

    print("--- Würfelspiel mit JSON-Speicherung ---")
    
    while True:
        ergebnis = random.randint(1, 6)
        statistik[ergebnis] += 1
        gesamt_anzahl += 1
        
        print(f"\n Würfel: {ergebnis} | Gesamt: {gesamt_anzahl}")
        
        nochmal = input("Erneut würfeln? (j/n): ").lower()
        if nochmal != 'j':
            speicher_daten = {
                "gesamt_anzahl": gesamt_anzahl,
                "verteilung": statistik
            }
            speichere_json(speicher_daten)
            print("Auf Wiedersehen!")
            break

if __name__ == "__main__":
    wuerfel_spiel()