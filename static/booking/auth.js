document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-password-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const targetId = button.getAttribute('data-target');
      const input = targetId ? document.getElementById(targetId) : null;
      if (!input) {
        return;
      }

      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      button.textContent = isPassword
        ? button.getAttribute('data-hide-text') || 'Hide'
        : button.getAttribute('data-show-text') || 'Show';
    });
  });

  document.querySelectorAll('[data-loading-form]').forEach((form) => {
    form.addEventListener('submit', () => {
      const submitButton = form.querySelector('button[type="submit"]');
      if (!submitButton) {
        return;
      }

      const loadingText = submitButton.getAttribute('data-loading-text');
      if (loadingText) {
        submitButton.textContent = loadingText;
      }
      submitButton.disabled = true;
      submitButton.setAttribute('aria-busy', 'true');
    });
  });
});
