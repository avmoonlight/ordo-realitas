// Modais
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
                form.action = `/editar_item/${id}`;
                document.getElementById('editNome').value = card.dataset.nome;
                document.getElementById('editElemento').value = card.dataset.elemento;
                document.getElementById('editEfeito').value = card.dataset.efeito;
                document.getElementById('editNum').value = card.dataset.num_categorico;
                document.getElementById('editRaridade').value = card.dataset.raridade;
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
                form.action = `/deletar_item/${id}`;
                document.getElementById('modalExcluirItem').style.display = 'flex';
            });
        });

// ====================
//  DETALHES DO ITEM
// ====================
document.querySelectorAll('.item-card').forEach(card => {
    card.addEventListener('click', () => {

        document.getElementById('detalheNome').innerText = card.dataset.nome;
        document.getElementById('detalheElemento').innerText = card.dataset.elemento;
        document.getElementById('detalheEfeito').innerText = card.dataset.efeito;
        document.getElementById('detalheNum').innerText = card.dataset.num_categorico;
        document.getElementById('detalheRaridade').innerText = card.dataset.raridade;

        // EDITAR
        document.getElementById('detalheEditar').onclick = e => {
            e.stopPropagation();
            const form = document.getElementById('formEditarItem');
            form.action = `/editar_item/${card.dataset.id}`;

            document.getElementById('editNome').value = card.dataset.nome;
            document.getElementById('editElemento').value = card.dataset.elemento;
            document.getElementById('editEfeito').value = card.dataset.efeito;
            document.getElementById('editNum').value = card.dataset.num_categorico;

            document.getElementById('modalEditarItem').style.display = 'flex';
            document.getElementById('modalDetalhesItem').style.display = 'none';
        };

        // EXCLUIR
        document.getElementById('detalheExcluir').onclick = e => {
            e.stopPropagation();
            const form = document.getElementById('formExcluirItem');
            form.action = `/deletar_item/${card.dataset.id}`;

            document.getElementById('modalExcluirItem').style.display = 'flex';
            document.getElementById('modalDetalhesItem').style.display = 'none';
        };

        document.getElementById('modalDetalhesItem').style.display = 'flex';
    });
});



// ====================
//  FILTRO DE PESQUISA
// ====================
const barraPesquisa = document.getElementById('barraPesquisa');

barraPesquisa.addEventListener('keyup', () => {
    const termo = barraPesquisa.value.toLowerCase();
    const cards = document.querySelectorAll('.item-card');

    cards.forEach(card => {
        const nome = card.dataset.nome?.toLowerCase() || "";
        const elemento = card.dataset.elemento?.toLowerCase() || "";
        const efeito = card.dataset.efeito?.toLowerCase() || "";
        const raridade = card.dataset.raridade?.toLowerCase() || "";
        const numero = card.dataset.num_categorico?.toLowerCase() || "";

        const textoCompleto = `${nome} ${elemento} ${efeito} ${raridade} ${numero}`;

        card.style.display = textoCompleto.includes(termo) ? 'block' : 'none';
    });
});
