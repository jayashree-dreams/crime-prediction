document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('/states');
    const states = await res.json();
    const sel = document.getElementById('state');
    sel.innerHTML = '';
    states.forEach(s => { const o = document.createElement('option'); o.value=s; o.textContent=s; sel.appendChild(o); });
  } catch (e) { console.error('Failed to load states', e); }

  const ctx = document.getElementById('crimeChart').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Predicted total crimes', data: [], tension:0.4, fill:true, backgroundColor:'rgba(54,162,235,0.2)', borderColor:'#36a2eb' }]},
    options: { responsive:true, scales:{ y: { beginAtZero:true } } }
  });

  document.getElementById('predict-form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const payload = {
      state: document.getElementById('state').value,
      year: parseInt(document.getElementById('year').value,10),
      crime_type: document.getElementById('crime_type').value,
      population: parseFloat(document.getElementById('population').value) || 0,
      murder: parseFloat(document.getElementById('murder').value) || 0,
      rape: parseFloat(document.getElementById('rape').value) || 0,
      robbery: parseFloat(document.getElementById('robbery').value) || 0,
      theft: parseFloat(document.getElementById('theft').value) || 0,
      assault: 0,
      property_crime: 0
    };
    document.getElementById('prediction-text').textContent = 'Predicting...';
    document.getElementById('prediction-card').style.display = 'block';
    try {
      const r = await fetch('/predict', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
      const data = await r.json();
      if (data.predicted_total_crimes !== undefined) {
        const val = Math.round(data.predicted_total_crimes);
        document.getElementById('prediction-text').textContent = val.toLocaleString();
        chart.data.labels.push(payload.year.toString());
        chart.data.datasets[0].data.push(val);
        chart.update();
      } else {
        document.getElementById('prediction-text').textContent = 'Prediction error';
      }
    } catch (err) {
      console.error(err);
      document.getElementById('prediction-text').textContent = 'Server error';
    }
  });
});
