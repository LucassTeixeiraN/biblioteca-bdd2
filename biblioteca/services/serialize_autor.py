def serialize_autor(autor):
    """Converte um objeto Autor para um dicionário serializável."""
    return {
        'id': autor.id,
        'nome': autor.nome,
        'livros': [
            {'id': livro.id, 'titulo': livro.titulo}
            for livro in autor.livros
        ]
    }