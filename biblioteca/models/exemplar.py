from core.database import db
from sqlalchemy import Enum

# Define o status do exemplar
class StatusExemplar(Enum):
    DISPONIVEL = 'Disponível'
    EMPRESTADO = 'Emprestado'
    RESERVADO = 'Reservado'

class Exemplar(db.Model):
    __tablename__ = 'exemplares'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('Disponível', 'Emprestado', 'Reservado'), default=StatusExemplar.DISPONIVEL, nullable=False)
    
    # Chave estrangeira para o Livro
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    livro = db.relationship('Livro', backref=db.backref('exemplares', lazy=True))

    def __repr__(self):
        return f"<Exemplar(id='{self.id}', livro='{self.livro.titulo}', status='{self.status.value}')>"