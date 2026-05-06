document.querySelectorAll('.editar').forEach(btn => {
    btn.addEventListener('click', () => {

        const card = btn.closest('.usuario-card');
        const id = card.dataset.id;

        // Define rota
        document.getElementById('formEditarUsuario').action = `/editar_prisioneiro/${id}`;

        // Preenche campos
        document.getElementById('editNome').value = card.dataset.nome || '';
        document.getElementById('editIdade').value = card.dataset.idade || '';
        document.getElementById('editQuem').value = card.dataset.quem_prendeu || '';
        document.getElementById('editPerigo').value = card.dataset.grau_perigo || '';
        document.getElementById('editSocial').value = card.dataset.socializacao || '';
        document.getElementById('editReintegracao').value = card.dataset.reintegracao || '';
        document.getElementById('editLiberado').value = card.dataset.liberado || '';

        // Abre modal
        document.getElementById('modalEditarUsuario').style.display = 'flex';
    });
});

document.querySelectorAll('.excluir').forEach(btn => {
    btn.addEventListener('click', () => {
        const id = btn.closest('.usuario-card').dataset.id;
        document.getElementById('formExcluirUsuario').action = `/deletar_prisioneiro/${id}`;
        document.getElementById('modalExcluirUsuario').style.display = 'flex';
    });
});