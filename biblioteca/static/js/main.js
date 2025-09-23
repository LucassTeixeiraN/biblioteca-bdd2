document.addEventListener('DOMContentLoaded', () => {
    const API_URL = '/api/livros';
    
    const listaLivros = document.getElementById('lista-livros');

    async function fetchLivros() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error('Erro na resposta da rede: ' + response.statusText);
            }
            const livros = await response.json();
            
            renderLivros(livros);
        } catch (error) {
            console.error('Houve um problema com a operação de fetch:', error);
            listaLivros.innerHTML = '<p>Erro ao carregar a lista de livros.</p>';
        }
    }

    function renderLivros(livros) {
        listaLivros.innerHTML = '';
        livros.forEach(livro => {
            const li = document.createElement('li');
            li.textContent = `${livro.titulo} (${livro.ano_publicacao}) - ${livro.autores.nome}`;
            listaLivros.appendChild(li);
        });
    }

    fetchLivros();
});