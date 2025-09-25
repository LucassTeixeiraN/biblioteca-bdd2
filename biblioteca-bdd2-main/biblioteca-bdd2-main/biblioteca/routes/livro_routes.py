from flask import render_template, request, redirect, url_for, Blueprint, jsonify
from core.database import db
from models.livro import Livro
from models.autor import Autor
from services.serialize_livro import serialize_livro

livro_bp = Blueprint('livro_bp', __name__)

@livro_bp.route('/')
def index():
    """Exibe a página inicial com a lista de livros."""
    livros = Livro.query.all()
    return render_template('index.html', livros=livros)

@livro_bp.route('/api/livros', methods=['GET'])
def get_livros_api():
    """Retorna uma lista de todos os livros."""
    livros = Livro.query.order_by(Livro.titulo).all()
    return jsonify([serialize_livro(livro) for livro in livros])

@livro_bp.route('/adicionar_livro', methods=['POST'])
def adicionar_livro():
    """Cria um novo livro."""
    data = request.get_json()
    if not data or not all(k in data for k in ['titulo', 'ano_publicacao', 'autores_ids']):
        return jsonify({'erro': 'Dados em falta: titulo, ano_publicacao e autores_ids são obrigatórios'}), 400

    autores_ids = data.get('autores_ids', [])
    if not autores_ids:
        return jsonify({'erro': 'Pelo menos um autor deve ser selecionado'}), 400
        
    autores = Autor.query.filter(Autor.id.in_(autores_ids)).all()

    novo_livro = Livro(
        titulo=data['titulo'],
        ano_publicacao=data['ano_publicacao'],
        autores=autores
    )
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify(serialize_livro(novo_livro)), 201
    

@livro_bp.route('/livro/<int:livro_id>')
def detalhe_livro(livro_id):
    """Exibe os detalhes de um livro específico."""
    livro = Livro.query.get_or_404(livro_id)
    return f"Detalhes do Livro: {livro.titulo}, Ano: {livro.ano_publicacao}"