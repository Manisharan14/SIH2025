// Validate and handle login form
async function validateLogin() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    if (!email || !password) {
        alert('Please enter both email and password!');
        return;
    }
    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });
        const data = await response.json();
        alert(data.message);
        if (data.success) {
            window.location.href = '/';
        }
    } catch (error) {
        alert('Login failed: ' + error);
    }
}
