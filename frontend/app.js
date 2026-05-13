const API_BASE_URL = window.BACKEND_URL || "https://YOUR-BACKEND-SERVICE.onrender.com";

const form = document.getElementById("predict-form");
const stateSelect = document.getElementById("state");
const statusBox = document.getElementById("status");
const resultBox = document.getElementById("result");
const predictionList = document.getElementById("prediction-list");
const totalCrimes = document.getElementById("total-crimes");
const chartCanvas = document.getElementById("crimeChart");

const chart = new Chart(chartCanvas, {
  type: "bar",
  data: {
    labels: [],
    datasets: [{
      label: "Predicted crimes",
      data: [],
      backgroundColor: ["#35d0ff", "#67f0c8", "#9c8cff", "#ffb86b", "#ff6b8b", "#ffd166"],
    }],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#edf6ff",
        },
      },
    },
    scales: {
      x: {
        ticks: { color: "#9fb4c9" },
        grid: { color: "rgba(255,255,255,0.06)" },
      },
      y: {
        beginAtZero: true,
        ticks: { color: "#9fb4c9" },
        grid: { color: "rgba(255,255,255,0.06)" },
      },
    },
  },
});

async function loadStates() {
  try {
    const response = await fetch(`${API_BASE_URL}/states`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const states = await response.json();
    stateSelect.innerHTML = '<option value="">Select a state</option>';

    states.forEach((state) => {
      const option = document.createElement("option");
      option.value = state;
      option.textContent = state;
      stateSelect.appendChild(option);
    });

    statusBox.textContent = "Backend connected. Choose a state and submit a prediction.";
  } catch (error) {
    statusBox.textContent = "Could not load states. Check the backend URL in app.js.";
    stateSelect.innerHTML = '<option value="">Backend unavailable</option>';
    console.error(error);
  }
}

function renderResults(predictions, total) {
  predictionList.innerHTML = "";

  Object.entries(predictions).forEach(([crime, value]) => {
    const item = document.createElement("li");
    item.innerHTML = `<span>${crime.replace(/_/g, " ")}</span><strong>${value.toLocaleString()}</strong>`;
    predictionList.appendChild(item);
  });

  totalCrimes.textContent = `Total predicted crimes: ${total.toLocaleString()}`;
  resultBox.classList.remove("hidden");

  chart.data.labels = Object.keys(predictions).map((crime) => crime.replace(/_/g, " "));
  chart.data.datasets[0].data = Object.values(predictions);
  chart.update();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    state: stateSelect.value,
    year: document.getElementById("year").value,
    population: document.getElementById("population").value,
  };

  statusBox.textContent = "Predicting...";

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Prediction failed");
    }

    renderResults(data.predictions, data.total_crimes);
    statusBox.textContent = `Prediction generated for ${data.state} in ${data.year}.`;
  } catch (error) {
    statusBox.textContent = error.message;
    console.error(error);
  }
});

loadStates();