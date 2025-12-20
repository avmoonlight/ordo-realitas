 // ===== MODAIS =====
        const modals = document.querySelectorAll('.modal');
        const fecharBtns = document.querySelectorAll('.fechar');
        fecharBtns.forEach(btn => btn.onclick = () => btn.parentElement.parentElement.style.display = 'none');
        window.onclick = e => { if (e.target.classList.contains('modal')) e.target.style.display = 'none'; };

        // Modal Novo
        document.getElementById('abrirModal').onclick = () => document.getElementById('modalNovoUsuario').style.display = 'flex';

        // Modal Editar
        const editarBtns = document.querySelectorAll('.editar');
        editarBtns.forEach(btn => {
            btn.addEventListener('click', e => {
                const card = e.target.closest('.usuario-card');
                const id = card.dataset.id;
                const username = card.dataset.username;
                const form = document.getElementById('formEditarUsuario');
                form.action = `/usuarios/editar/${id}`;
                document.getElementById('editUsername').value = username;
                document.getElementById('modalEditarUsuario').style.display = 'flex';
            });
        });

        // Modal Excluir
        const excluirBtns = document.querySelectorAll('.excluir');
        excluirBtns.forEach(btn => {
            btn.addEventListener('click', e => {
                const card = e.target.closest('.usuario-card');
                const id = card.dataset.id;
                const form = document.getElementById('formExcluirUsuario');
                form.action = `/usuarios/deletar/${id}`;
                document.getElementById('modalExcluirUsuario').style.display = 'flex';
            });
        });