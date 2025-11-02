// Toggle Sidebar
        const navToggle = document.getElementById('navToggle');
        const sidebar = document.getElementById('sidebar');

        navToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
            navToggle.classList.toggle('active');
        });

        // Dark Mode Toggle
        const themeToggle = document.getElementById('themeToggle');
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
        });

        // Exemplo Chart.js
        const ctx1 = document.getElementById('chart1').getContext('2d');
        const chart1 = new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril'],
                datasets: [{
                    label: 'Usuários',
                    data: [12, 19, 3, 5],
                    backgroundColor: '#ffd700'
                }]
            },
            options: {
                responsive: true
            }
        });

        const ctx2 = document.getElementById('chart2').getContext('2d');
        const chart2 = new Chart(ctx2, {
            type: 'line',
            data: {
                labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril'],
                datasets: [{
                    label: 'Equipes Ativas',
                    data: [7, 11, 5, 8],
                    borderColor: '#00bfff',
                    tension: 0.3
                }]
            },
            options: {
                responsive: true
            }
        });