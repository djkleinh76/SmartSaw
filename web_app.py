from flask import Flask, render_template, request, send_file, jsonify
from backend import verwerk_zaagplan, genereer_zaagplan_pdf

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate-zaagplan", methods=["POST"])
def generate_zaagplan():
    print("DEBUG - Start verwerking zaagplan")

    # 🛑 Debugging: Log alles wat binnenkomt
    print("DEBUG - Request headers:", request.headers)
    print("DEBUG - Ruwe request body:", request.data)  # ✅ Dit toont de exacte ontvangen JSON-string
    print("DEBUG - JSON via get_json():", request.get_json())  # ✅ Controleer of JSON correct wordt opgehaald

    data = request.get_json()

    if not data:
        return jsonify({"error": "Geen JSON ontvangen"}), 400  # ❌ Dit betekent dat de frontend niets correct stuurt

    response, status = verwerk_zaagplan(data)
    return jsonify(response), status

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    print("DEBUG - Start verwerking PDF")

    # 🔍 Ontvang de request data
    data = request.get_json()
    print("DEBUG - Ontvangen JSON in backend:", data)

    # Controleer of 'zaagplan' aanwezig is
    if not data or "zaagplan" not in data:
        print("❌ Fout - Geen zaagplan ontvangen!")
        return jsonify({"error": "Geen zaagplan ontvangen"}), 400

    zaagplan = data["zaagplan"]
    print("✅ Zaagplan ontvangen in backend:", zaagplan)

    # Roep de PDF-generator aan
    response, status = genereer_zaagplan_pdf(zaagplan)
    return jsonify(response), status

@app.route("/download-pdf")
def download_pdf():
    return send_file("static/zaagplan.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)