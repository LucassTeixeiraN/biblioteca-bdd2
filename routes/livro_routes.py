from flask import render_template, request, Blueprint, jsonify
from core.database import db
from sqlalchemy import text
from models.livro import Livro
from models.autor import Autor
from services.serialize_livro import serialize_livro

livro_bp = Blueprint('livro_bp', __name__)

def _filtrar_livros_query(params):
    """
    Constrói uma string de consulta SQL pura com base nos parâmetros de filtro,
    garantindo a segurança contra injeção de SQL através de named parameters.
    """
    # Dicionário para armazenar os parâmetros da consulta de forma segura
    query_params = {}
    
    # Base da query SQL. Usamos DISTINCT para evitar duplicatas de livros com múltiplos autores.
    # Selecionamos todas as colunas de 'livros' para que o ORM possa reconstruir o objeto.
    base_query = "SELECT DISTINCT livros.* FROM livros"
    
    # Lista para armazenar as cláusulas JOIN e WHERE
    joins = []
    wheres = []

    # Obtém os parâmetros de filtro da URL
    autor_id = params.get('autor_id')
    ano = params.get('ano')

    # Se um autor_id for fornecido, adiciona um JOIN e um WHERE à consulta
    if autor_id:
        # Assumindo que a tabela de associação se chama 'livro_autor'
        joins.append("JOIN livro_autor ON livros.id = livro_autor.livro_id")
        wheres.append("livro_autor.autor_id = :autor_id")
        query_params['autor_id'] = autor_id

    # Se um ano for fornecido, adiciona uma cláusula WHERE
    if ano:
        wheres.append("livros.ano_publicacao = :ano")
        query_params['ano'] = ano
    
    # Monta a string SQL final
    final_query = base_query
    if joins:
        final_query += " " + " ".join(joins)
    if wheres:
        final_query += " WHERE " + " AND ".join(wheres)
    
    final_query += " ORDER BY livros.titulo"
    
    return final_query, query_params

@livro_bp.route('/')
def index():
    """Exibe a página inicial com a lista de livros."""
    livros = Livro.query.all()
    return render_template('index.html', livros=livros)

@livro_bp.route('/livros', methods=['GET', 'POST'])
def livros_collection():
    """
        - GET: Retorna todos os livros.
        - POST: Cria um novo livro.
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ['titulo', 'ano_publicacao', 'autores_ids']): return jsonify({'erro': 'Dados em falta'}), 400
        autores = Autor.query.filter(Autor.id.in_(data['autores_ids'])).all()
        if len(autores) != len(data['autores_ids']): return jsonify({'erro': 'Um ou mais autores não encontrados'}), 404
        try:
            novo_livro = Livro(titulo=data['titulo'], ano_publicacao=data['ano_publicacao'], autores=autores) # type: ignore
            db.session.add(novo_livro)
            db.session.commit()
            return jsonify(serialize_livro(novo_livro)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
        
    #Método GET
    try:
        # 1. Constrói a string SQL e os parâmetros
        sql_string, params = _filtrar_livros_query(request.args)

        # 2. Prepara a declaração SQL para execução segura
        stmt = text(sql_string)

        # 3. Executa a query e mapeia os resultados de volta para objetos Livro
        # O .params(**params) é a forma segura de passar os valores para a query
        livros = db.session.query(Livro).from_statement(stmt).params(**params).all() # type: ignore
        
        # 4. Serializa e retorna os resultados como JSON
        return jsonify([serialize_livro(l) for l in livros])
    except Exception as e:
        return jsonify({'erro': 'Ocorreu um erro ao buscar os livros', 'detalhes': str(e)}), 500
    

@livro_bp.route('/livros/<int:livro_id>', methods=['GET', 'PUT', 'DELETE'])
def livro_resource(livro_id):
    """- GET: Retorna um livro específico.
       - PUT: Atualiza um livro.
       - DELETE: Remove um livro."""
    livro = Livro.query.get_or_404(livro_id)
    if request.method == 'PUT':
        data = request.get_json()
        if not data: return jsonify({'erro': 'Corpo da requisição vazio'}), 400
        autores = Autor.query.filter(Autor.id.in_(data.get('autores_ids', []))).all()
        if len(autores) != len(data.get('autores_ids', [])): return jsonify({'erro': 'Um ou mais autores não encontrados'}), 404
        try:
            livro.titulo = data.get('titulo', livro.titulo)
            livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)
            livro.autores = autores
            db.session.commit()
            return jsonify(serialize_livro(livro))
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
        
    if request.method == 'DELETE':
        if livro.emprestimos.filter_by(data_devolucao=None).count() > 0: return jsonify({'erro': 'Não é possível deletar um livro emprestado.'}), 403
        try:
            db.session.delete(livro)
            db.session.commit()
            return jsonify({'mensagem': 'Livro deletado!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
        
    #Método GET
    return jsonify(serialize_livro(livro))