// Main Application Controller: Routing, Navigation, Modals & Notifications

let currentTab = 'jobs';

function switchTab(tabId) {
  currentTab = tabId;

  // Update navbar state
  document.querySelectorAll('.nav-tab').forEach(btn => {
    btn.classList.remove('active');
  });
  const activeBtn = document.getElementById(`nav-btn-${tabId}`);
  if (activeBtn) activeBtn.classList.add('active');

  // Update panes
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.remove('active');
    pane.classList.add('hidden');
  });
  const activePane = document.getElementById(`tab-${tabId}`);
  if (activePane) {
    activePane.classList.remove('hidden');
    activePane.classList.add('active');
  }

  // Trigger tab-specific refresh if needed
  if (tabId === 'jobs') {
    fetchJobs();
  } else if (tabId === 'prep') {
    loadPrepData();
  } else if (tabId === 'companies') {
    fetchCompanies();
  } else if (tabId === 'dsa') {
    fetchDSAProblems();
    fetchDSATopics();
    fetchDSAStats();
  } else if (tabId === 'dashboard') {
    loadDashboardMetrics();
    loadDashboardApplications();
  }
}

// Modal handling
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

// Toast Notifications
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  const bgColors = {
    success: 'bg-emerald-600 text-white',
    error: 'bg-rose-600 text-white',
    info: 'bg-brand-600 text-white',
    warning: 'bg-amber-600 text-white'
  };
  const iconClasses = {
    success: 'fa-solid fa-circle-check',
    error: 'fa-solid fa-circle-xmark',
    info: 'fa-solid fa-circle-info',
    warning: 'fa-solid fa-triangle-exclamation'
  };

  toast.className = `toast-alert ${bgColors[type] || bgColors.success} flex items-center space-x-2 text-xs font-medium`;
  toast.innerHTML = `
    <i class="${iconClasses[type] || iconClasses.success} text-sm"></i>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Escape key closes open modals
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('[id^="modal-"]').forEach(modal => {
      if (!modal.classList.contains('hidden')) {
        closeModal(modal.id);
      }
    });
  }
});

// App Bootstrap
document.addEventListener('DOMContentLoaded', () => {
  // Initial load
  fetchJobs();
  updateHeaderCounts();
});

async function updateHeaderCounts() {
  try {
    const res = await fetch('/api/applications');
    const data = await res.json();
    const badge = document.getElementById('badge-applied-count');
    if (badge && data.count > 0) {
      badge.textContent = data.count;
      badge.classList.remove('hidden');
    }
  } catch (e) {
    console.error('Error fetching applications count:', e);
  }
}
