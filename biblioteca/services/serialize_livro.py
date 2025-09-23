from .serialize_autor import serialize_autor

def serialize_livro(livro):
    """Converte um objeto Livro para um dicionário serializável."""
    return {
        'id': livro.id,
        'titulo': livro.titulo,
        'ano_publicacao': livro.ano_publicacao,
        # Serializa a lista de autores associados
        'autores': [serialize_autor(autor) for autor in livro.autores],
        # Serializa apenas a informação necessária dos empréstimos
        'emprestimos': [{'data_devolucao': emprestimo.data_devolucao} for emprestimo in livro.emprestimos]
    }