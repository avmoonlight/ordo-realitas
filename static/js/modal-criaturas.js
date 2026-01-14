// Modais
        const modals = document.querySelectorAll('.modal');
        const fecharBtns = document.querySelectorAll('.fechar');
        fecharBtns.forEach(btn => btn.onclick = () => btn.parentElement.parentElement.style.display = 'none');
        window.onclick = e => { if (e.target.classList.contains('modal')) e.target.style.display = 'none'; };

        document.getElementById('abrirModal').onclick = () => document.getElementById('modalNovaCriatura').style.display = 'flex';

        // BOTÕES EDITAR
        const editarBtns = document.querySelectorAll('.editar');
        editarBtns.forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const card = e.target.closest('.criatura-card');
                const id = card.dataset.id;
                const form = document.getElementById('formEditarCriatura');
                form.action = `/editar_criatura/${id}`;
                document.getElementById('editNome').value = card.dataset.nome;
                document.getElementById('editElemento').value = card.dataset.elemento;
                document.getElementById('editLocal').value = card.dataset.local;
                document.getElementById('editDescricao').value = card.dataset.descricao;
                document.getElementById('editRaridade').value = card.dataset.raridade;
                document.getElementById('modalEditarCriatura').style.display = 'flex';
            });
        });

        // BOTÕES EXCLUIR
        const excluirBtns = document.querySelectorAll('.excluir');
        excluirBtns.forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const card = e.target.closest('.criatura-card');
                const id = card.dataset.id;
                const form = document.getElementById('formExcluirCriatura');
                form.action = `/deletar_criatura/${id}`;
                document.getElementById('modalExcluirCriatura').style.display = 'flex';
            });
        });

// ====================
//  DETALHES DA CRIATURA
// ====================
document.querySelectorAll('.criatura-card').forEach(card => {
    card.addEventListener('click', () => {

        document.getElementById('detalheNome').innerText = card.dataset.nome;
        document.getElementById('detalheElemento').innerText = card.dataset.elemento;
        document.getElementById('detalheLocal').innerText = card.dataset.local;
        document.getElementById('detalheDescricao').innerText = card.dataset.descricao;
        document.getElementById('detalheRaridade').innerText = card.dataset.raridade;

        // EDITAR
        document.getElementById('detalheEditar').onclick = e => {
            e.stopPropagation();
            const form = document.getElementById('formEditarCriatura');
            form.action = `/editar_criatura/${card.dataset.id}`;

            document.getElementById('editNome').value = card.dataset.nome;
            document.getElementById('editElemento').value = card.dataset.elemento;
            document.getElementById('editLocal').value = card.dataset.local;
            document.getElementById('editDescricao').value = card.dataset.descricao;
            document.getElementById('editRaridade').value = card.dataset.raridade;

            document.getElementById('modalEditarCriatura').style.display = 'flex';
            document.getElementById('modalDetalhesCriatura').style.display = 'none';
        };

        // EXCLUIR
        document.getElementById('detalheExcluir').onclick = e => {
            e.stopPropagation();
            const form = document.getElementById('formExcluirCriatura');
            form.action = `/deletar_criatura/${card.dataset.id}`;

            document.getElementById('modalExcluirCriatura').style.display = 'flex';
            document.getElementById('modalDetalhesCriatura').style.display = 'none';
        };

        document.getElementById('modalDetalhesCriatura').style.display = 'flex';
    });
});

        // ====================
//  FILTRO DE PESQUISA
// ====================
const barraPesquisa = document.getElementById('barraPesquisa');

barraPesquisa.addEventListener('keyup', () => {
    const termo = barraPesquisa.value.toLowerCase();
    const cards = document.querySelectorAll('.usuario-card');

    cards.forEach(card => {
        const nome = card.dataset.nome.toLowerCase();
        const sobrenome = card.dataset.sobrenome.toLowerCase();
        const nomeCompleto = `${nome} ${sobrenome}`;

        card.style.display = nomeCompleto.includes(termo) ? 'block' : 'none';
    });
});