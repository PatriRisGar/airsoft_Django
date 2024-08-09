document.addEventListener('DOMContentLoaded', function () {
	const inputs = document.querySelectorAll('input');

	for (const input of inputs) {
		if (input.type != 'radio' && input.type != 'checkbox' && input.type != 'select') {
			input.classList.add('form-control');
		}
		if (input.type == 'select') {
			input.classList.add('form-select');
		}
	}
});
