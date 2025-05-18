function getCSRFToken() {
    const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
    if (!match) throw new Error('CSRF token not found in cookies');
    return match[2];
}