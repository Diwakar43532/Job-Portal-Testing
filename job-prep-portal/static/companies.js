// Companies Hiring Process Controller

let selectedCompanySegment = 'All';
let companiesList = [];
let currentViewingCompany = null;

async function fetchCompanies() {
  const container = document.getElementById('companies-container');
  if (!container) return;

  container.innerHTML = `
    <div class="col-span-full py-12 text-center text-slate-400">
      <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-brand-400"></i>
      <p class="text-xs">Loading company hiring guides...</p>
    </div>
  `;

  let url = '/api/companies';
  if (selectedCompanySegment && selectedCompanySegment !== 'All') {
    url += `?category=${encodeURIComponent(selectedCompanySegment)}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();
    companiesList = data.companies || [];

    renderCompaniesGrid();
  } catch (err) {
    container.innerHTML = `<p class="col-span-full text-rose-400 text-xs py-4 text-center">Failed to load company guides.</p>`;
  }
}

function filterCompanies(segment) {
  selectedCompanySegment = segment;
  document.querySelectorAll('.comp-filter-pill').forEach(pill => {
    if (pill.textContent.trim().includes(segment === 'All' ? 'All' : segment.split('/')[0].trim())) {
      pill.className = 'comp-filter-pill active px-3.5 py-1.5 rounded-lg bg-brand-600 text-white font-medium';
    } else {
      pill.className = 'comp-filter-pill px-3.5 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 font-medium';
    }
  });
  fetchCompanies();
}

function renderCompaniesGrid() {
  const container = document.getElementById('companies-container');
  if (!container) return;

  if (!companiesList.length) {
    container.innerHTML = `
      <div class="col-span-full py-10 text-center text-slate-400 bg-slate-800/40 rounded-xl border border-slate-700">
        <p class="text-xs">No companies found in this category.</p>
      </div>
    `;
    return;
  }

  const compIcons = {
    'google': 'fa-brands fa-google text-red-400 bg-red-500/20',
    'amazon': 'fa-brands fa-amazon text-amber-400 bg-amber-500/20',
    'microsoft': 'fa-brands fa-microsoft text-sky-400 bg-sky-500/20',
    'tcs': 'fa-solid fa-microchip text-blue-400 bg-blue-500/20',
    'infosys': 'fa-solid fa-code text-indigo-400 bg-indigo-500/20',
    'flipkart': 'fa-solid fa-bag-shopping text-yellow-400 bg-yellow-500/20'
  };

  container.innerHTML = companiesList.map(c => {
    const iconClass = compIcons[c.slug] || 'fa-solid fa-building text-brand-400 bg-brand-500/20';

    const diffColors = {
      'Hard': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
      'Medium': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
      'Easy-Medium': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
    };

    const topicsPills = (c.frequently_asked_topics || []).slice(0, 3).map(t => 
      `<span class="px-2 py-0.5 rounded text-[11px] bg-slate-900 border border-slate-700 text-slate-300">${t}</span>`
    ).join('');

    return `
      <div class="bg-slate-800/80 hover:bg-slate-800 border border-slate-700 hover:border-violet-500/50 rounded-2xl p-5 transition-all shadow-md hover:shadow-xl flex flex-col justify-between space-y-4 group">
        
        <div class="space-y-3">
          <!-- Top Row -->
          <div class="flex items-start justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl font-bold shadow-inner ${iconClass.split(' ').slice(1).join(' ')}">
                <i class="${iconClass.split(' ')[0]} ${iconClass.split(' ')[1]}"></i>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white group-hover:text-violet-300 transition-colors">${c.name}</h3>
                <span class="text-[11px] font-semibold text-slate-400">${c.category}</span>
              </div>
            </div>
            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${diffColors[c.difficulty] || diffColors.Hard}">
              ${c.difficulty}
            </span>
          </div>

          <!-- CTC & Tagline -->
          <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">
            ${c.tagline}
          </p>

          <div class="bg-slate-900/60 p-2.5 rounded-lg border border-slate-700/60 flex items-center justify-between text-xs">
            <span class="text-slate-400">Typical Package:</span>
            <span class="font-bold text-emerald-400">${c.avg_salary}</span>
          </div>

          <!-- Frequently Asked Topics -->
          <div class="space-y-1">
            <span class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">High Frequency Topics:</span>
            <div class="flex flex-wrap gap-1">
              ${topicsPills}
            </div>
          </div>
        </div>

        <!-- Action Button -->
        <div class="pt-3 border-t border-slate-700/60">
          <button onclick="openCompanyGuide('${c.slug}')" class="w-full py-2 px-3 rounded-lg bg-violet-600 hover:bg-violet-500 text-white font-semibold text-xs flex items-center justify-center space-x-2 transition-all shadow-md shadow-violet-600/20">
            <i class="fa-solid fa-map-location-dot"></i>
            <span>View Full Hiring Roadmap</span>
          </button>
        </div>

      </div>
    `;
  }).join('');
}

async function openCompanyGuide(slug) {
  try {
    const res = await fetch(`/api/companies/${slug}`);
    currentViewingCompany = await res.json();
    const c = currentViewingCompany;

    document.getElementById('comp-modal-name').textContent = c.name;
    document.getElementById('comp-modal-category').textContent = c.category;
    document.getElementById('comp-modal-difficulty').textContent = c.difficulty;
    document.getElementById('comp-modal-tagline').textContent = c.tagline;

    // Render Exam Pattern & Rounds
    renderCompanyRounds(c.exam_pattern || []);

    // Render Eligibility & Syllabus
    renderCompanyEligibility(c.eligibility || {}, c.syllabus || {});

    // Render Questions & Tips
    renderCompanyQuestionsAndTips(c.sample_questions || [], c.tips || []);

    // Reset to tab 1
    switchCompTab('pattern');

    openModal('modal-company-guide');
  } catch (err) {
    showToast('Failed to open company guide', 'error');
  }
}

function switchCompTab(tab) {
  ['pattern', 'eligibility', 'questions'].forEach(t => {
    const btn = document.getElementById(`comptab-btn-${t}`);
    const pane = document.getElementById(`comptab-pane-${t}`);
    if (btn && pane) {
      if (t === tab) {
        btn.className = 'comp-inner-tab active px-4 py-2 border-b-2 border-brand-500 text-white font-semibold';
        pane.classList.remove('hidden');
      } else {
        btn.className = 'comp-inner-tab px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-white font-semibold';
        pane.classList.add('hidden');
      }
    }
  });
}

function renderCompanyRounds(rounds) {
  const container = document.getElementById('comp-modal-rounds');
  if (!container) return;

  container.innerHTML = rounds.map(r => `
    <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-700/80 space-y-2">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2.5">
          <span class="w-6 h-6 rounded-lg bg-brand-500/20 text-brand-300 flex items-center justify-center font-bold text-xs">
            ${r.round_num}
          </span>
          <h5 class="font-bold text-white text-sm">${r.name}</h5>
        </div>
        <div class="flex items-center space-x-2 text-xs">
          <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
            <i class="fa-regular fa-clock mr-1"></i>${r.duration}
          </span>
          <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
            ${r.platform || 'Online'}
          </span>
        </div>
      </div>
      <p class="text-xs text-slate-300 leading-relaxed"><strong class="text-slate-400">Format:</strong> ${r.questions}</p>
      <div class="text-xs text-brand-300 bg-brand-950/40 p-2 rounded-lg border border-brand-500/20">
        <strong>Key Focus:</strong> ${r.focus}
      </div>
    </div>
  `).join('');
}

function renderCompanyEligibility(elig, syll) {
  const eligContainer = document.getElementById('comp-modal-eligibility-details');
  if (eligContainer) {
    eligContainer.innerHTML = `
      <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
        <span class="text-slate-400 font-bold block mb-1">Academic CGPA Cutoff:</span>
        <span class="text-white">${elig.cgpa || '60% or 6.5 CGPA'}</span>
      </div>
      <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
        <span class="text-slate-400 font-bold block mb-1">Backlog Criteria:</span>
        <span class="text-white">${elig.backlogs || 'No active backlogs allowed'}</span>
      </div>
      <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
        <span class="text-slate-400 font-bold block mb-1">Eligible Branches:</span>
        <span class="text-white">${elig.branches || 'All Engineering & MCA'}</span>
      </div>
      <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
        <span class="text-slate-400 font-bold block mb-1">Graduation Batches:</span>
        <span class="text-white">${elig.batches || '2025, 2026 Batch'}</span>
      </div>
      <div class="sm:col-span-2 bg-slate-800/80 p-3 rounded-lg border border-slate-700">
        <span class="text-amber-400 font-bold block mb-1">Important Note:</span>
        <span class="text-slate-300">${elig.notes || 'Please verify exact eligibility with your campus placement cell.'}</span>
      </div>
    `;
  }

  const syllContainer = document.getElementById('comp-modal-syllabus');
  if (syllContainer) {
    const topics = syll.key_syllabus_topics || [];
    syllContainer.innerHTML = `
      <div class="space-y-2">
        <p class="text-xs text-slate-300 font-semibold mb-2">High-Priority Technical & Cognitive Syllabus:</p>
        <ul class="list-disc pl-5 space-y-1.5 text-slate-300">
          ${topics.map(t => `<li>${t}</li>`).join('')}
        </ul>
      </div>
    `;
  }
}

function renderCompanyQuestionsAndTips(questions, tips) {
  const qContainer = document.getElementById('comp-modal-sample-questions');
  if (qContainer) {
    qContainer.innerHTML = questions.map((q, idx) => `
      <div class="bg-slate-900/60 p-3 rounded-lg border border-slate-700/70 text-xs text-slate-200 flex items-start space-x-2">
        <span class="w-5 h-5 rounded bg-brand-500/20 text-brand-300 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">
          Q${idx + 1}
        </span>
        <span class="leading-relaxed font-medium">${q}</span>
      </div>
    `).join('');
  }

  const tipsContainer = document.getElementById('comp-modal-tips');
  if (tipsContainer) {
    tipsContainer.innerHTML = tips.map(t => `<li>${t}</li>`).join('');
  }
}
