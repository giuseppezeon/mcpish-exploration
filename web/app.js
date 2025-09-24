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
  try{
    const skills = await fetchJSON('/api/skills');
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
window.addEventListener('DOMContentLoaded', loadSkills);

