// Validate and handle registration form
async function submitSignup() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const idNumber = document.getElementById('idNumber').value.trim();
    const language = document.getElementById('language').value;
    const password = document.getElementById('password').value;
    if (!name || !email || !phone || !idNumber || !language || !password) {
        alert('Please fill all fields!');
        return;
    }
    try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, email, phone, idNumber, language, password})
        });
        const data = await response.json();
        alert(data.message);
        if (data.success) {
            window.location.href = 'login.html';
        }
    } catch (error) {
        alert('Registration failed: ' + error);
    }
}
