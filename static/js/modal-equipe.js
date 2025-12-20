 // Modais
        function abrirModal(nomeEquipe) {
            document.getElementById('modal-' + nomeEquipe).style.display = 'flex';
        }
        function fecharModal(nomeEquipe) {
            document.getElementById('modal-' + nomeEquipe).style.display = 'none';
        }
        window.onclick = e => {
            if (e.target.classList.contains('modal')) e.target.style.display = 'none';
        };