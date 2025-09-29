from core.database import db
from sqlalchemy.orm import relationship
from .autor import livro_autor
 
class Livro(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    ano_publicacao = db.Column(db.Integer)

    # Relacionamento com a tabela de associação para autores
    autores = db.relationship('Autor', secondary=livro_autor, back_populates='livros')

    emprestimos = db.relationship(
        'Emprestimo',
        back_populates='livro',
        lazy='dynamic',
        cascade="all, delete-orphan" 
    )

    def __repr__(self):
        return f"<Livro(titulo='{self.titulo}')>"