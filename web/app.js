async function fetchJSON(url, options){
  const res = await fetch(url, Object.assign({ headers: { 'Content-Type': 'application/json' } }, options));
  if(!res.ok){
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

async function loadSkills(){
  const container = document.getElementById('skills');
  container.innerHTML = '<div class="muted">Loading…</div>';

  // Get selected tiers
  const selectedTiers = [];
  if (document.getElementById('tierT0').checked) selectedTiers.push('T0');
  if (document.getElementById('tierT1').checked) selectedTiers.push('T1');
  if (document.getElementById('tierT2').checked) selectedTiers.push('T2');

  try{
    // Build URL with tier filters
    let url = '/api/skills';
    if (selectedTiers.length > 0) {
      const params = new URLSearchParams();
      selectedTiers.forEach(tier => params.append('tiers', tier));
      url += '?' + params.toString();
    }

    const skills = await fetchJSON(url);
    container.innerHTML = '';
    skills.forEach(s => {
      const card = document.createElement('div');
      card.className = 'skill';
      card.innerHTML = `
        <h3>${s.name} <span class="muted">v${s.version}</span></h3>
        <div class="muted">Tier: ${s.tier ?? '—'}</div>
        <p>${s.description ?? ''}</p>
        <button data-skill="${s.name}">View</button>
      `;
      card.querySelector('button').addEventListener('click', async () => {
        const detail = await fetchJSON(`/api/skills/${encodeURIComponent(s.name)}`);
        alert(JSON.stringify(detail, null, 2));
      });
      container.appendChild(card);
    });
  }catch(e){
    container.innerHTML = `<div class="muted">Failed to load skills: ${e.message}</div>`;
  }
}

async function plan(){
  const input = document.getElementById('taskInput');
  const provider = document.getElementById('provider').value;
  const model = document.getElementById('model').value;
  const apiKey = document.getElementById('apiKey').value;
  const useBaml = document.getElementById('useBaml').checked;
  const output = document.getElementById('planOutput');
  output.textContent = 'Planning…';
  try{
    const result = await fetchJSON('/api/plan', {
      method: 'POST',
      body: JSON.stringify({ task: input.value, context: {}, provider, model, api_key: apiKey || null, use_baml: useBaml })
    });
    output.textContent = JSON.stringify(result, null, 2);
  }catch(e){
    output.textContent = `Error: ${e.message}`;
  }
}

document.getElementById('planBtn').addEventListener('click', plan);
document.getElementById('refreshSkills').addEventListener('click', loadSkills);

// Add event listeners for tier checkboxes
document.getElementById('tierT0').addEventListener('change', loadSkills);
document.getElementById('tierT1').addEventListener('change', loadSkills);
document.getElementById('tierT2').addEventListener('change', loadSkills);

window.addEventListener('DOMContentLoaded', loadSkills);

