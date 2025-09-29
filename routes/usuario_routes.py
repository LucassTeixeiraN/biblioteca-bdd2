from flask import Blueprint, jsonify, request
from core.database import db
from models.usuario import Aluno, Funcionario, Professor, Usuario
from services.serialize_usuario import serialize_usuario


usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET', 'POST'])
def usuarios_collection():
    """
        - GET: Retorna uma lista de todos os usuários.
        - POST: Cria um novo usuário.
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ['nome', 'email', 'tipo']): return jsonify({'erro': 'Dados em falta'}), 400
        if Usuario.query.filter_by(email=data['email']).first(): return jsonify({'erro': 'Email já registado'}), 409
        try:
            tipo = data['tipo'].lower()
            if tipo == 'aluno': novo_usuario = Aluno(nome=data['nome'], email=data['email'], matricula=data.get('matricula')) #type: ignore
            elif tipo == 'professor': novo_usuario = Professor(nome=data['nome'], email=data['email'], departamento=data.get('departamento')) #type: ignore
            elif tipo == 'funcionario': novo_usuario = Funcionario(nome=data['nome'], email=data['email'], cargo=data.get('cargo')) #type: ignore
            else: return jsonify({'erro': f"Tipo inválido: '{data['tipo']}'"}), 400
            db.session.add(novo_usuario)
            db.session.commit()
            return jsonify(serialize_usuario(novo_usuario)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
    usuarios = Usuario.query.order_by(Usuario.nome).all()

    #Método GET
    return jsonify([serialize_usuario(u) for u in usuarios])


@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['GET', 'PUT', 'DELETE'])
def usuario_resource(usuario_id):
    """
        - GET: Retorna os detalhes de um usuário.
        - PUT: Atualiza um usuário.
        - DELETE: Remove um usuário.
    """
    usuario = Usuario.query.get_or_404(usuario_id)

    if request.method == 'PUT':
        data = request.get_json()
        if not data: return jsonify({'erro': 'Corpo da requisição vazio'}), 400
        if 'email' in data and Usuario.query.filter(Usuario.email == data['email'], Usuario.id != usuario_id).first(): return jsonify({'erro': 'Email já em uso'}), 409
        try:
            usuario.nome = data.get('nome', usuario.nome)
            usuario.email = data.get('email', usuario.email)
            if usuario.tipo == 'aluno': usuario.matricula = data.get('matricula', usuario.matricula)
            elif usuario.tipo == 'professor': usuario.departamento = data.get('departamento', usuario.departamento)
            elif usuario.tipo == 'funcionario': usuario.cargo = data.get('cargo', usuario.cargo)
            db.session.commit()
            return jsonify(serialize_usuario(usuario))
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
        

    if request.method == 'DELETE':
        if usuario.emprestimos_ativos > 0: return jsonify({'erro': 'Não é possível deletar com empréstimos ativos.'}), 403
        try:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({'mensagem': 'Usuário deletado!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
        
    #Método GET
    return jsonify(serialize_usuario(usuario))