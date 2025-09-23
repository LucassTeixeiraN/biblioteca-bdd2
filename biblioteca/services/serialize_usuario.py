def serialize_usuario(usuario):
    """Converte um objeto Usuario para um dicionário serializável."""
    detalhes_especificos = {}
    if usuario.tipo == 'aluno':
        detalhes_especificos['matricula'] = usuario.matricula
    elif usuario.tipo == 'professor':
        detalhes_especificos['departamento'] = usuario.departamento
    elif usuario.tipo == 'funcionario':
        detalhes_especificos['cargo'] = usuario.cargo

    return {
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo': usuario.tipo,
        'limite_emprestimo': usuario.limite_emprestimo,
        'emprestimos_ativos': usuario.emprestimos_ativos,
        'pode_emprestar': usuario.pode_emprestar(),
        'tem_emprestimos_atrasados': usuario.tem_emprestimos_atrasados,
        **detalhes_especificos
    }
