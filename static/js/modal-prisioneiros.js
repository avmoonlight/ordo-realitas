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

// ABRIR MODAL NOVO
const btnNovo = document.getElementById('abrirModal');
const modalNovo = document.getElementById('modalNovoUsuario');

btnNovo.addEventListener('click', () => {
    modalNovo.style.display = 'flex';
});

// FECHAR MODAIS
document.querySelectorAll('.fechar').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.closest('.modal').style.display = 'none';
    });
});

window.addEventListener('click', e => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// ====================
//  DETALHES DO PRISIONEIRO
// ====================
const cards = document.querySelectorAll('.usuario-card');

cards.forEach(card => {
    card.addEventListener('click', () => {

        // Preenche modal de detalhes
        document.getElementById('detalheNome').innerText = card.dataset.nome;
        document.getElementById('detalheIdade').innerText = card.dataset.idade;
        document.getElementById('detalheQuem').innerText = card.dataset.quem_prendeu;
        document.getElementById('detalhePerigo').innerText = card.dataset.grau_perigo;
        document.getElementById('detalheSocial').innerText = card.dataset.socializacao;
        document.getElementById('detalheReintegracao').innerText = card.dataset.reintegracao;
        document.getElementById('detalheLiberado').innerText = card.dataset.liberado;

        // ====================
        // EDITAR (DENTRO DO MODAL)
        // ====================
        document.getElementById('detalheEditar').onclick = (e) => {
            e.stopPropagation();

            const form = document.getElementById('formEditarUsuario');
            form.action = `/editar_prisioneiro/${card.dataset.id}`;

            document.getElementById('editNome').value = card.dataset.nome || '';
            document.getElementById('editIdade').value = card.dataset.idade || '';
            document.getElementById('editQuem').value = card.dataset.quem_prendeu || '';
            document.getElementById('editPerigo').value = card.dataset.grau_perigo || '';
            document.getElementById('editSocial').value = card.dataset.socializacao || '';
            document.getElementById('editReintegracao').value = card.dataset.reintegracao || '';
            document.getElementById('editLiberado').value = card.dataset.liberado || '';

            document.getElementById('modalEditarUsuario').style.display = 'flex';
            document.getElementById('modalDetalhesAgente').style.display = 'none';
        };

        // ====================
        // EXCLUIR (DENTRO DO MODAL)
        // ====================
        document.getElementById('detalheExcluir').onclick = (e) => {
            e.stopPropagation();

            const form = document.getElementById('formExcluirUsuario');
            form.action = `/deletar_prisioneiro/${card.dataset.id}`;

            document.getElementById('modalExcluirUsuario').style.display = 'flex';
            document.getElementById('modalDetalhesAgente').style.display = 'none';
        };

        // Abre modal
        document.getElementById('modalDetalhesAgente').style.display = 'flex';
    });
});