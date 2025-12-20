const modals = document.querySelectorAll('.modal');
        const fecharBtns = document.querySelectorAll('.fechar');
        fecharBtns.forEach(btn => btn.onclick = () => btn.parentElement.parentElement.style.display = 'none');
        window.onclick = e => { if (e.target.classList.contains('modal')) e.target.style.display = 'none'; };

        document.getElementById('abrirModal').onclick = () => document.getElementById('modalNovoItem').style.display = 'flex';

        // BOTÕES EDITAR
        const editarBtns = document.querySelectorAll('.editar');
        editarBtns.forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const card = e.target.closest('.item-card');
                const id = card.dataset.id;
                const form = document.getElementById('formEditarItem');
                form.action = `/editar_relatorio/${id}`;
                document.getElementById('editNome').value = card.dataset.nome;
                document.getElementById('editEquipe').value = card.dataset.equipe;
                document.getElementById('editData').value = card.dataset.data;
                document.getElementById('editTexto').value = card.dataset.texto;
                document.getElementById('editAutoria').value = card.dataset.autoria;
                document.getElementById('modalEditarItem').style.display = 'flex';
            });
        });

        // BOTÕES EXCLUIR
        const excluirBtns = document.querySelectorAll('.excluir');
        excluirBtns.forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const card = e.target.closest('.item-card');
                const id = card.dataset.id;
                const form = document.getElementById('formExcluirItem');
                form.action = `/deletar_relatorio/${id}`;
                document.getElementById('modalExcluirItem').style.display = 'flex';
            });
        });