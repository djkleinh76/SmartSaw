import json
from smartsaw import SmartSaw
from pdf_generator import genereer_pdf

def verwerk_zaagplan(data):
    """
    Ontvangt de JSON-invoer, verwerkt deze met SmartSaw en retourneert het geoptimaliseerde zaagplan.
    """
    print("🔹 DEBUG - Ontvangen data in backend:", data)  # ✅ Check ontvangen JSON
    print("🔹 DEBUG - Type ontvangen data:", type(data))  # ✅ Controleer of het een dict is

    try:
        # JSON-invoer is al een dictionary, geen json.loads() nodig!
        te_zagen = data.get("zaaglijst", {})
        voorraad = data.get("voorraad", {})
        standaard_lengte = int(data.get("standaard_lengte", 12000))
        zaagbreedte = int(data.get("zaagbreedte", 5))

        print(data)
        print(te_zagen)
        print(voorraad)
        print(standaard_lengte)
        print(zaagbreedte)

        # Zet JSON-lengtes om naar integers (JSON keys zijn standaard strings)
        te_zagen = {
            project: {int(lengte): aantal for lengte, aantal in stukken.items()}
            for project, stukken in te_zagen.items()
        }
        voorraad = {int(lengte): aantal for lengte, aantal in voorraad.items()}

        # Controleer of de invoer geldig is
        if not te_zagen:
            return {"error": "Fout: Geen te zagen items opgegeven."}, 400

        # Zaagplan genereren met SmartSaw
        smartsaw = SmartSaw(voorraad, standaard_lengte, zaagbreedte)
        zaagplan, _ = smartsaw.optimaliseer_zaagplan(te_zagen)

        # 🔍 Debugging: Bekijk wat `zaagplan` bevat
        print("🔹 Zaagplan gegenereerd:", zaagplan)

        # Bereken samenvatting zonder onnodige conversies
        totalelengte = sum(staaf.get("lengte", 0) for staaf in zaagplan)
        totalerest = sum(staaf.get("rest", 0) for staaf in zaagplan)
        efficientie = 0 if totalelengte == 0 else (1 - (totalerest / totalelengte)) * 100

        # JSON-response terugsturen
        return {
            "message": "Zaagplan succesvol gegenereerd!",
            "zaagplan": zaagplan,
            "totalelengte": totalelengte,
            "totalerest": totalerest,
            "efficientie": round(efficientie, 2)
        }, 200

    except json.JSONDecodeError:
        return {"error": "Fout: Ongeldige JSON-invoer."}, 400
    except Exception as e:
        return {"error": f"Fout bij verwerking: {str(e)}"}, 500

def genereer_zaagplan_pdf(zaagplan):
    """
    Genereert een PDF van het zaagplan en slaat deze op in /static/.
    """
    try:
        print("DEBUG - Start PDF generatie")
        print("DEBUG - Type van ontvangen zaagplan:", type(zaagplan))
        print("DEBUG - Zaagplan data:", zaagplan)

        # Bereken totalen zonder onnodige conversies
        totalelengte = sum(staaf.get("lengte", 0) for staaf in zaagplan)
        totalerest = sum(staaf.get("rest", 0) for staaf in zaagplan)
        efficientie = 0 if totalelengte == 0 else (1 - (totalerest / totalelengte)) * 100

        print("tot hier")
        # PDF genereren
        bestandspad = "static/zaagplan.pdf"
        genereer_pdf(zaagplan, totalelengte, totalerest, efficientie, bestandspad=bestandspad)

        return {"message": "PDF gegenereerd!", "pdf_path": bestandspad}, 200

    except Exception as e:
        return {"error": f"Fout bij PDF-generatie: {str(e)}"}, 500