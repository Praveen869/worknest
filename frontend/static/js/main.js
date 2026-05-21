const API = '';

function getToken() {
    return localStorage.getItem('token');
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}

function isAdmin() {
    const user = getUser();
    return user && user.role === 'admin';
}

function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

function setupUserInfo() {
    const user = getUser();
    if (user) {
        document.getElementById('user-info').innerHTML = `
            <strong style="color:white">${user.name}</strong><br>
            <span class="badge badge-${user.role}">${user.role}</span>
        `;
        document.getElementById('user-name') &&
            (document.getElementById('user-name').textContent = user.name);
    }
    // Hide admin-only elements for members
    if (!isAdmin()) {
        document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'none');
    }
}

async function apiFetch(url, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
    };
    const res = await fetch(API + url, { ...options, headers });
    if (res.status === 401 || res.status === 422) {
        logout();
        return null;
    }
    return res;
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function isOverdue(dateStr, status) {
    if (!dateStr || status === 'done') return false;
    return new Date(dateStr) < new Date();
}

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname !== '/login') {
        checkAuth();
        setupUserInfo();
    }
});