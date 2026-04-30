const API_BASE = 'http://127.0.0.1:5000';

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function loadList() {
  const listEl = document.getElementById('coaster-list');
  listEl.textContent = 'Loading...';
  try {
    const data = await fetchJSON(`${API_BASE}/coasters`);
    listEl.innerHTML = '';
    if (!data || !data.length) {
      listEl.textContent = 'No rollercoasters found.';
      return;
    }
    data.forEach(c => {
      const li = document.createElement('li');
      const btn = document.createElement('button');
      btn.textContent = c.name;
      btn.addEventListener('click', () => loadDetails(c.rollercoaster_id));
      li.appendChild(btn);
      listEl.appendChild(li);
    });
  } catch (err) {
    listEl.textContent = 'Failed to load list.';
    console.error(err);
  }
}

async function loadDetails(id) {
  const det = document.getElementById('coaster-details');
  det.textContent = 'Loading...';
  try {
    const c = await fetchJSON(`${API_BASE}/coasters/${id}`);
    det.innerHTML = renderDetails(c);
  } catch (err) {
    det.textContent = 'Failed to load details.';
    console.error(err);
  }
}

function renderDetails(c) {
  if (!c) return 'Not found';
  return `
    <h3>${escapeHtml(c.name)}</h3>
    <p><strong>Park:</strong> ${escapeHtml(c.park_name || 'Unknown')}</p>
    <p><strong>Manufacturer:</strong> ${escapeHtml(c.manufacturer_name || 'Unknown')}</p>
    <p><strong>Type:</strong> ${escapeHtml(c.type)}</p>
    <p><strong>Height:</strong> ${escapeHtml(c.height)}</p>
    <p><strong>Speed:</strong> ${escapeHtml(c.speed)}</p>
    <p><strong>Length:</strong> ${escapeHtml(c.length)}</p>
    <p><strong>Year Opened:</strong> ${escapeHtml(c.year_opened)}</p>
    <p><strong>Thrill level:</strong> ${escapeHtml(c.thrill_level)}</p>
    <p><strong>Inversions:</strong> ${escapeHtml(String(c.inversions))}</p>
    <p><strong>Age:</strong> ${escapeHtml(String(c.age))}</p>
    <p><em>${escapeHtml(c.image || '')}</em></p>
  `;
}

// small helper to avoid XSS when rendering simple strings
function escapeHtml(s) {
  if (!s && s !== 0) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Render query results into the results container
function renderQueryResults(data) {
  hideChart();
  const out = document.getElementById('query-results');
  if (!out) return;
  if (!data) {
    out.textContent = 'No results.';
    return;
  }
  if (Array.isArray(data)) {
    if (data.length === 0) {
      out.textContent = 'No results.';
      return;
    }
    const first = data[0];
    if (first && typeof first === 'object') {
      const keys = Object.keys(first);
      const table = document.createElement('table');
      const thead = document.createElement('thead');
      const trh = document.createElement('tr');
      keys.forEach(k => { const th = document.createElement('th'); th.textContent = k; trh.appendChild(th); });
      thead.appendChild(trh);
      table.appendChild(thead);
      const tbody = document.createElement('tbody');
      data.forEach(row => {
        const tr = document.createElement('tr');
        keys.forEach(k => {
          const td = document.createElement('td');
          td.textContent = row[k] === null || row[k] === undefined ? '' : row[k];
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      out.innerHTML = '';
      out.appendChild(table);
      return;
    }
    out.innerHTML = '';
    const ul = document.createElement('ul');
    data.forEach(i => { const li = document.createElement('li'); li.textContent = String(i); ul.appendChild(li); });
    out.appendChild(ul);
    return;
  }
  out.textContent = typeof data === 'object' ? JSON.stringify(data, null, 2) : String(data);
}

async function safeFetchJSON(path) {
  try {
    const url = `${API_BASE}${path}`;
    return await fetchJSON(url);
  } catch (err) {
    const out = document.getElementById('query-results');
    if (out) out.textContent = 'Query failed.';
    console.error(err);
    return null;
  }
}

// Chart.js integration
let queryChart = null;
function hideChart() {
  const wrap = document.getElementById('chart-wrap');
  if (wrap) wrap.style.display = 'none';
}

function showChart() {
  const wrap = document.getElementById('chart-wrap');
  if (wrap) wrap.style.display = 'block';
}

function renderChart(labels, values, title = '') {
  const ctx = document.getElementById('query-chart').getContext('2d');
  if (queryChart) queryChart.destroy();
  queryChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{ label: title, data: values, backgroundColor: 'rgba(255,83,123,0.9)' }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, title: { display: !!title, text: title } },
      scales: { y: { beginAtZero: true } }
    }
  });
  showChart();
}

function renderChartFromObjects(data, labelKeys, valueKeys, title) {
  if (!Array.isArray(data) || data.length === 0) return false;
  const first = data[0];
  const labelKey = labelKeys.find(k => k in first) || Object.keys(first)[0];
  const valueKey = valueKeys.find(k => k in first) || Object.keys(first).find(k => typeof first[k] === 'number' || !isNaN(Number(first[k])));
  if (!labelKey || !valueKey) return false;
  const labels = data.map(r => r[labelKey]);
  const values = data.map(r => Number(r[valueKey] || 0));
  renderChart(labels, values, title || `${valueKey} by ${labelKey}`);
  return true;
}

function setupQueries() {
  const byId = id => document.getElementById(id);
  byId('btn-operating')?.addEventListener('click', async () => { hideChart(); renderQueryResults(await safeFetchJSON('/queries/operating')); });
  byId('btn-defunct')?.addEventListener('click', async () => { hideChart(); renderQueryResults(await safeFetchJSON('/queries/defunct')); });
  byId('btn-sbno')?.addEventListener('click', async () => { hideChart(); renderQueryResults(await safeFetchJSON('/queries/sbno')); });
  byId('btn-manuf-avg-height')?.addEventListener('click', async () => {
    const data = await safeFetchJSON('/queries/manufacturers/avg_height');
    if (data) {
      const did = renderChartFromObjects(data, ['manufacturer', 'name'], ['avg_height', 'avg'], 'Manufacturers — Avg Height');
      if (!did) { hideChart(); renderQueryResults(data); } else { document.getElementById('query-results').innerHTML = ''; }
    }
  });
  byId('btn-manuf-avg-speed')?.addEventListener('click', async () => {
    const data = await safeFetchJSON('/queries/manufacturers/avg_speed');
    if (data) {
      const did = renderChartFromObjects(data, ['manufacturer', 'name'], ['avg_speed', 'avg'], 'Manufacturers — Avg Speed');
      if (!did) { hideChart(); renderQueryResults(data); } else { document.getElementById('query-results').innerHTML = ''; }
    }
  });
  byId('btn-parks-low-wait')?.addEventListener('click', async () => {
    const data = await safeFetchJSON('/queries/parks/low_wait_high_attendance');
    if (data) {
      const did = renderChartFromObjects(data, ['park_name', 'name'], ['daily_visitors', 'avg_wait', 'visitors_per_day'], 'Parks — Visitors vs Avg Wait');
      if (!did) { hideChart(); renderQueryResults(data); } else { document.getElementById('query-results').innerHTML = ''; }
    }
  });
  const topX = () => document.getElementById('top-x')?.value.trim() || '';
  byId('btn-top-age')?.addEventListener('click', async () => {
    const data = await safeFetchJSON(`/queries/top/age?x=${encodeURIComponent(topX())}`);
    if (data) {
      const did = renderChartFromObjects(data, ['name'], ['age'], 'Top by Age');
      if (!did) { hideChart(); renderQueryResults(data); } else { document.getElementById('query-results').innerHTML = ''; }
    }
  });
  byId('btn-top-height')?.addEventListener('click', async () => {
    const data = await safeFetchJSON(`/queries/top/height?x=${encodeURIComponent(topX())}`);
    if (data) {
      const did = renderChartFromObjects(data, ['name'], ['height'], 'Top by Height');
      if (!did) { hideChart(); renderQueryResults(data); } else { document.getElementById('query-results').innerHTML = ''; }
    }
  });
  byId('btn-top-speed')?.addEventListener('click', async () => {
    const data = await safeFetchJSON(`/queries/top/speed?x=${encodeURIComponent(topX())}`);
    if (data) {
      const did = renderChartFromObjects(data, ['name'], ['speed'], 'Top by Speed');
      if (!did) { hideChart(); renderQueryResults(data); } else { document.getElementById('query-results').innerHTML = ''; }
    }
  });
  byId('btn-top-length')?.addEventListener('click', async () => {
    const data = await safeFetchJSON(`/queries/top/length?x=${encodeURIComponent(topX())}`);
    if (data) {
      const did = renderChartFromObjects(data, ['name'], ['length'], 'Top by Length');
      if (!did) { hideChart(); renderQueryResults(data); } else { document.getElementById('query-results').innerHTML = ''; }
    }
  });
}

window.addEventListener('DOMContentLoaded', () => { loadList(); setupQueries(); });