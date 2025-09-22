from flask import render_template, request, redirect, url_for, Blueprint
from core.database import db
from models.autor import Autor
from models.exemplar import Exemplar
from models.usuario import Aluno, Professor, Funcionario
from models.livro import Livro

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/autores')
def lista_autores():
    autores = Autor.query.all()
    return render_template('admin/autores.html', autores=autores)

@admin_bp.route('/adicionar_autor', methods=['POST'])
def adicionar_autor():
    nome = request.form.get('nome')
    if nome:
        novo_autor = Autor(nome=nome)
        db.session.add(novo_autor)
        db.session.commit()
    return redirect(url_for('admin_bp.lista_autores'))

@admin_bp.route('/livros')
def lista_livros():
    livros = Livro.query.all()
    return render_template('admin/livros.html', livros=livros)

@admin_bp.route('/exemplares')
def lista_exemplares():
    exemplares = Exemplar.query.all()
    return render_template('admin/exemplares.html', exemplares=exemplares)

@admin_bp.route('/usuarios')
def lista_usuarios():
    alunos = Aluno.query.all()
    professores = Professor.query.all()
    funcionarios = Funcionario.query.all()
    return render_template('admin/usuarios.html', 
        alunos=alunos, 
        professores=professores, 
        funcionarios=funcionarios
    )

@admin_bp.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    tipo = request.form.get('tipo')
    
    if tipo == 'aluno':
        novo_usuario = Aluno(nome=nome, email=email, matricula=request.form.get('matricula'))
    elif tipo == 'professor':
        novo_usuario = Professor(nome=nome, email=email, departamento=request.form.get('departamento'))
    elif tipo == 'funcionario':
        novo_usuario = Funcionario(nome=nome, email=email, cargo=request.form.get('cargo'))
    
    if novo_usuario:
        db.session.add(novo_usuario)
        db.session.commit()
    return redirect(url_for('admin_bp.lista_usuarios'))