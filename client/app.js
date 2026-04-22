const API_BASE = ''; // same-origin; when Flask serves the client this will call /coasters and /coasters/:id

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

// Initialize
window.addEventListener('DOMContentLoaded', loadList);