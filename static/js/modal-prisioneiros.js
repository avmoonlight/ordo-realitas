// ==============================
// ELEMENTOS
// ==============================
const modalNovo = document.getElementById('modalNovoUsuario');
const modalEditar = document.getElementById('modalEditarUsuario');
const modalExcluir = document.getElementById('modalExcluirUsuario');

const btnAbrirModal = document.getElementById('abrirModal');


// ==============================
// ABRIR MODAL NOVO
// ==============================
if (btnAbrirModal && modalNovo) {
    btnAbrirModal.addEventListener('click', () => {
        modalNovo.style.display = 'flex';
    });
}


// ==============================
// EDITAR PRISIONEIRO
// ==============================
document.querySelectorAll('.editar').forEach(btn => {
    btn.addEventListener('click', () => {

        const card = btn.closest('.usuario-card');
        if (!card) return;

        const id = card.dataset.id;

        const form = document.getElementById('formEditarUsuario');
        if (form) {
            form.action = `/editar_prisioneiro/${id}`;
        }

        // Preencher campos com segurança
        const setValue = (id, value) => {
            const el = document.getElementById(id);
            if (el) el.value = value || '';
        };

        setValue('editNome', card.dataset.nome);
        setValue('editIdade', card.dataset.idade);
        setValue('editQuem', card.dataset.quem_prendeu);
        setValue('editPerigo', card.dataset.grau_perigo);
        setValue('editSocial', card.dataset.socializacao);
        setValue('editReintegracao', card.dataset.reintegracao);
        setValue('editLiberado', card.dataset.liberado);

        if (modalEditar) {
            modalEditar.style.display = 'flex';
        }
    });
});


// ==============================
// EXCLUIR PRISIONEIRO
// ==============================
document.querySelectorAll('.excluir').forEach(btn => {
    btn.addEventListener('click', () => {

        const card = btn.closest('.usuario-card');
        if (!card) return;

        const id = card.dataset.id;

        const form = document.getElementById('formExcluirUsuario');
        if (form) {
            form.action = `/deletar_prisioneiro/${id}`;
        }

        if (modalExcluir) {
            modalExcluir.style.display = 'flex';
        }
    });
});


// ==============================
// FECHAR MODAIS (BOTÃO X)
// ==============================
document.querySelectorAll('.fechar').forEach(btn => {
    btn.addEventListener('click', () => {
        const modal = btn.closest('.modal');
        if (modal) modal.style.display = 'none';
    });
});


// ==============================
// FECHAR CLICANDO FORA
// ==============================
window.addEventListener('click', (e) => {
    [modalNovo, modalEditar, modalExcluir].forEach(modal => {
        if (modal && e.target === modal) {
            modal.style.display = 'none';
        }
    });
});


// ==============================
// FECHAR COM ESC
// ==============================
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        [modalNovo, modalEditar, modalExcluir].forEach(modal => {
            if (modal) modal.style.display = 'none';
        });
    }
});