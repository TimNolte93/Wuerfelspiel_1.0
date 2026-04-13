import random

def wuerfel_spiel():
    statistik = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    gesamt_anzahl = 0

    print("--- Willkommen beim Würfelspiel mit Statistik! ---")
    
    while True:
        ergebnis = random.randint(1, 6)

        statistik[ergebnis] += 1
        gesamt_anzahl += 1
        
        print(f"\n🎲 Wurf-Ergebnis: {ergebnis}")
        
        print("-" * 30)
        print(f"Gesamtanzahl Würfe: {gesamt_anzahl}")
        print("Verteilung der Zahlen:")
        for zahl in range(1, 7):
            print(f"  Zahl {zahl}: {statistik[zahl]}x")
        print("-" * 30)

        nochmal = input("Möchtest du erneut würfeln? (j/n): ").lower()
        if nochmal != 'j':
            print("\nFinaler Stand der Statistik:")
            print(f"Insgesamt wurde {gesamt_anzahl} Mal gewürfelt.")
            print("Auf Wiedersehen!")
            break

if __name__ == "__main__":
    wuerfel_spiel()