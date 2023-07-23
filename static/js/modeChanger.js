const savedTheme = localStorage.getItem('theme');

if (savedTheme) {
    document.body.classList.add(savedTheme);
    $('#moon-icon').toggle();
    $('#sun-icon').toggle();
}

function toggleTheme() {
    document.body.classList.toggle('dark-theme');

    if (document.body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark-theme');
    } else {
        localStorage.removeItem('theme');
    }
}

document.getElementById('theme-button').addEventListener('click', function() {
    toggleTheme();
    $('#moon-icon').toggle();
    $('#sun-icon').toggle();
});
