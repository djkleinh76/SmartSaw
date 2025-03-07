import numpy as np
from pdf_generator import genereer_pdf  # Importeer de PDF-functie

class SmartSaw:
    def __init__(self, voorraad, standaard_lengte, zaagbreedte):
        self.voorraad = voorraad.copy()  # Kopie maken om originele data niet te wijzigen
        self.standaard_lengte = standaard_lengte
        self.zaagbreedte = zaagbreedte

    def _neem_staaf(self):
        """ Neemt een voorraadstaaf als beschikbaar, anders een nieuwe standaard staaf. """
        beschikbare_lengtes = sorted(self.voorraad.keys(), reverse=True)

        for lengte in beschikbare_lengtes:
            if self.voorraad[lengte] > 0:
                self.voorraad[lengte] -= 1
                return lengte  # Gebruik voorraadstaaf

        return self.standaard_lengte  # Bestel een nieuwe staaf
    
    """
    def optimaliseer_zaagplan(self, te_zagen):
        
        # Stap 1: Eerst het zaagplan uitvoeren zonder voorraadregel te checken.
        # Stap 2: Na afloop evalueren of de voorraad gebruikt mocht worden en zo nodig corrigeren.
        
        staven_gebruikt = []
        opdrachten = []
        voorraad_vooraf = self.voorraad.copy()  # Bewaar initiële voorraad

        # Stap 1: Standaard zaagplan uitvoeren
        alle_stukken = [(p, l) for p, stukken in te_zagen.items() for l, a in stukken.items() for _ in range(a)]
        alle_stukken.sort(key=lambda x: x[1], reverse=True)

        for project, lengte in alle_stukken:
            beste_staaf = None
            minste_rest = float("inf")

            for staaf in staven_gebruikt:
                rest_na_plaatsen = staaf["rest"] - (lengte + self.zaagbreedte)
                if 0 <= rest_na_plaatsen < minste_rest:
                    beste_staaf = staaf
                    minste_rest = rest_na_plaatsen

            if beste_staaf:
                beste_staaf["stukken"].append({"project": project, "lengte": lengte})
                beste_staaf["rest"] = minste_rest
                beste_staaf["zaagsnedes"] += 1
                opdrachten.append({"project": project, "lengte": lengte, "staaf": beste_staaf["lengte"]})
            else:
                nieuwe_staaf = self._neem_staaf()  # Kies voorraad of bestel nieuwe staaf
                staven_gebruikt.append({
                    "lengte": nieuwe_staaf,
                    "stukken": [{"project": project, "lengte": lengte}],
                    "rest": nieuwe_staaf - lengte - self.zaagbreedte,
                    "type": "voorraad" if nieuwe_staaf in voorraad_vooraf else "bestelstandaard",
                    "zaagsnedes": 1
                })
                opdrachten.append({"project": project, "lengte": lengte, "staaf": nieuwe_staaf})

        return staven_gebruikt, opdrachten
    """

    def optimaliseer_zaagplan(self, te_zagen):
        # Optimalisatie van het zaagplan:
        # Voorkomt negatieve restwaarden door lengtecontrole.
        # Zorgt ervoor dat alle zaagregels correct worden meegenomen.
        # Geeft prioriteit aan bestaande voorraadstaven, mits ze lang genoeg zijn.
        staven_gebruikt = []
        opdrachten = []
        voorraad_vooraf = self.voorraad.copy()  # Bewaar initiële voorraad

        # Sorteer stukken van groot naar klein
        alle_stukken = [(p, l) for p, stukken in te_zagen.items() for l, a in stukken.items() for _ in range(a)]
        alle_stukken.sort(key=lambda x: x[1], reverse=True)

        for project, lengte in alle_stukken:
            beste_staaf = None
            minste_rest = float("inf")

            # ✅ Controle: zoek een bestaande staaf die lang genoeg is
            for staaf in staven_gebruikt:
                rest_na_plaatsen = staaf["rest"] - (lengte + self.zaagbreedte)

                # Staaf mag alleen gekozen worden als de restlengte niet negatief wordt
                if 0 <= rest_na_plaatsen < minste_rest:
                    beste_staaf = staaf
                    minste_rest = rest_na_plaatsen

            if beste_staaf:
                # ✅ Voeg stuk toe aan de beste staaf en update restlengte
                beste_staaf["stukken"].append({"project": project, "lengte": lengte})
                beste_staaf["rest"] = minste_rest
                beste_staaf["zaagsnedes"] += 1
                opdrachten.append({"project": project, "lengte": lengte, "staaf": beste_staaf["lengte"]})
            else:
                # ✅ Neem een nieuwe staaf, maar zorg dat deze groot genoeg is
                nieuwe_staaf = self._neem_staaf()

                if nieuwe_staaf < lengte + self.zaagbreedte:
                    print(f"⚠️ ERROR: Geen geschikte staaf voor lengte {lengte}. Dit stuk wordt overgeslagen!")
                    continue  # Dit voorkomt dat zaagregels verloren gaan!

                # ✅ Voeg de nieuwe staaf toe en verwerk de zaagopdracht correct
                staven_gebruikt.append({
                    "lengte": nieuwe_staaf,
                    "stukken": [{"project": project, "lengte": lengte}],
                    "rest": nieuwe_staaf - lengte - self.zaagbreedte,
                    "type": "voorraad" if nieuwe_staaf in voorraad_vooraf else "bestelstandaard",
                    "zaagsnedes": 1
                })
                opdrachten.append({"project": project, "lengte": lengte, "staaf": nieuwe_staaf})

        return staven_gebruikt, opdrachten


    def print_resultaat(self, zaagplan, opdrachten):
        print("\n--- Geoptimaliseerd Zaagplan ---")
        for i, staaf in enumerate(zaagplan):
            print(f"Staaf {i+1} ({staaf['lengte']} mm) [{staaf['type']}]")
            print(f"  - Aantal zaagsnedes: {staaf['zaagsnedes']}")
            for stuk in staaf["stukken"]:
                print(f"  - {stuk['lengte']} mm voor {stuk['project']}")
            print(f"  - Restmateriaal: {staaf['rest']} mm")

        print("\n--- Opdrachten per project ---")
        projecten = {}
        for opdracht in opdrachten:
            projecten.setdefault(opdracht["project"], []).append(f"{opdracht['lengte']} mm uit {opdracht['staaf']} mm staaf")

        for project, taken in projecten.items():
            print(f"{project}:")
            for taak in taken:
                print(f"  - {taak}")

if __name__ == "__main__":
    # Invoerdata
    #voorraad = {}  
    voorraad = {9000: 1, 2000: 3}  
    standaard_staaf = 12000  # Standaardlengte van nieuwe staven
    zaagbreedte = 5  # Breedte van de zaagsnede
    te_zagen = {
        "Pr15": {560: 48},
        "Pr7": {1800: 24},
        "Pr11": {1800: 24},
        "Pr10": {1700: 24},
        "Pr8": {1200: 48},
        "Pr3": {560: 48},
        "Pr5": {560: 96}
    }  # Nested dict met zaagstukken per project

    # Optimalisatie uitvoeren
    smartsaw = SmartSaw(voorraad, standaard_staaf, zaagbreedte)
    zaagplan, opdrachten = smartsaw.optimaliseer_zaagplan(te_zagen)

    # Samenvatting berekenen
    aantalstukkenstuitvoorraad, aantalstukkenstuitbestelstandaard,totalelengte, totalerest = 0, 0, 0,0
    for i in zaagplan:
        if i["type"] == "voorraad":
            aantalstukkenstuitvoorraad += 1
        elif i["type"]  =="bestelstandaard" :
            aantalstukkenstuitbestelstandaard += 1
        totalelengte += i["lengte"]
        totalerest += i["rest"]

    efficientie = (1 - (totalerest / totalelengte)) * 100

    print("\nSamenvatting zaagplan")
    print(f"Aantal Stukken gebruikt uit voorraaad: {aantalstukkenstuitvoorraad}")
    print(f"Aangevuld met {aantalstukkenstuitbestelstandaard} bestelde lengtes")
    print(f"Totaal aantal lengte aan ruw materiaal: {totalelengte} mm")
    print(f"Totaal lengte restmateriaal: {totalerest} mm")
    print(f"Efficiëntie is {(efficientie)}%")

    # PDF genereren via aparte module
    genereer_pdf(zaagplan, totalelengte, totalerest, efficientie)
