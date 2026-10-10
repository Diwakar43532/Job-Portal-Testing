// Candidate Dashboard & Application Tracker Controller

async function loadDashboardMetrics() {
  const container = document.getElementById('dashboard-metric-cards');
  if (!container) return;

  try {
    const res = await fetch('/api/dashboard/stats');
    const d = await res.json();

    container.innerHTML = `
      <!-- Readiness Score -->
      <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-md flex items-center justify-between">
        <div>
          <span class="text-xs text-slate-400 font-semibold block uppercase">Interview Readiness</span>
          <span class="text-2xl font-extrabold text-brand-400 mt-1 block">${d.readiness_score}%</span>
          <span class="text-[11px] text-slate-500 mt-0.5 block">DSA + Quizzes combined</span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-brand-500/20 text-brand-400 flex items-center justify-center text-xl">
          <i class="fa-solid fa-gauge-high"></i>
        </div>
      </div>

      <!-- DSA Solved -->
      <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-md flex items-center justify-between">
        <div>
          <span class="text-xs text-slate-400 font-semibold block uppercase">DSA Progress</span>
          <span class="text-2xl font-extrabold text-emerald-400 mt-1 block">${d.dsa_solved} / ${d.dsa_total}</span>
          <span class="text-[11px] text-slate-500 mt-0.5 block">${d.dsa_percentage}% completed</span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xl">
          <i class="fa-solid fa-code"></i>
        </div>
      </div>

      <!-- Quiz Accuracy -->
      <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-md flex items-center justify-between">
        <div>
          <span class="text-xs text-slate-400 font-semibold block uppercase">Quiz Accuracy</span>
          <span class="text-2xl font-extrabold text-amber-400 mt-1 block">${d.quizzes_accuracy}%</span>
          <span class="text-[11px] text-slate-500 mt-0.5 block">${d.quizzes_attempted} tests taken</span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-xl">
          <i class="fa-solid fa-brain"></i>
        </div>
      </div>

      <!-- Applications Sent -->
      <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-md flex items-center justify-between">
        <div>
          <span class="text-xs text-slate-400 font-semibold block uppercase">Applications</span>
          <span class="text-2xl font-extrabold text-blue-400 mt-1 block">${d.applications_submitted}</span>
          <span class="text-[11px] text-slate-500 mt-0.5 block">${d.saved_jobs} bookmarked jobs</span>
        </div>
        <div class="w-12 h-12 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center text-xl">
          <i class="fa-solid fa-paper-plane"></i>
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Error loading dashboard metrics:', err);
  }
}

async function loadDashboardApplications() {
  const container = document.getElementById('applications-table-container');
  if (!container) return;

  container.innerHTML = `
    <div class="py-10 text-center text-slate-400">
      <i class="fa-solid fa-spinner fa-spin text-xl mb-2 text-brand-400"></i>
      <p class="text-xs">Loading submitted applications...</p>
    </div>
  `;

  try {
    const res = await fetch('/api/applications');
    const data = await res.json();
    const apps = data.applications || [];

    if (!apps.length) {
      container.innerHTML = `
        <div class="py-12 text-center text-slate-400 bg-slate-900/40 rounded-xl border border-slate-700/60 space-y-2">
          <i class="fa-solid fa-inbox text-3xl text-slate-600 mb-1"></i>
          <h4 class="text-sm font-bold text-slate-300">No applications submitted yet</h4>
          <p class="text-xs text-slate-500 max-w-sm mx-auto">Explore verified tech openings on the Job Portal and submit your profile in one click.</p>
          <button onclick="switchTab('jobs')" class="mt-2 px-3.5 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs transition-all">
            Browse Job Openings
          </button>
        </div>
      `;
      return;
    }

    const statusBadge = {
      'Applied': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
      'Reviewing': 'bg-amber-500/10 text-amber-400 border-amber-500/20',
      'Shortlisted': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      'Interview': 'bg-purple-500/10 text-purple-400 border-purple-500/20',
      'Offer': 'bg-teal-500/10 text-teal-300 border-teal-500/20'
    };

    container.innerHTML = `
      <table class="w-full text-left text-xs text-slate-300">
        <thead class="bg-slate-900/80 text-[11px] uppercase font-semibold text-slate-400 border-b border-slate-700 tracking-wider">
          <tr>
            <th class="py-3 px-4">Role & Company</th>
            <th class="py-3 px-4">Location & CTC</th>
            <th class="py-3 px-4">Candidate Name</th>
            <th class="py-3 px-4">Applied Date</th>
            <th class="py-3 px-4 text-center">Status</th>
            <th class="py-3 px-4 text-center">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-700/60">
          ${apps.map(a => `
            <tr class="hover:bg-slate-700/30 transition-colors">
              <td class="py-3 px-4">
                <div class="font-bold text-white">${a.job_title}</div>
                <div class="text-slate-400">${a.job_company}</div>
              </td>
              <td class="py-3 px-4">
                <div>${a.location}</div>
                <div class="text-emerald-400 font-semibold">${a.salary}</div>
              </td>
              <td class="py-3 px-4">
                <div class="text-slate-200 font-medium">${a.candidate_name}</div>
                <div class="text-slate-500">${a.candidate_email}</div>
              </td>
              <td class="py-3 px-4 text-slate-400">
                ${a.applied_at}
              </td>
              <td class="py-3 px-4 text-center">
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${statusBadge[a.status] || statusBadge.Applied}">
                  ${a.status}
                </span>
              </td>
              <td class="py-3 px-4 text-center">
                <button onclick="openJobDetail(${a.job_id})" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-medium transition-all" title="View Job Description">
                  View Job
                </button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } catch (err) {
    container.innerHTML = `<p class="text-rose-400 text-xs py-4 text-center">Failed to load applications.</p>`;
  }
}
