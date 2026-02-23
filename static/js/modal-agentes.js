// Modais
const modals = document.querySelectorAll('.modal');
const fecharBtns = document.querySelectorAll('.fechar');
fecharBtns.forEach(btn => btn.onclick = () => btn.parentElement.parentElement.style.display = 'none');
window.onclick = e => { if (e.target.classList.contains('modal')) e.target.style.display = 'none'; };

document.getElementById('abrirModal').onclick = () => document.getElementById('modalNovoUsuario').style.display = 'flex';

// ====================
//  BOTÕES EDITAR
// ====================
const editarBtns = document.querySelectorAll('.editar');
editarBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        e.stopPropagation();
        const card = e.target.closest('.usuario-card');
        const id = card.dataset.id;
        const form = document.getElementById('formEditarUsuario');
        form.action = `/editar/${id}`;  // ✅ corrigido
        document.getElementById('editNome').value = card.dataset.nome;
        document.getElementById('editSobrenome').value = card.dataset.sobrenome;
        document.getElementById('editDataNasc').value = card.dataset.data_nasc;
        document.getElementById('editContato').value = card.dataset.contato;
        document.getElementById('editElemento').value = card.dataset.elemento;
        document.getElementById('editClasse').value = card.dataset.classe;
        document.getElementById('editOcupacao').value = card.dataset.ocupacao;
        document.getElementById('editMarca').value = card.dataset.marca;
        document.getElementById('editEquipe').value = card.dataset.equipe;
        document.getElementById('editStatus').value = card.dataset.status;
        document.getElementById('editObservacoes').value = card.dataset.observacoes;
        document.getElementById('modalEditarUsuario').style.display = 'flex';
    });
});

// ====================
//  BOTÕES EXCLUIR
// ====================
const excluirBtns = document.querySelectorAll('.excluir');
excluirBtns.forEach(btn => {
    btn.addEventListener('click', e => {
        e.stopPropagation();
        const card = e.target.closest('.usuario-card');
        const id = card.dataset.id;
        const form = document.getElementById('formExcluirUsuario');
        form.action = `/deletar/${id}`;  // ✅ corrigido
        document.getElementById('modalExcluirUsuario').style.display = 'flex';
    });
});

// ====================
//  DETALHES DO AGENTE
// ====================
const cards = document.querySelectorAll('.usuario-card');
cards.forEach(card => {
    card.addEventListener('click', () => {
        document.getElementById('detalheNome').innerText = card.dataset.nome + ' ' + card.dataset.sobrenome;
        document.getElementById('detalheData').innerText = card.dataset.data_nasc;
        document.getElementById('detalheContato').innerText = card.dataset.contato;
        document.getElementById('detalheElemento').innerText = card.dataset.elemento;
        document.getElementById('detalheClasse').innerText = card.dataset.classe;
        document.getElementById('detalheOcupacao').innerText = card.dataset.ocupacao;
        document.getElementById('detalheMarca').innerText = card.dataset.marca;
        document.getElementById('detalheEquipe').innerText = card.dataset.equipe;
        document.getElementById('detalheStatus').innerText = card.dataset.status;
        document.getElementById('detalheObservacoes').innerText = card.dataset.observacoes;

        // Botão Editar dentro do modal
        document.getElementById('detalheEditar').onclick = (e) => {
            e.stopPropagation();
            const form = document.getElementById('formEditarUsuario');
            form.action = `/editar/${card.dataset.id}`;  // ✅ corrigido
            document.getElementById('editNome').value = card.dataset.nome;
            document.getElementById('editSobrenome').value = card.dataset.sobrenome;
            document.getElementById('editDataNasc').value = card.dataset.data_nasc;
            document.getElementById('editContato').value = card.dataset.contato;
            document.getElementById('editElemento').value = card.dataset.elemento;
            document.getElementById('editClasse').value = card.dataset.classe;
            document.getElementById('editOcupacao').value = card.dataset.ocupacao;
            document.getElementById('editMarca').value = card.dataset.marca;
            document.getElementById('editEquipe').value = card.dataset.equipe;
            document.getElementById('editStatus').value = card.dataset.status;
            document.getElementById('editObservacoes').value = card.dataset.observacoes;
            document.getElementById('modalEditarUsuario').style.display = 'flex';
            document.getElementById('modalDetalhesAgente').style.display = 'none';
        };

        // Botão Excluir dentro do modal
        document.getElementById('detalheExcluir').onclick = (e) => {
            e.stopPropagation();
            const form = document.getElementById('formExcluirUsuario');
            form.action = `/deletar/${card.dataset.id}`;  // ✅ corrigido
            document.getElementById('modalExcluirUsuario').style.display = 'flex';
            document.getElementById('modalDetalhesAgente').style.display = 'none';
        };

        document.getElementById('modalDetalhesAgente').style.display = 'flex';
    });
});
// ====================
// ====================
// FILTRO SIMPLES
// ====================

const tipoFiltro = document.getElementById('tipoFiltro');
const barraPesquisa = document.getElementById('barraPesquisa');

function aplicarFiltros() {

    const campoSelecionado = tipoFiltro.value;
    const termo = barraPesquisa.value.toLowerCase();

    const cards = document.querySelectorAll('.usuario-card');

    cards.forEach(card => {

        let valorCampo = (card.dataset[campoSelecionado] || "").toLowerCase();

        let correspondePesquisa = valorCampo.includes(termo);

        if (correspondePesquisa) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }

    });
}

// Eventos
barraPesquisa.addEventListener("keyup", aplicarFiltros);
tipoFiltro.addEventListener("change", aplicarFiltros);