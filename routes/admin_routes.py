from flask import render_template, Blueprint
from models.autor import Autor
from models.usuario import Aluno, Professor, Funcionario
from models.livro import Livro
from models.emprestimo import Emprestimo

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/buscarLivros')
def renderiza_filtros():
    livros = Livro.query.all()
    return render_template('index.html', livros=livros)

@admin_bp.route('/autores')
def renderiza_autores():
    autores = Autor.query.all()
    return render_template('autores.html', autores=autores)

@admin_bp.route('/livros')
def lista_livros():
    livros = Livro.query.all()
    return render_template('livros.html', livros=livros)

@admin_bp.route('/usuarios')
def lista_usuarios():
    alunos = Aluno.query.all()
    professores = Professor.query.all()
    funcionarios = Funcionario.query.all()
    return render_template('usuarios.html', 
        alunos=alunos, 
        professores=professores, 
        funcionarios=funcionarios
    )

@admin_bp.route('/emprestimos')
def renderizar_emprestimo():
    emprestimos = Emprestimo.query.all()
    return render_template('emprestimo.html', emprestimos=emprestimos)