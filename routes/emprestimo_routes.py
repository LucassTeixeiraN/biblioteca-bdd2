from flask import Blueprint, jsonify, request
from core.database import db
from models.usuario import Usuario
from models.livro import Livro
from models.emprestimo import Emprestimo
from services.serialize_emprestimo import serialize_emprestimo
from datetime import datetime

emprestimo_bp = Blueprint('emprestimo_bp', __name__)


@emprestimo_bp.route('/emprestimos', methods=['GET', 'POST'])
def emprestimos_collection():
    """
        - GET: Retorna uma lista de empréstimos, com filtros opcionais.
        - POST: Cria um novo empréstimo.
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ['usuario_id', 'livro_id']): return jsonify({'erro': 'usuario_id e livro_id obrigatórios'}), 400
        usuario = Usuario.query.get(data['usuario_id'])
        livro = Livro.query.get(data['livro_id'])
        if not usuario or not livro: return jsonify({'erro': 'Usuário ou Livro não encontrado'}), 404
        if not usuario.pode_emprestar(): return jsonify({'erro': 'Usuário não pode realizar novos empréstimos.'}), 403
        if Emprestimo.query.filter_by(livro_id=livro.id, data_devolucao=None).first(): return jsonify({'erro': 'Livro já emprestado.'}), 409
        try:
            novo_emprestimo = Emprestimo(usuario_id=usuario.id, livro_id=livro.id) #type: ignore
            db.session.add(novo_emprestimo)
            db.session.commit()
            return jsonify(serialize_emprestimo(novo_emprestimo)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
    emprestimos = Emprestimo.query.order_by(Emprestimo.data_emprestimo.desc()).all()

    #Método GET
    return jsonify([serialize_emprestimo(e) for e in emprestimos])

@emprestimo_bp.route('/emprestimos/<int:emprestimo_id>', methods=['GET', 'PUT'])
def emprestimo_resource(emprestimo_id):
    """
        - GET: Retorna um empréstimo específico.
        - PUT: Atualiza um empréstimo (devolver, forçar atraso).
    """
    emprestimo = Emprestimo.query.get_or_404(emprestimo_id)
    if request.method == 'PUT':
        data = request.get_json()
        if not data or 'acao' not in data: return jsonify({'erro': 'Ação é obrigatória'}), 400
        try:
            if data['acao'] == 'devolver' and not emprestimo.data_devolucao: emprestimo.data_devolucao = datetime.utcnow()
            elif data['acao'] == 'alternar_atraso_manual': emprestimo.atrasado_manualmente = not emprestimo.atrasado_manualmente
            db.session.commit()
            return jsonify(serialize_emprestimo(emprestimo))
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
    
    #Método GET
    return jsonify(serialize_emprestimo(emprestimo))
