import random
import os
import xml.etree.ElementTree as ET 
FILENAME = "spielstand.xml"

def lade_spielstand():
    """
    Lädt den Spielstand aus einer XML-Datei.
    Struktur: <Spielstand><Gesamt>X</Gesamt><Verteilung><Wurf zahl="1">X</Wurf>...</Verteilung></Spielstand>
    """
    if not os.path.exists(FILENAME):
        print(f"--- Info: '{FILENAME}' nicht gefunden. Neues Spiel startet bei 0. ---")
        return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 0
    
    try:
        tree = ET.parse(FILENAME)
        root = tree.getroot()

        gesamt = int(root.find("Gesamt").text)

        statistik = {}

        for wurf in root.find("Verteilung").findall("Wurf"):
            zahl = int(wurf.get("zahl"))
            anzahl = int(wurf.text)     
            statistik[zahl] = anzahl
            
        print(f"--- XML-Spielstand geladen! (Gesamt: {gesamt}) ---")
        return statistik, gesamt
        
    except Exception as e:
        print(f"XML-Ladefehler: {e}. Starte neu.")
        return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 0

def speichere_spielstand(statistik, gesamt):

    root = ET.Element("Spielstand")    

    ET.SubElement(root, "Gesamt").text = str(gesamt)    

    verteilung_node = ET.SubElement(root, "Verteilung")
    
    for zahl in range(1, 7):

        wurf_node = ET.SubElement(verteilung_node, "Wurf", zahl=str(zahl))
        wurf_node.text = str(statistik[zahl])

    tree = ET.ElementTree(root)
    tree.write(FILENAME, encoding="utf-8", xml_declaration=True)
    print(f"\nFortschritt in '{FILENAME}' gespeichert!")

def wuerfel_spiel():
    statistik, gesamt_anzahl = lade_spielstand()
    print("\n--- Würfelspiel (XML-Edition) ---")
    
    while True:
        ergebnis = random.randint(1, 6)
        statistik[ergebnis] += 1
        gesamt_anzahl += 1
        
        print(f"\nGewürfelt: {ergebnis} | Total: {gesamt_anzahl}")
        print("Statistik:")
        for z, a in statistik.items():
            print(f"  {z}: {a}x")
        
        if input("\nNochmal? (j/n): ").lower() != 'j':
            speichere_spielstand(statistik, gesamt_anzahl)
            break

if __name__ == "__main__":
    wuerfel_spiel()