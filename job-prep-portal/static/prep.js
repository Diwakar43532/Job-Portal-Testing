// Preparation Hub Controller: Notes & Interactive Practice Quizzes

let selectedPrepCategory = 'Aptitude';
let currentPrepMode = 'notes'; // 'notes' or 'quiz'
let currentQuestionsList = [];
let userQuizScore = { total: 0, attempted: 0, correct: 0 };

function selectPrepCategory(category) {
  selectedPrepCategory = category;

  // Highlight active category card
  ['Aptitude', 'Technical', 'HR'].forEach(cat => {
    const card = document.getElementById(`prep-card-${cat}`);
    if (card) {
      if (cat === category) {
        card.classList.add('active', 'border-brand-500');
        card.classList.remove('border-slate-700');
      } else {
        card.classList.remove('active', 'border-brand-500');
        card.classList.add('border-slate-700');
      }
    }
  });

  loadPrepData();
}

function setPrepMode(mode) {
  currentPrepMode = mode;
  const btnNotes = document.getElementById('prep-mode-notes');
  const btnQuiz = document.getElementById('prep-mode-quiz');
  const notesContainer = document.getElementById('prep-notes-container');
  const quizContainer = document.getElementById('prep-quiz-container');
  const quizScoreBadge = document.getElementById('quiz-score-badge');

  if (mode === 'notes') {
    btnNotes.className = 'px-4 py-2 rounded-lg text-xs font-bold bg-brand-600 text-white transition-all flex items-center space-x-2';
    btnQuiz.className = 'px-4 py-2 rounded-lg text-xs font-bold text-slate-300 hover:text-white transition-all flex items-center space-x-2';
    notesContainer.classList.remove('hidden');
    quizContainer.classList.add('hidden');
    if (quizScoreBadge) quizScoreBadge.classList.add('hidden');
    loadPrepNotes();
  } else {
    btnQuiz.className = 'px-4 py-2 rounded-lg text-xs font-bold bg-brand-600 text-white transition-all flex items-center space-x-2';
    btnNotes.className = 'px-4 py-2 rounded-lg text-xs font-bold text-slate-300 hover:text-white transition-all flex items-center space-x-2';
    quizContainer.classList.remove('hidden');
    notesContainer.classList.add('hidden');
    if (quizScoreBadge) quizScoreBadge.classList.remove('hidden');
    loadPrepQuiz();
  }
}

function loadPrepData() {
  if (currentPrepMode === 'notes') {
    loadPrepNotes();
  } else {
    loadPrepQuiz();
  }
}

// -------------------------------------------------------------
// Notes & Cheatsheets
// -------------------------------------------------------------
async function loadPrepNotes() {
  const container = document.getElementById('prep-notes-container');
  if (!container) return;

  container.innerHTML = `
    <div class="py-12 text-center text-slate-400">
      <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-brand-400"></i>
      <p class="text-xs">Loading comprehensive study notes...</p>
    </div>
  `;

  try {
    const res = await fetch(`/api/prep/topics?category=${encodeURIComponent(selectedPrepCategory)}`);
    const data = await res.json();
    const topics = data.topics || [];

    if (!topics.length) {
      container.innerHTML = `
        <div class="py-10 text-center text-slate-400 bg-slate-800/40 rounded-xl border border-slate-700">
          <p class="text-xs">No notes found for this category.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        ${topics.map(t => `
          <div class="bg-slate-800/80 hover:bg-slate-800 border border-slate-700 hover:border-brand-500/50 rounded-xl p-5 transition-all flex flex-col justify-between space-y-3 group shadow-md">
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-slate-700 text-brand-300 border border-slate-600/50">
                  ${t.sub_category}
                </span>
                <span class="text-[11px] text-slate-400 flex items-center space-x-1">
                  <i class="fa-regular fa-clock text-[10px]"></i>
                  <span>${t.read_time}</span>
                </span>
              </div>
              <h3 class="text-base font-bold text-white group-hover:text-brand-300 transition-colors">
                ${t.title}
              </h3>
              <p class="text-xs text-slate-400 leading-relaxed line-clamp-2">
                ${t.summary}
              </p>
            </div>

            <div class="pt-3 border-t border-slate-700/60 flex items-center justify-between">
              <span class="text-[11px] text-slate-400 font-medium">Verified Cheatsheet</span>
              <button onclick="openNoteDetail(${t.id})" class="px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs flex items-center space-x-1.5 transition-all shadow-md shadow-brand-600/20">
                <i class="fa-solid fa-book-open text-[10px]"></i>
                <span>Read Notes</span>
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<p class="text-rose-400 text-xs py-4 text-center">Failed to load study notes.</p>`;
  }
}

async function openNoteDetail(topicId) {
  try {
    const res = await fetch(`/api/prep/topics/${topicId}`);
    const note = await res.json();

    document.getElementById('note-modal-category').textContent = `${note.category} • ${note.sub_category}`;
    document.getElementById('note-modal-time').textContent = note.read_time;
    document.getElementById('note-modal-title').textContent = note.title;

    // Render markdown safely
    const contentEl = document.getElementById('note-modal-content');
    if (typeof marked !== 'undefined') {
      contentEl.innerHTML = marked.parse(note.content || '');
    } else {
      contentEl.textContent = note.content;
    }

    // Trigger highlight.js code highlighting
    if (typeof hljs !== 'undefined') {
      contentEl.querySelectorAll('pre code').forEach((el) => {
        hljs.highlightElement(el);
      });
    }

    openModal('modal-prep-note');
  } catch (err) {
    showToast('Failed to load note content', 'error');
  }
}

// -------------------------------------------------------------
// Interactive Practice Quiz Engine
// -------------------------------------------------------------
async function loadPrepQuiz() {
  const container = document.getElementById('prep-quiz-container');
  if (!container) return;

  container.innerHTML = `
    <div class="py-12 text-center text-slate-400">
      <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-brand-400"></i>
      <p class="text-xs">Loading practice questions...</p>
    </div>
  `;

  try {
    const res = await fetch(`/api/prep/questions?category=${encodeURIComponent(selectedPrepCategory)}`);
    const data = await res.json();
    currentQuestionsList = data.questions || [];

    updateQuizScoreBadge();

    if (!currentQuestionsList.length) {
      container.innerHTML = `
        <div class="py-10 text-center text-slate-400 bg-slate-800/40 rounded-xl border border-slate-700">
          <p class="text-xs">No practice questions available for this category yet.</p>
        </div>
      `;
      return;
    }

    renderQuizQuestions();
  } catch (err) {
    container.innerHTML = `<p class="text-rose-400 text-xs py-4 text-center">Failed to load practice questions.</p>`;
  }
}

function updateQuizScoreBadge() {
  const badge = document.getElementById('quiz-score-badge');
  if (!badge) return;

  const attemptedCount = currentQuestionsList.filter(q => q.user_attempt).length;
  const correctCount = currentQuestionsList.filter(q => q.user_attempt && q.user_attempt.is_correct).length;
  const total = currentQuestionsList.length;

  badge.innerHTML = `
    <div class="flex items-center space-x-2 text-xs">
      <span class="text-slate-400">Answered: <strong class="text-white">${attemptedCount}/${total}</strong></span>
      <span class="text-slate-600">|</span>
      <span class="text-emerald-400 font-semibold">Correct: <strong>${correctCount}</strong></span>
    </div>
  `;
}

function renderQuizQuestions() {
  const container = document.getElementById('prep-quiz-container');
  if (!container) return;

  container.innerHTML = `
    <div class="space-y-4">
      ${currentQuestionsList.map((q, idx) => {
        const diffColors = {
          'Easy': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
          'Medium': 'bg-amber-500/10 text-amber-400 border-amber-500/20',
          'Hard': 'bg-rose-500/10 text-rose-400 border-rose-500/20'
        };

        const attempt = q.user_attempt;
        const isAttempted = attempt !== null;

        return `
          <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 space-y-4 shadow-md" id="q-card-${q.id}">
            
            <!-- Question header -->
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-2.5">
              <div class="flex items-center space-x-2">
                <span class="w-6 h-6 rounded-full bg-slate-700 text-white flex items-center justify-center text-xs font-bold">
                  ${idx + 1}
                </span>
                <span class="text-xs font-bold text-slate-300">${q.sub_category}</span>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${diffColors[q.difficulty] || diffColors.Easy}">
                  ${q.difficulty}
                </span>
              </div>
              <div class="flex items-center space-x-1">
                ${(q.tags || []).map(t => `<span class="text-[10px] bg-slate-900 px-2 py-0.5 rounded text-slate-400 border border-slate-700/60">${t}</span>`).join('')}
              </div>
            </div>

            <!-- Question statement -->
            <p class="text-sm font-medium text-white leading-relaxed">
              ${q.question}
            </p>

            <!-- Options grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
              ${q.options.map((opt, optIdx) => {
                let optClass = 'bg-slate-900/80 hover:bg-slate-700 border-slate-700 text-slate-200';
                let indicator = '';

                if (isAttempted) {
                  if (optIdx === attempt.selected_option) {
                    if (attempt.is_correct) {
                      optClass = 'bg-emerald-950/60 border-emerald-500 text-emerald-200 font-semibold';
                      indicator = '<i class="fa-solid fa-circle-check text-emerald-400 ml-auto"></i>';
                    } else {
                      optClass = 'bg-rose-950/60 border-rose-500 text-rose-200 font-semibold';
                      indicator = '<i class="fa-solid fa-circle-xmark text-rose-400 ml-auto"></i>';
                    }
                  }
                }

                const optLetters = ['A', 'B', 'C', 'D'];

                return `
                  <button 
                    onclick="submitQuizAnswer(${q.id}, ${optIdx})" 
                    ${isAttempted ? 'disabled' : ''} 
                    class="p-3 rounded-lg border text-left text-xs transition-all flex items-center space-x-2.5 ${optClass} ${isAttempted ? 'cursor-default' : 'cursor-pointer hover:border-brand-500'}">
                    <span class="w-5 h-5 rounded bg-slate-800 text-slate-300 font-bold flex items-center justify-center text-[10px] shrink-0 border border-slate-700">
                      ${optLetters[optIdx]}
                    </span>
                    <span class="flex-1">${opt}</span>
                    ${indicator}
                  </button>
                `;
              }).join('')}
            </div>

            <!-- Result Explanation (if already attempted) -->
            <div id="q-explanation-${q.id}" class="${isAttempted ? 'block' : 'hidden'} mt-3 bg-slate-900/90 p-3.5 rounded-lg border border-slate-700/80 text-xs text-slate-300 space-y-1">
              <span class="font-bold text-amber-400 block flex items-center space-x-1.5">
                <i class="fa-solid fa-lightbulb text-[11px]"></i>
                <span>Explanation & Detailed Logic:</span>
              </span>
              <p id="q-exp-text-${q.id}" class="text-slate-300 leading-relaxed">${q.explanation || ''}</p>
            </div>

          </div>
        `;
      }).join('')}
    </div>
  `;
}

async function submitQuizAnswer(questionId, selectedOption) {
  try {
    const res = await fetch(`/api/prep/questions/${questionId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ selected_option: selectedOption })
    });
    const result = await res.json();

    // Update local state
    const targetQ = currentQuestionsList.find(q => q.id === questionId);
    if (targetQ) {
      targetQ.user_attempt = {
        selected_option: selectedOption,
        is_correct: result.is_correct
      };
      targetQ.explanation = result.explanation;
    }

    if (result.is_correct) {
      showToast('Correct answer! +1 point', 'success');
    } else {
      showToast('Incorrect. Review the detailed explanation below.', 'warning');
    }

    updateQuizScoreBadge();
    renderQuizQuestions();
  } catch (err) {
    showToast('Failed to record answer', 'error');
  }
}
