
def serialize_emprestimo(emprestimo):
    """Converte um objeto Emprestimo para um dicionário serializável."""
    return {
        'id': emprestimo.id,
        'data_emprestimo': emprestimo.data_emprestimo.isoformat(),
        'data_prevista_devolucao': emprestimo.data_prevista_devolucao.isoformat(),
        'data_devolucao': emprestimo.data_devolucao.isoformat() if emprestimo.data_devolucao else None,
        'esta_atrasado': emprestimo.esta_atrasado,
        'atrasado_manualmente': emprestimo.atrasado_manualmente,
        'usuario': {'id': emprestimo.usuario_id, 'nome': emprestimo.usuario.nome},
        'livro': {'id': emprestimo.livro_id, 'titulo': emprestimo.livro.titulo}
    }