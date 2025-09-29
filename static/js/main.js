document.addEventListener('DOMContentLoaded', () => {
    const selectAutor = document.getElementById('filtro-autor');
    const inputAno = document.getElementById('filtro-ano');
    const listaLivrosUl = document.getElementById('lista-livros');
    const btnLimpar = document.getElementById('limpar-filtros');
    
    // Função para buscar autores e popular o select
    async function carregarAutores() {
        try {
            const response = await fetch('/autores');
            if (!response.ok) throw new Error('Falha ao carregar autores');
            const autores = await response.json();
            
            autores.forEach(autor => {
                const option = document.createElement('option');
                option.value = autor.id;
                option.textContent = autor.nome;
                selectAutor.appendChild(option);
            });
        } catch (error) {
            console.error("Erro:", error);
        }
    }

    // --- FUNÇÃO CARREGAR LIVROS ATUALIZADA ---
    // Agora ela constrói a URL com os filtros e busca na API.
    async function carregarLivros() {
        const autorId = selectAutor.value;
        const ano = inputAno.value;
        
        const params = new URLSearchParams();
        if (autorId) {
            params.append('autor_id', autorId);
        }
        if (ano) {
            params.append('ano', ano);
        }
        
        listaLivrosUl.innerHTML = '<li class="list-group-item">A filtrar livros...</li>';

        try {
            const response = await fetch(`/livros?${params.toString()}`);
            if (!response.ok) throw new Error('Falha ao carregar livros');
            const livrosFiltrados = await response.json();
            renderizarLivros(livrosFiltrados);
        } catch (error) {
            console.error("Erro:", error);
            listaLivrosUl.innerHTML = '<li class="list-group-item list-group-item-danger">Não foi possível carregar os livros.</li>';
        }
    }

    // Função para renderizar a lista de livros na tela (sem alterações)
    function renderizarLivros(livrosParaRenderizar) {
        listaLivrosUl.innerHTML = '';
        if (livrosParaRenderizar.length === 0) {
            listaLivrosUl.innerHTML = '<li class="list-group-item">Nenhum livro encontrado com os filtros aplicados.</li>';
            return;
        }

        livrosParaRenderizar.forEach(livro => {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            const autoresNomes = livro.autores.map(a => a.nome).join(', ');
            li.innerHTML = `
                <h4>Título: ${livro.titulo} (${livro.ano_publicacao})</h4>
                <small>Autores: ${autoresNomes}</small>
            `;
            listaLivrosUl.appendChild(li);
        });
    }

    // Adiciona os event listeners que agora chamam carregarLivros
    selectAutor.addEventListener('change', carregarLivros);
    inputAno.addEventListener('input', carregarLivros);

    // Funcionalidade do botão de limpar
    btnLimpar.addEventListener('click', () => {
        selectAutor.value = "";
        inputAno.value = "";
        carregarLivros(); 
    });

    // Inicialização
    carregarAutores();
    carregarLivros(); 
});