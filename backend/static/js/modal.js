document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('modal-overlay');
  const content = document.getElementById('modal-content');
  const closeBtn = document.getElementById('modal-close');

  // Close modal
  const closeModal = () => overlay.classList.add('hidden');
  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal();
  });

  // Helper: open modal with fetched form
  const openFormModal = (url) => {
    fetch(url)
      .then(res => res.text())
      .then(html => {
        content.innerHTML = html;
        overlay.classList.remove('hidden');

        // Intercept the form submission
        const form = content.querySelector('form');
        if (form) {
          form.addEventListener('submit', (ev) => {
            ev.preventDefault();

            fetch(url, {
              method: 'POST',
              body: new FormData(form),
              headers: { 'X-Requested-With': 'XMLHttpRequest' },
            })
            .then(resp => {
              if (resp.redirected) {
                window.location.href = resp.url; // refresh list after success
              } else {
                return resp.text().then(html => {
                  content.innerHTML = html; // re-render form with errors
                });
              }
            });
          });
        }
      });
  };

  // Hook buttons
  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-add, .btn-edit, .btn-delete');
    if (btn) {
      e.preventDefault();
      const url = btn.getAttribute('href');
      openFormModal(url);
    }
  });
});

