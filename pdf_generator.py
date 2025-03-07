from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def genereer_pdf(zaagplan, totalelengte, totalerest, efficientie, bestandspad="zaagplan.pdf"):
    """ Genereert een PDF-bestand met het zaagplan. """
    c = canvas.Canvas(bestandspad, pagesize=A4)
    width, height = A4
    y_offset = height - 50  # Startpositie voor tekst

    # Titel
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_offset, "Zaagplan Overzicht")
    y_offset -= 30

    # Samenvatting
    c.setFont("Helvetica", 12)
    c.drawString(50, y_offset, f"Totaal ruw materiaal: {totalelengte} mm")
    c.drawString(300, y_offset, f"Breedte Zaagsnede: 5mm")
    y_offset -= 20
    c.drawString(50, y_offset, f"Totaal restmateriaal: {totalerest} mm")
    c.drawString(300, y_offset, f"Standaard Lengte: 12000mm")
    y_offset -= 20
    c.drawString(50, y_offset, f"Lengtes Gebruikt:")
    y_offset -= 20
    c.drawString(70, y_offset, f"# Voorraad lengte(s):")
    y_offset -= 20
    c.drawString(70, y_offset, f"# Standaard lengte(s):")
    y_offset -= 20
    c.drawString(50, y_offset, f"Efficiëntie: {efficientie:.2f}%")
    y_offset -= 40

    
    
    y_offset -= 20

    # Zaagplan details
    for i, staaf in enumerate(zaagplan):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_offset, f"Staaf {i+1} ({staaf['lengte']} mm) [{staaf['type']}]")
        y_offset -= 20

        c.setFont("Helvetica", 10)
        c.drawString(70, y_offset, f"Aantal zaagsnedes: {staaf['zaagsnedes']}")
        y_offset -= 15

        for stuk in staaf["stukken"]:
            c.drawString(90, y_offset, f"- {stuk['lengte']} mm voor {stuk['project']}")
            y_offset -= 15

        c.drawString(70, y_offset, f"Restmateriaal: {staaf['rest']} mm")
        y_offset -= 30

        # Pagina-overflow voorkomen
        if y_offset < 100:
            c.showPage()
            y_offset = height - 50

    c.save()
    print(f"PDF gegenereerd: {bestandspad}")
