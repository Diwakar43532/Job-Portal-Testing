// Dedicated Topic-Wise DSA Sheet Controller

let selectedDSATopic = 'All';
let currentDSAProblems = [];
let currentViewingDSAProblem = null;
let currentCodeLang = 'python';

async function fetchDSATopics() {
  const container = document.getElementById('dsa-topic-pills');
  if (!container) return;

  try {
    const res = await fetch('/api/dsa/topics');
    const data = await res.json();
    const topics = data.topics || [];

    let html = `
      <button onclick="filterDSATopic('All')" class="dsa-topic-btn ${selectedDSATopic === 'All' ? 'active bg-brand-500/20 text-brand-300 border-brand-500/40' : 'bg-slate-900 text-slate-400 border-slate-700 hover:text-white'} px-3 py-1 rounded-full border whitespace-nowrap font-medium transition-all">
        All Topics
      </button>
    `;

    html += topics.map(t => {
      const isAct = selectedDSATopic === t.topic;
      return `
        <button onclick="filterDSATopic('${t.topic}')" class="dsa-topic-btn ${isAct ? 'active bg-brand-500/20 text-brand-300 border-brand-500/40' : 'bg-slate-900 text-slate-400 border-slate-700 hover:text-white'} px-3 py-1 rounded-full border whitespace-nowrap font-medium transition-all flex items-center space-x-1.5">
          <span>${t.topic}</span>
          <span class="text-[10px] px-1.5 py-0.2 rounded-full ${t.solved === t.total ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-400'} font-bold">
            ${t.solved}/${t.total}
          </span>
        </button>
      `;
    }).join('');

    container.innerHTML = html;
  } catch (err) {
    console.error('Error fetching DSA topics:', err);
  }
}

function filterDSATopic(topic) {
  selectedDSATopic = topic;
  fetchDSATopics();
  fetchDSAProblems();
}

async function fetchDSAStats() {
  try {
    const res = await fetch('/api/dsa/stats');
    const stats = await res.json();

    const pctEl = document.getElementById('dsa-stat-pct');
    const barEl = document.getElementById('dsa-progress-bar');
    const easyEl = document.getElementById('dsa-stat-easy');
    const medEl = document.getElementById('dsa-stat-med');
    const hardEl = document.getElementById('dsa-stat-hard');

    if (pctEl) pctEl.textContent = `${stats.percentage}%`;
    if (barEl) barEl.style.width = `${stats.percentage}%`;
    if (easyEl) easyEl.textContent = `${stats.by_difficulty.easy.solved}/${stats.by_difficulty.easy.total}`;
    if (medEl) medEl.textContent = `${stats.by_difficulty.medium.solved}/${stats.by_difficulty.medium.total}`;
    if (hardEl) hardEl.textContent = `${stats.by_difficulty.hard.solved}/${stats.by_difficulty.hard.total}`;
  } catch (err) {
    console.error('Error fetching DSA stats:', err);
  }
}

async function fetchDSAProblems() {
  const tbody = document.getElementById('dsa-problems-tbody');
  if (!tbody) return;

  const search = document.getElementById('dsa-search-input')?.value.trim() || '';
  const difficulty = document.getElementById('dsa-difficulty-select')?.value || 'All';
  const status = document.getElementById('dsa-status-select')?.value || 'All';

  let url = '/api/dsa/problems?';
  const params = [];
  if (selectedDSATopic && selectedDSATopic !== 'All') params.push(`topic=${encodeURIComponent(selectedDSATopic)}`);
  if (difficulty && difficulty !== 'All') params.push(`difficulty=${encodeURIComponent(difficulty)}`);
  if (status && status !== 'All') params.push(`status=${encodeURIComponent(status)}`);
  if (search) params.push(`search=${encodeURIComponent(search)}`);
  url += params.join('&');

  tbody.innerHTML = `
    <tr>
      <td colspan="6" class="py-12 text-center text-slate-400">
        <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-brand-400"></i>
        <p class="text-xs">Loading DSA problems...</p>
      </td>
    </tr>
  `;

  try {
    const res = await fetch(url);
    const data = await res.json();
    currentDSAProblems = data.problems || [];

    renderDSAProblemsTable();
  } catch (err) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="py-6 text-center text-rose-400 text-xs">
          Failed to load DSA problems.
        </td>
      </tr>
    `;
  }
}

function renderDSAProblemsTable() {
  const tbody = document.getElementById('dsa-problems-tbody');
  if (!tbody) return;

  if (!currentDSAProblems.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="py-12 text-center text-slate-400">
          <p class="text-xs">No problems match your current filter criteria.</p>
        </td>
      </tr>
    `;
    return;
  }

  const diffColors = {
    'Easy': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    'Medium': 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    'Hard': 'bg-rose-500/10 text-rose-400 border-rose-500/20'
  };

  const statusIcons = {
    'Solved': '<i class="fa-solid fa-circle-check text-emerald-400 text-base"></i>',
    'In Progress': '<i class="fa-solid fa-circle-play text-amber-400 text-base"></i>',
    'Revise': '<i class="fa-solid fa-bookmark text-violet-400 text-base"></i>',
    'Unsolved': '<i class="fa-regular fa-circle text-slate-500 text-base"></i>'
  };

  tbody.innerHTML = currentDSAProblems.map(p => {
    const hasNotes = Boolean(p.user_notes && p.user_notes.trim());

    return `
      <tr class="hover:bg-slate-700/40 transition-colors group">
        
        <!-- Status Toggle -->
        <td class="py-3 px-4 text-center">
          <button onclick="cycleProblemStatus(${p.id}, '${p.user_status}')" class="p-1 rounded hover:scale-110 transition-transform" title="Current Status: ${p.user_status}. Click to change status">
            ${statusIcons[p.user_status] || statusIcons['Unsolved']}
          </button>
        </td>

        <!-- Title & Topic -->
        <td class="py-3 px-4">
          <div class="flex items-center space-x-2">
            <span class="font-bold text-white group-hover:text-brand-300 transition-colors">${p.title}</span>
            <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-900 border border-slate-700 text-slate-400">
              ${p.topic}
            </span>
          </div>
        </td>

        <!-- Difficulty -->
        <td class="py-3 px-4">
          <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${diffColors[p.difficulty] || diffColors.Easy}">
            ${p.difficulty}
          </span>
        </td>

        <!-- Complexity -->
        <td class="py-3 px-4 text-xs font-mono text-slate-400">
          <div>Time: <span class="text-slate-200 font-bold">${p.time_complexity}</span></div>
          <div>Space: <span class="text-slate-200 font-bold">${p.space_complexity}</span></div>
        </td>

        <!-- Practice Links -->
        <td class="py-3 px-4 text-center">
          <div class="flex items-center justify-center space-x-2 text-xs">
            ${p.leetcode_url ? `
              <a href="${p.leetcode_url}" target="_blank" rel="noopener noreferrer" class="p-1.5 rounded-lg bg-slate-900 hover:bg-amber-500/20 text-slate-400 hover:text-amber-400 border border-slate-700 transition-all" title="Solve on LeetCode">
                <i class="fa-solid fa-terminal"></i>
              </a>
            ` : ''}
            ${p.gfg_url ? `
              <a href="${p.gfg_url}" target="_blank" rel="noopener noreferrer" class="p-1.5 rounded-lg bg-slate-900 hover:bg-emerald-500/20 text-slate-400 hover:text-emerald-400 border border-slate-700 transition-all" title="Solve on GeeksforGeeks">
                <i class="fa-solid fa-code"></i>
              </a>
            ` : ''}
          </div>
        </td>

        <!-- Actions: Solution & Personal Notes -->
        <td class="py-3 px-4 text-center">
          <div class="flex items-center justify-center space-x-2 text-xs">
            <button onclick="openDSASolutionModal(${p.id})" class="px-2.5 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-semibold transition-all flex items-center space-x-1 shadow-sm">
              <i class="fa-solid fa-lightbulb text-[10px]"></i>
              <span>Solution</span>
            </button>
            <button onclick="openDSANotesModal(${p.id}, '${escapeHTML(p.title)}', '${escapeHTML(p.user_notes)}')" class="p-1.5 rounded-lg ${hasNotes ? 'bg-amber-500/20 text-amber-400 border-amber-500/40' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'} border border-slate-600 transition-all" title="Personal Notes">
              <i class="fa-regular fa-note-sticky"></i>
            </button>
          </div>
        </td>

      </tr>
    `;
  }).join('');
}

function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

async function cycleProblemStatus(problemId, currentStatus) {
  const statusCycle = {
    'Unsolved': 'In Progress',
    'In Progress': 'Solved',
    'Solved': 'Revise',
    'Revise': 'Unsolved'
  };
  const newStatus = statusCycle[currentStatus] || 'Solved';

  try {
    const res = await fetch(`/api/dsa/problems/${problemId}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      showToast(`Status updated to: ${newStatus}`, 'info');
      // Update locally
      const p = currentDSAProblems.find(item => item.id === problemId);
      if (p) p.user_status = newStatus;
      renderDSAProblemsTable();
      fetchDSAStats();
      fetchDSATopics();
    }
  } catch (err) {
    showToast('Failed to update status', 'error');
  }
}

async function openDSASolutionModal(problemId) {
  try {
    const res = await fetch(`/api/dsa/problems/${problemId}`);
    currentViewingDSAProblem = await res.json();
    const p = currentViewingDSAProblem;

    document.getElementById('dsa-sol-title').textContent = p.title;
    document.getElementById('dsa-sol-topic').textContent = p.topic;
    document.getElementById('dsa-sol-diff').textContent = p.difficulty;
    document.getElementById('dsa-sol-desc').textContent = p.description;
    document.getElementById('dsa-sol-approach').textContent = p.approach_notes;
    document.getElementById('dsa-sol-time').textContent = p.time_complexity;
    document.getElementById('dsa-sol-space').textContent = p.space_complexity;

    setDSACodeLang(currentCodeLang);

    openModal('modal-dsa-solution');
  } catch (err) {
    showToast('Failed to load solution', 'error');
  }
}

function setDSACodeLang(lang) {
  currentCodeLang = lang;
  const btnPy = document.getElementById('code-btn-python');
  const btnCpp = document.getElementById('code-btn-cpp');
  const codeEl = document.getElementById('dsa-sol-code');

  if (lang === 'python') {
    if (btnPy) btnPy.className = 'px-3 py-1 rounded bg-brand-600 text-white';
    if (btnCpp) btnCpp.className = 'px-3 py-1 rounded text-slate-400 hover:text-white';
    if (codeEl && currentViewingDSAProblem) {
      codeEl.className = 'language-python';
      codeEl.textContent = currentViewingDSAProblem.code_python;
    }
  } else {
    if (btnCpp) btnCpp.className = 'px-3 py-1 rounded bg-brand-600 text-white';
    if (btnPy) btnPy.className = 'px-3 py-1 rounded text-slate-400 hover:text-white';
    if (codeEl && currentViewingDSAProblem) {
      codeEl.className = 'language-cpp';
      codeEl.textContent = currentViewingDSAProblem.code_cpp;
    }
  }

  if (typeof hljs !== 'undefined' && codeEl) {
    hljs.highlightElement(codeEl);
  }
}

function copyDSACode() {
  const codeEl = document.getElementById('dsa-sol-code');
  if (!codeEl) return;

  navigator.clipboard.writeText(codeEl.textContent).then(() => {
    const copyText = document.getElementById('copy-btn-text');
    if (copyText) {
      copyText.textContent = 'Copied!';
      setTimeout(() => copyText.textContent = 'Copy', 2000);
    }
    showToast('Code copied to clipboard', 'success');
  }).catch(() => {
    showToast('Failed to copy code', 'error');
  });
}

function openDSANotesModal(problemId, problemTitle, currentNotes) {
  document.getElementById('notes-problem-id').value = problemId;
  document.getElementById('notes-modal-title').textContent = `Notes: ${problemTitle}`;
  document.getElementById('notes-textarea').value = currentNotes || '';
  openModal('modal-dsa-notes');
}

async function saveProblemNotes() {
  const problemId = document.getElementById('notes-problem-id').value;
  const notes = document.getElementById('notes-textarea').value.trim();

  try {
    const res = await fetch(`/api/dsa/problems/${problemId}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes: notes })
    });
    if (res.ok) {
      showToast('Problem notes saved successfully', 'success');
      closeModal('modal-dsa-notes');
      // Update local state
      const p = currentDSAProblems.find(item => item.id == problemId);
      if (p) p.user_notes = notes;
      renderDSAProblemsTable();
    }
  } catch (err) {
    showToast('Failed to save notes', 'error');
  }
}
