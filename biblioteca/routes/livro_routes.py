from flask import render_template, request, redirect, url_for, Blueprint, jsonify
from core.database import db
from models.livro import Livro
from models.autor import Autor

livro_bp = Blueprint('livro_bp', __name__)

@livro_bp.route('/')
def index():
    """Exibe a página inicial com a lista de livros."""
    livros = Livro.query.all()
    return render_template('index.html', livros=livros)

@livro_bp.route('/api/livros', methods=['GET'])
def get_livros_api():
    """Endpoint da API para listar todos os livros em JSON."""
    livros = Livro.query.all()
    # Converte a lista de objetos Livro para uma lista de dicionários
    livros_json = [{
        'id': livro.id,
        'titulo': livro.titulo,
        'ano_publicacao': livro.ano_publicacao,
        'autor': livro.autor
    } for livro in livros]
    return jsonify(livros_json)

@livro_bp.route('/adicionar_livro', methods=['POST'])
def adicionar_livro():
    """Rota para adicionar um novo livro."""
    titulo = request.form.get('titulo')
    ano = request.form.get('ano')
    autor_id = request.form.get('autor')
    
    autor = Autor.query.get(autor_id)
    if titulo and ano and autor:
        novo_livro = Livro(titulo=titulo, ano_publicacao=int(ano), autor=autor)
        db.session.add(novo_livro)
        db.session.commit()
    
    return redirect(url_for('livro_bp.index'))

@livro_bp.route('/livro/<int:livro_id>')
def detalhe_livro(livro_id):
    """Exibe os detalhes de um livro específico."""
    livro = Livro.query.get_or_404(livro_id)
    return f"Detalhes do Livro: {livro.titulo}, Ano: {livro.ano_publicacao}"