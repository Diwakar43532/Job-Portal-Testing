// Job Portal Controller

let selectedJobCategory = 'All';
let isBookmarkedOnly = false;
let currentJobsList = [];

// Company icon map
const companyIcons = {
  'google': { icon: 'fa-brands fa-google', bg: 'bg-red-500/20 text-red-400' },
  'amazon': { icon: 'fa-brands fa-amazon', bg: 'bg-amber-500/20 text-amber-400' },
  'microsoft': { icon: 'fa-brands fa-microsoft', bg: 'bg-sky-500/20 text-sky-400' },
  'tcs': { icon: 'fa-solid fa-microchip', bg: 'bg-blue-500/20 text-blue-400' },
  'infosys': { icon: 'fa-solid fa-code', bg: 'bg-indigo-500/20 text-indigo-400' },
  'razorpay': { icon: 'fa-solid fa-credit-card', bg: 'bg-blue-600/20 text-blue-400' },
  'swiggy': { icon: 'fa-solid fa-utensils', bg: 'bg-orange-500/20 text-orange-400' },
  'flipkart': { icon: 'fa-solid fa-bag-shopping', bg: 'bg-yellow-500/20 text-yellow-400' },
  'nvidia': { icon: 'fa-solid fa-microchip', bg: 'bg-emerald-500/20 text-emerald-400' },
  'wipro': { icon: 'fa-solid fa-laptop-code', bg: 'bg-purple-500/20 text-purple-400' },
  'atlassian': { icon: 'fa-brands fa-atlassian', bg: 'bg-blue-500/20 text-blue-400' },
  'cred': { icon: 'fa-solid fa-shield-halved', bg: 'bg-stone-500/20 text-stone-200' },
  'default': { icon: 'fa-solid fa-building', bg: 'bg-brand-500/20 text-brand-400' }
};

function getCompanyIconMeta(companyName) {
  const key = (companyName || '').toLowerCase().trim();
  for (const k in companyIcons) {
    if (key.includes(k)) return companyIcons[k];
  }
  return companyIcons.default;
}

async function fetchJobs() {
  const container = document.getElementById('jobs-container');
  if (!container) return;

  const search = document.getElementById('job-search-input')?.value.trim() || '';
  const location = document.getElementById('job-location-input')?.value.trim() || '';
  const jobType = document.getElementById('job-type-select')?.value || 'All';

  let url = `/api/jobs?`;
  const params = [];
  if (search) params.push(`search=${encodeURIComponent(search)}`);
  if (location) params.push(`location=${encodeURIComponent(location)}`);
  if (jobType && jobType !== 'All') params.push(`job_type=${encodeURIComponent(jobType)}`);
  if (selectedJobCategory && selectedJobCategory !== 'All') params.push(`category=${encodeURIComponent(selectedJobCategory)}`);
  if (isBookmarkedOnly) params.push(`bookmarked_only=true`);

  url += params.join('&');

  container.innerHTML = `
    <div class="col-span-full py-12 text-center text-slate-400">
      <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-brand-400"></i>
      <p class="text-sm">Fetching verified job openings...</p>
    </div>
  `;

  try {
    const res = await fetch(url);
    const data = await res.json();
    currentJobsList = data.jobs || [];

    const badge = document.getElementById('jobs-count-badge');
    if (badge) badge.textContent = currentJobsList.length;

    renderJobsGrid(currentJobsList);
  } catch (err) {
    console.error('Error fetching jobs:', err);
    container.innerHTML = `
      <div class="col-span-full py-8 text-center text-rose-400 bg-slate-800/60 rounded-xl border border-rose-500/30">
        <i class="fa-solid fa-triangle-exclamation text-2xl mb-2"></i>
        <p class="text-sm">Failed to load jobs. Please try refreshing.</p>
      </div>
    `;
  }
}

function renderJobsGrid(jobs) {
  const container = document.getElementById('jobs-container');
  if (!container) return;

  if (!jobs.length) {
    container.innerHTML = `
      <div class="col-span-full py-16 text-center text-slate-400 bg-slate-800/40 rounded-2xl border border-slate-700/60 space-y-3">
        <div class="w-12 h-12 mx-auto rounded-full bg-slate-800 flex items-center justify-center text-slate-500 text-xl">
          <i class="fa-solid fa-magnifying-glass"></i>
        </div>
        <h3 class="text-base font-semibold text-slate-300">No matching job openings found</h3>
        <p class="text-xs text-slate-500 max-w-sm mx-auto">Try clearing search filters or switching job categories.</p>
        <button onclick="clearJobFilters()" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-brand-600 text-white hover:bg-brand-500 transition-all">
          Reset Filters
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = jobs.map(j => {
    const iconMeta = getCompanyIconMeta(j.company);
    const skillsPills = (j.skills || []).slice(0, 4).map(s => 
      `<span class="px-2 py-0.5 rounded text-[11px] bg-slate-900/80 border border-slate-700 text-slate-300">${s}</span>`
    ).join('');

    const bookmarkActive = j.is_bookmarked ? 'text-amber-400 fa-solid' : 'text-slate-400 fa-regular';

    return `
      <div class="group relative bg-slate-800/80 hover:bg-slate-800 border border-slate-700 hover:border-brand-500/60 rounded-2xl p-5 transition-all duration-300 shadow-md hover:shadow-xl flex flex-col justify-between space-y-4">
        
        <!-- Header: Logo, Company, Title, Bookmark -->
        <div class="space-y-3">
          <div class="flex items-start justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-11 h-11 rounded-xl ${iconMeta.bg} flex items-center justify-center text-xl font-bold shadow-inner">
                <i class="${iconMeta.icon}"></i>
              </div>
              <div>
                <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">${j.company}</h4>
                <h3 class="text-base font-bold text-white group-hover:text-brand-300 transition-colors line-clamp-1">${j.title}</h3>
              </div>
            </div>
            <button onclick="toggleBookmark(${j.id}, event)" class="p-1.5 rounded-lg hover:bg-slate-700/80 transition-colors" title="Save Job">
              <i class="${bookmarkActive} fa-bookmark text-base"></i>
            </button>
          </div>

          <!-- Badges & CTC -->
          <div class="flex flex-wrap gap-1.5 text-[11px]">
            <span class="px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">
              <i class="fa-solid fa-money-bill-wave text-[10px] mr-1"></i>${j.salary}
            </span>
            <span class="px-2 py-1 rounded-md bg-slate-700/70 text-slate-300 border border-slate-600/50">
              <i class="fa-solid fa-location-dot text-[10px] mr-1"></i>${j.location}
            </span>
            <span class="px-2 py-1 rounded-md bg-slate-700/70 text-slate-300 border border-slate-600/50">
              <i class="fa-solid fa-user-clock text-[10px] mr-1"></i>${j.experience}
            </span>
          </div>

          <!-- Short Description -->
          <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">
            ${j.description}
          </p>

          <!-- Skills tags -->
          <div class="flex flex-wrap gap-1 pt-1">
            ${skillsPills}
          </div>
        </div>

        <!-- Footer Buttons -->
        <div class="pt-3 border-t border-slate-700/60 flex items-center justify-between text-xs">
          <span class="text-slate-400 text-[11px] flex items-center space-x-1">
            <i class="fa-solid fa-users text-slate-400"></i>
            <span>${j.applicant_count || 0} applied</span>
          </span>
          <div class="flex items-center space-x-2">
            <button onclick="openJobDetail(${j.id})" class="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 font-medium transition-all">
              Details
            </button>
            <button onclick="openApplyJob(${j.id})" class="px-3.5 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-semibold transition-all shadow-md shadow-brand-600/20">
              Apply
            </button>
          </div>
        </div>

      </div>
    `;
  }).join('');
}

function filterJobCategory(cat) {
  selectedJobCategory = cat;
  document.querySelectorAll('.job-cat-pill').forEach(pill => {
    if (pill.textContent.trim() === (cat === 'All' ? 'All Roles' : cat)) {
      pill.className = 'job-cat-pill active px-3 py-1 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30 whitespace-nowrap';
    } else {
      pill.className = 'job-cat-pill px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700 whitespace-nowrap hover:bg-slate-700';
    }
  });
  fetchJobs();
}

function toggleSavedJobsOnly() {
  isBookmarkedOnly = !isBookmarkedOnly;
  const btn = document.getElementById('btn-toggle-saved');
  if (btn) {
    if (isBookmarkedOnly) {
      btn.className = 'p-2.5 bg-amber-500 text-slate-900 font-bold rounded-lg text-sm transition-all shadow-md';
      showToast('Showing bookmarked openings only', 'info');
    } else {
      btn.className = 'p-2.5 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg text-sm transition-all';
      showToast('Showing all openings', 'info');
    }
  }
  fetchJobs();
}

function clearJobFilters() {
  const s = document.getElementById('job-search-input');
  const l = document.getElementById('job-location-input');
  const t = document.getElementById('job-type-select');
  if (s) s.value = '';
  if (l) l.value = '';
  if (t) t.value = 'All';
  selectedJobCategory = 'All';
  isBookmarkedOnly = false;
  fetchJobs();
}

async function toggleBookmark(jobId, event) {
  if (event) event.stopPropagation();
  try {
    const res = await fetch(`/api/jobs/${jobId}/bookmark`, { method: 'POST' });
    const data = await res.json();
    showToast(data.message, data.bookmarked ? 'success' : 'info');
    fetchJobs();
  } catch (err) {
    showToast('Failed to update bookmark', 'error');
  }
}

async function openJobDetail(jobId) {
  try {
    const res = await fetch(`/api/jobs/${jobId}`);
    const j = await res.json();

    const iconMeta = getCompanyIconMeta(j.company);
    const logoEl = document.getElementById('job-modal-logo');
    if (logoEl) {
      logoEl.className = `w-12 h-12 rounded-xl ${iconMeta.bg} flex items-center justify-center text-2xl font-bold`;
      logoEl.innerHTML = `<i class="${iconMeta.icon}"></i>`;
    }

    document.getElementById('job-modal-title').textContent = j.title;
    document.getElementById('job-modal-company').textContent = j.company;
    document.getElementById('job-modal-location').textContent = j.location;
    document.getElementById('job-modal-type').textContent = j.job_type;
    document.getElementById('job-modal-exp').textContent = j.experience;
    document.getElementById('job-modal-salary').textContent = j.salary;
    document.getElementById('job-modal-desc').textContent = j.description;

    // Requirements
    const reqList = document.getElementById('job-modal-reqs');
    reqList.innerHTML = (j.requirements || []).map(r => `<li>${r}</li>`).join('');

    // Skills
    const skillsDiv = document.getElementById('job-modal-skills');
    skillsDiv.innerHTML = (j.skills || []).map(s => 
      `<span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-brand-500/10 text-brand-300 border border-brand-500/30">${s}</span>`
    ).join('');

    // Set apply hidden ID
    document.getElementById('apply-job-id').value = j.id;

    openModal('modal-job-detail');
  } catch (err) {
    showToast('Error loading job details', 'error');
  }
}

function openApplyJob(jobId) {
  openJobDetail(jobId);
  setTimeout(() => {
    document.getElementById('form-job-apply')?.scrollIntoView({ behavior: 'smooth' });
    document.getElementById('apply-name')?.focus();
  }, 300);
}

async function submitJobApplication(event) {
  event.preventDefault();
  const jobId = document.getElementById('apply-job-id').value;
  const name = document.getElementById('apply-name').value.trim();
  const email = document.getElementById('apply-email').value.trim();
  const phone = document.getElementById('apply-phone').value.trim();
  const exp = parseFloat(document.getElementById('apply-exp').value) || 0.0;
  const resume = document.getElementById('apply-resume').value.trim();
  const portfolio = document.getElementById('apply-portfolio').value.trim();
  const cover = document.getElementById('apply-cover').value.trim();

  if (!name || !email || !phone) {
    showToast('Please fill all required fields', 'warning');
    return;
  }

  try {
    const res = await fetch(`/api/jobs/${jobId}/apply`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        candidate_name: name,
        candidate_email: email,
        candidate_phone: phone,
        experience_years: exp,
        resume_url: resume,
        portfolio_url: portfolio,
        cover_letter: cover
      })
    });
    const data = await res.json();
    if (res.ok) {
      showToast(data.message, 'success');
      closeModal('modal-job-detail');
      document.getElementById('form-job-apply').reset();
      updateHeaderCounts();
      fetchJobs();
    } else {
      showToast(data.detail || 'Application failed', 'error');
    }
  } catch (err) {
    showToast('Application submission failed', 'error');
  }
}

function openPostJobModal() {
  openModal('modal-post-job');
}

async function submitNewJob(event) {
  event.preventDefault();
  const title = document.getElementById('post-title').value.trim();
  const company = document.getElementById('post-company').value.trim();
  const category = document.getElementById('post-category').value;
  const location = document.getElementById('post-location').value.trim();
  const job_type = document.getElementById('post-type').value;
  const salary = document.getElementById('post-salary').value.trim() || 'Competitive';
  const experience = document.getElementById('post-exp').value.trim() || '0-2 years';
  const description = document.getElementById('post-desc').value.trim();
  const reqsRaw = document.getElementById('post-reqs').value.trim();
  const skillsRaw = document.getElementById('post-skills').value.trim();

  const requirements = reqsRaw.split(',').map(s => s.trim()).filter(Boolean);
  const skills = skillsRaw.split(',').map(s => s.trim()).filter(Boolean);

  try {
    const res = await fetch('/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title, company, category, location, job_type, salary, experience, description, requirements, skills
      })
    });
    const data = await res.json();
    if (res.ok) {
      showToast('New job opening published successfully!', 'success');
      closeModal('modal-post-job');
      document.getElementById('form-post-job').reset();
      fetchJobs();
    } else {
      showToast(data.detail || 'Failed to post job', 'error');
    }
  } catch (err) {
    showToast('Failed to post job opening', 'error');
  }
}
