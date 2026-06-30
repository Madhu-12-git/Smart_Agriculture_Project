async function analyzeFarm() {

    const farmId = document.getElementById("farmerId").value;

    const response = await fetch(
        `http://127.0.0.1:8000/farm/${farmId}`
    );

    const data = await response.json();

    if (data.status === "Not Found") {
        alert("Farm ID not found");
        return;
    }

    // ===========================
    // Farm Details
    // ===========================

    document.querySelectorAll(".info-box h2")[0].innerHTML = data.Farm_ID;
    document.querySelectorAll(".info-box h2")[1].innerHTML = data.Crop;
    document.querySelectorAll(".info-box h2")[2].innerHTML = data.District;
    document.querySelectorAll(".info-box h2")[4].innerHTML =
    data.Yield + " q/ac";

    document.querySelectorAll(".info-box h2")[5].innerHTML =
    data.DistrictAverage + " q/ac";
    // ===========================
// Sensor Readings
// ===========================

document.getElementById("sensorSection").innerHTML = `

<div class="sensor">

    <div class="sensor-title">
        <span>🌱 Nitrogen</span>
        <span>${data.N} ppm</span>
    </div>

    <div class="progress">
        <div class="progress-bar green"
             style="width:${data.N}%"></div>
    </div>

</div>

<div class="sensor">

    <div class="sensor-title">
        <span>💧 Moisture</span>
        <span>${data.Moisture}%</span>
    </div>

    <div class="progress">
        <div class="progress-bar blue"
             style="width:${data.Moisture}%"></div>
    </div>

</div>

<div class="sensor">

    <div class="sensor-title">
        <span>☁ Humidity</span>
        <span>${data.Humidity}%</span>
    </div>

    <div class="progress">
        <div class="progress-bar purple"
             style="width:${data.Humidity}%"></div>
    </div>

</div>

<div class="sensor">

    <div class="sensor-title">
        <span>🌡 Temperature</span>
        <span>${data.Temperature}°C</span>
    </div>

    <div class="progress">
        <div class="progress-bar orange"
             style="width:${data.Temperature * 2}%"></div>
    </div>

</div>

<div class="sensor">

    <div class="sensor-title">
        <span>🌿 NDVI</span>
        <span>${data.NDVI}</span>
    </div>

    <div class="progress">
        <div class="progress-bar teal"
             style="width:${data.NDVI * 100}%"></div>
    </div>

</div>

<div class="sensor">

    <div class="sensor-title">
        <span>⚗ Soil pH</span>
        <span>${data.pH}</span>
    </div>

    <div class="progress">
        <div class="progress-bar pink"
             style="width:${data.pH * 7}%"></div>
    </div>

</div>
`;

    // ===========================
    // Yield
    // ===========================

    let difference = (data.Yield - data.DistrictAverage).toFixed(2);

    document.getElementById("yieldSection").innerHTML = `

    <div class="yield-box">

        <h3>Predicted Yield</h3>

        <h1>${data.Yield} Quintals / Acre</h1>

        <p><b>District Average:</b> ${data.DistrictAverage} Quintals / Acre</p>

        <p><b>Difference:</b> ${difference} Quintals / Acre</p>

    </div>

    `;

    // ===========================
    // Pest Risk
    // ===========================

    let riskColor = "green";

    if (data.PestRisk === "MEDIUM")
        riskColor = "orange";

    if (data.PestRisk === "HIGH")
        riskColor = "red";

    document.getElementById("pestSection").innerHTML = `

        <center>

        <h1 style="color:${riskColor};">

            ${data.PestRisk}

        </h1>

        </center>

    `;

    // ===========================
    // Data Quality
    // ===========================

    document.getElementById("qualitySection").innerHTML = `

        <h2>${data.QualityScore}%</h2>

        <h3 style="color:green;">

            ${data.QualityStatus}

        </h3>

    `;

    // ===========================
    // Recommendations
    // ===========================

    let recHTML = "<ul>";

    data.Recommendations.forEach(rec => {

        recHTML += `<li>✅ ${rec}</li>`;

    });

    recHTML += "</ul>";

    document.getElementById("recommendationSection").innerHTML = recHTML;
    // =====================================
// Destroy previous charts
// =====================================

if (window.yieldChartInstance) {
    window.yieldChartInstance.destroy();
}

if (window.ndviChartInstance) {
    window.ndviChartInstance.destroy();
}


// ===========================
// NDVI Trend Chart
// ===========================

if (window.ndviChartInstance) {
    window.ndviChartInstance.destroy();
}

const ndviCtx =
document.getElementById("ndviChart").getContext("2d");

window.ndviChartInstance = new Chart(ndviCtx, {

    type: "line",

    data: {

        labels: data.NDVIDates,

        datasets: [{

            label: "NDVI",

            data: data.NDVIHistory,

            borderColor: "#16a34a",

            backgroundColor: "rgba(22,163,74,0.2)",

            fill: true,

            tension: 0.4,

            pointRadius: 5,

            pointBackgroundColor: "#16a34a"

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                display: true

            }

        },

        scales: {

            y: {

                min: 0,

                max: 1

            }

        }

    }

});
}
analyzeFarm();

function downloadReport(){

    window.print();

}