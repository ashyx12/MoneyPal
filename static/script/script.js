document.addEventListener('DOMContentLoaded', (event) => {
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.querySelector('input[type="password"]');

    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }
});