from core.database import db

# Tabela de associação para o relacionamento N:N entre Livro e Autor
livro_autor = db.Table('livro_autor',
    db.Column('livro_id', db.Integer, db.ForeignKey('livros.id'), primary_key=True),
    db.Column('autor_id', db.Integer, db.ForeignKey('autores.id'), primary_key=True)
)

class Autor(db.Model):
    __tablename__ = 'autores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Relacionamento 'many-to-many' com a classe Livro
    livros = db.relationship('Livro', secondary=livro_autor, back_populates='autores')

    def __repr__(self):
        return f"<Autor(nome='{self.nome}')>"