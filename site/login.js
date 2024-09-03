const username = document.getElementById('username');
const password = document.getElementById('password');
const submit = document.getElementById('submit');
const congrats = document.getElementById('congrats');

username.disabled = true;
password.disabled = true;
submit.disabled = true;

function checkFlag() {
	if (sessionStorage.getItem('ok') == 'ok') {
		username.disabled = false;
		password.disabled = false;
		submit.disabled = false;
		congrats.classList.remove('disabled');
	}
}

window.setInterval(checkFlag, 100);
