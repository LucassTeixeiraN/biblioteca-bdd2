from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import  Autor, Exemplar, Usuario, Aluno, Professor, Funcionario
from core.database import db
from routes.livro_routes import livro_bp
from routes.admin_routes import admin_bp
from routes.usuario_routes import usuario_bp
from routes.emprestimo_routes import emprestimo_bp
from routes.autores_route import autores_bp


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(livro_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(emprestimo_bp)
    app.register_blueprint(autores_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)