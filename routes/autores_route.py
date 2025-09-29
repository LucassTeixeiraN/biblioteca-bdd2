from flask import request, Blueprint, jsonify
from core.database import db
from models.autor import Autor
from services.serialize_autor import serialize_autor

autores_bp = Blueprint('autores_bp', __name__)

@autores_bp.route('/autores', methods=['GET', 'POST'])
def autores_collection():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not data.get('nome'): return jsonify({'erro': 'Nome é obrigatório'}), 400
        if Autor.query.filter_by(nome=data['nome']).first(): return jsonify({'erro': 'Autor já existe'}), 409
        try:
            novo_autor = Autor(nome=data['nome']) #type: ignore
            db.session.add(novo_autor)
            db.session.commit()
            return jsonify(serialize_autor(novo_autor)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
    
    #Método GET
    autores = Autor.query.order_by(Autor.nome).all()
    return jsonify([serialize_autor(a) for a in autores])

@autores_bp.route('/autores/<int:autor_id>', methods=['DELETE'])
def deletar_autor(autor_id):
    """Deleta um autor."""
    autor = Autor.query.get_or_404(autor_id)
    
    # Regra de negócio: Não permitir exclusão se o autor tiver livros associados.
    if autor.livros: return jsonify({'erro': 'Não é possível excluir autor com livros associados.'}), 403
    try:
        db.session.delete(autor)
        db.session.commit()
        return jsonify({'mensagem': 'Autor excluído!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500