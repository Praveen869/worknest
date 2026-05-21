function showTab(tab) {
    document.getElementById('login-form').style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById('signup-form').style.display = tab === 'signup' ? 'block' : 'none';
    document.querySelectorAll('.tab-btn').forEach((btn, i) => {
        btn.classList.toggle('active', (i === 0 && tab === 'login') || (i === 1 && tab === 'signup'));
    });
}

async function login() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');
    errorEl.textContent = '';

    if (!email || !password) {
        errorEl.textContent = 'Please fill all fields';
        return;
    }

    try {
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            errorEl.textContent = data.error || 'Login failed';
            return;
        }

        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        window.location.href = '/dashboard';

    } catch (err) {
        errorEl.textContent = 'Server error. Try again.';
    }
}

async function signup() {
    const name = document.getElementById('signup-name').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    const role = document.getElementById('signup-role').value;
    const errorEl = document.getElementById('signup-error');
    errorEl.textContent = '';

    if (!name || !email || !password) {
        errorEl.textContent = 'Please fill all fields';
        return;
    }

    try {
        const res = await fetch('/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password, role })
        });

        const data = await res.json();

        if (!res.ok) {
            errorEl.textContent = data.error || 'Signup failed';
            return;
        }

        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        window.location.href = '/dashboard';

    } catch (err) {
        errorEl.textContent = 'Server error. Try again.';
    }
}