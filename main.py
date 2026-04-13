import random

def wuerfel_spiel():
    print("--- Willkommen beim Würfelspiel! ---")
    
    while True:

        ergebnis = random.randint(1, 6)
        

        print(f"\nDu hast eine {ergebnis} gewürfelt!")
        

        nochmal = input("Möchtest du erneut würfeln? (j/n): ").lower()
        
        if nochmal != 'j':
            print("Danke fürs Spielen! Bis zum nächsten Mal.")
            break

if __name__ == "__main__":
    wuerfel_spiel()