const hamburger = document.getElementById('hamburger');
const sidebar = document.getElementById('sidebar');

hamburger.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
    hamburger.classList.toggle('active');
});

/* GRÁFICOS */
const purple = '#9b59b6';

new Chart(monstrosChart, {
    type: 'bar',
    data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
        datasets: [{
            data: [5, 9, 7, 12, 8],
            backgroundColor: 'rgba(155,89,182,0.4)'
        }]
    },
    options: { plugins: { legend: { display: false } } }
});

new Chart(mortesChart, {
    type: 'line',
    data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
        datasets: [{
            data: [2, 3, 1, 4, 2],
            borderColor: purple,
            tension: 0.3,
            fill: true,
            backgroundColor: 'rgba(155,89,182,0.2)'
        }]
    },
    options: { plugins: { legend: { display: false } } }
});

new Chart(atividadeChart, {
    type: 'doughnut',
    data: {
        labels: ['Baixa', 'Média', 'Alta'],
        datasets: [{
            data: [25, 40, 35],
            backgroundColor: ['#6a1b9a', '#8e24aa', '#b388ff']
        }]
    }
});

new Chart(missoesChart, {
    type: 'radar',
    data: {
        labels: ['Campo', 'Urbano', 'Floresta', 'Costeiro', 'Subterrâneo'],
        datasets: [{
            data: [8, 6, 7, 4, 5],
            borderColor: purple,
            backgroundColor: 'rgba(155,89,182,0.3)'
        }]
    }
});
