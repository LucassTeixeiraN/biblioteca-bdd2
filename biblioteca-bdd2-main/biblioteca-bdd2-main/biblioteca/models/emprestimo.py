from datetime import datetime, timedelta
from core.database import db

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    id = db.Column(db.Integer, primary_key=True)
    data_emprestimo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_prevista_devolucao = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=14))
    data_devolucao = db.Column(db.DateTime, nullable=True)
    
    # Campo para forçar o estado de "atrasado" manualmente
    atrasado_manualmente = db.Column(db.Boolean, default=False, nullable=False)

    # Chaves Estrangeiras
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False) # Supondo que a tabela de livros se chame 'livros'

    # Relacionamentos
    usuario = db.relationship('Usuario', back_populates='emprestimos')
    livro = db.relationship('Livro', back_populates='emprestimos')
    
    @property
    def esta_atrasado(self):

        if self.atrasado_manualmente:
            return True
        if self.data_devolucao is None and datetime.utcnow() > self.data_prevista_devolucao:
            return True
        return False