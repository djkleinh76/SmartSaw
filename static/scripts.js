document.addEventListener("DOMContentLoaded", function() {
    ensureMinimumRows("zaagplanTable");
    ensureMinimumRows("voorraadTable");
});

function addRow(tableId) {
    let table = document.getElementById(tableId);
    let row = table.insertRow(-1);
    
    if (tableId === "zaagplanTable") {
        row.innerHTML = `
            <td><input type="text" name="projectnaam" required></td>
            <td><input type="number" name="lengte" required></td>
            <td><input type="number" name="aantal" required></td>
            <td><button type="button" class="delete-btn" onclick="removeRow(this, '${tableId}')">-</button></td>
        `;
    } else {
        row.innerHTML = `
            <td><input type="number" name="voorraad_lengte" required></td>
            <td><input type="number" name="voorraad_aantal" required></td>
            <td><button type="button" class="delete-btn" onclick="removeRow(this, '${tableId}')">-</button></td>
        `;
    }
    
    row.cells[0].children[0].focus(); // Zet de focus op het eerste veld in de nieuwe rij
}

function removeRow(button, tableId) {
    let table = document.getElementById(tableId);
    if (table.rows.length > 2) {
        let row = button.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
}

function ensureMinimumRows(tableId) {
    let table = document.getElementById(tableId);
    if (table.rows.length < 2) {
        addRow(tableId);
    }
}
/*
function submitForm() {
    let zaagplanData = {};
    let voorraadData = {};

    let zaagplanTable = document.getElementById("zaagplanTable");
    let voorraadTable = document.getElementById("voorraadTable");

    for (let i = 1; i < zaagplanTable.rows.length; i++) {
        let project = zaagplanTable.rows[i].cells[0].children[0].value;
        let lengte = zaagplanTable.rows[i].cells[1].children[0].value;
        let aantal = zaagplanTable.rows[i].cells[2].children[0].value;

        if (project && lengte && aantal) {
            if (!zaagplanData[project]) {
                zaagplanData[project] = {};
            }
            zaagplanData[project][parseInt(lengte)] = parseInt(aantal);
        }
    }

    for (let i = 1; i < voorraadTable.rows.length; i++) {
        let lengte = voorraadTable.rows[i].cells[0].children[0].value;
        let aantal = voorraadTable.rows[i].cells[1].children[0].value;

        if (lengte && aantal) {
            voorraadData[parseInt(lengte)] = parseInt(aantal);
        }
    }

    // ✅ **Stuur JSON correct met headers en body**
    fetch("/generate-zaagplan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },  // 🔥 JSON-header toegevoegd!
        body: JSON.stringify({ zaaglijst: zaagplanData, voorraad: voorraadData })  // 🔥 JSON correct verzonden
    })
    .then(response => response.json())
    .then(data => {
        console.log("DEBUG - Zaagplan response:", data);

        if (data.zaagplan) {
            localStorage.setItem("zaagplanResponse", JSON.stringify(data.zaagplan));  // ✅ Correcte JSON opslag
            alert("Zaagplan gegenereerd!");
        } else {
            alert("Fout bij genereren zaagplan: " + (data.error || "Onbekende fout"));
        }
    })
    .catch(error => console.error("Fout bij zaagplan-aanvraag:", error));
}
*/

function submitForm() {
    let zaagplanData = {};
    let voorraadData = {};

    let zaagplanTable = document.getElementById("zaagplanTable");
    let voorraadTable = document.getElementById("voorraadTable");

    // ✅ Haal zaagbreedte en standaard voorraadlengte op
    let zaagbreedte = document.getElementById("zaagbreedteInput").value;
    let standaardLengte = document.getElementById("standaardVoorraadInput").value;

    // ✅ Verwerk zaagplan invoer
    for (let i = 1; i < zaagplanTable.rows.length; i++) {
        let project = zaagplanTable.rows[i].cells[0].children[0].value;
        let lengte = zaagplanTable.rows[i].cells[1].children[0].value;
        let aantal = zaagplanTable.rows[i].cells[2].children[0].value;

        if (project && lengte && aantal) {
            if (!zaagplanData[project]) {
                zaagplanData[project] = {};
            }
            zaagplanData[project][parseInt(lengte)] = parseInt(aantal);
        }
    }

    // ✅ Verwerk voorraad invoer
    for (let i = 1; i < voorraadTable.rows.length; i++) {
        let lengte = voorraadTable.rows[i].cells[0].children[0].value;
        let aantal = voorraadTable.rows[i].cells[1].children[0].value;

        if (lengte && aantal) {
            voorraadData[parseInt(lengte)] = parseInt(aantal);
        }
    }

    // ✅ **Zorg dat alle data correct wordt verzonden**
    let data = {
        zaaglijst: zaagplanData,
        voorraad: voorraadData,
        zaagbreedte: parseInt(zaagbreedte),
        standaard_lengte: parseInt(standaardLengte)
    };

    console.log("DEBUG - Data die naar backend wordt gestuurd:", data);

    // ✅ **Verstuur data correct als JSON**
    fetch("/generate-zaagplan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("DEBUG - Zaagplan response:", data);

        if (data.zaagplan) {
            localStorage.setItem("zaagplanResponse", JSON.stringify(data.zaagplan));  // ✅ Correcte JSON opslag
            alert("Zaagplan gegenereerd!");
        } else {
            alert("Fout bij genereren zaagplan: " + (data.error || "Onbekende fout"));
        }
    })
    .catch(error => console.error("Fout bij zaagplan-aanvraag:", error));
}


function generatePDF() {
    console.log("DEBUG - PDF genereren gestart");

    // ✅ Haal het zaagplan op en converteer de string naar een echt JSON-object
    let zaagplanData = JSON.parse(localStorage.getItem("zaagplanResponse"));

    if (!zaagplanData) {
        alert("Fout: Geen zaagplan beschikbaar. Genereer eerst een zaagplan.");
        return;
    }
    console.log("DEBUG - Verzenden JSON naar PDF-generator:", zaagplanData);

    fetch("/generate-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zaagplan: zaagplanData })  // ✅ Nu correct als JSON verstuurd
    })
    .then(response => response.json())
    .then(data => {
        console.log("DEBUG - Server response:", data);
        if (data.pdf_path) {
            console.log("DEBUG - PDF gegenereerd:", data.pdf_path);
            window.location.href = data.pdf_path; // PDF downloaden
        } else {
            alert("Fout bij genereren PDF: " + (data.error || "Onbekende fout"));
        }
    })
    .catch(error => console.error("Fout bij PDF-aanvraag:", error));
}