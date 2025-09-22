from core.database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Coluna usada para determinar o tipo de usuário (aluno, professor, etc.)
    tipo = db.Column(db.String(50))
    
    # Configuração para herança de tabela única
    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }
    
    def __repr__(self):
        return f"<Usuario(nome='{self.nome}', tipo='{self.tipo}')>"

class Aluno(Usuario):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    matricula = db.Column(db.String(20), unique=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'aluno',
    }
    
    def __repr__(self):
        return f"<Aluno(nome='{self.nome}', matricula='{self.matricula}')>"

class Professor(Usuario):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    departamento = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'professor',
    }

class Funcionario(Usuario):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    cargo = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
    }