const AUTH_LOGIN_KEY = 'ttt_login';
const AUTH_PASS_KEY = 'ttt_password';

function saveCredentials(login, password) {
    sessionStorage.setItem(AUTH_LOGIN_KEY, login);
    sessionStorage.setItem(AUTH_PASS_KEY, password);
}

function clearCredentials() {
    sessionStorage.removeItem(AUTH_LOGIN_KEY);
    sessionStorage.removeItem(AUTH_PASS_KEY);
}

function getCredentials() {
    const login = sessionStorage.getItem(AUTH_LOGIN_KEY);
    const password = sessionStorage.getItem(AUTH_PASS_KEY);
    if (!login || !password) return null;
    return { login, password };
}

function isLoggedIn() {
    return getCredentials() !== null;
}

/** Заголовок Authorization: Basic ... для fetch */
function authHeader() {
    const creds = getCredentials();
    if (!creds) return {};
    const token = btoa(creds.login + ':' + creds.password);
    return { 'Authorization': 'Basic ' + token };
}

/** fetch с JSON + Basic Auth */
async function apiFetch(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...authHeader(),
        ...(options.headers || {})
    };
    const response = await fetch(url, { ...options, headers });
    let body = null;
    const text = await response.text();
    if (text) {
        try { body = JSON.parse(text); } catch { body = text; }
    }
    return { response, body };
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/index.html';
    }
}

function logout() {
    if (typeof stopWaitPoll === 'function') stopWaitPoll();
    clearCredentials();
    sessionStorage.removeItem('ttt_userId');
    window.location.href = '/index.html';
}
