from core.database import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Coluna usada para determinar o tipo de usuário (aluno, professor, etc.)
    tipo = db.Column(db.String(50))
    
    # Relacionamento com a tabela de Empréstimos
    emprestimos = db.relationship('Emprestimo', back_populates='usuario', lazy='dynamic', cascade="all, delete-orphan")
    
    # Configuração para herança de tabela única
    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }
    
    @property
    def limite_emprestimo(self):
        """
        Define um limite padrão ou levanta um erro. 
        Este método DEVE ser sobrescrito pelas subclasses.
        """
        raise NotImplementedError("Subclasses de Usuario devem implementar a propriedade 'limite_emprestimo'.")

    @property
    def emprestimos_ativos(self):
        """Retorna a contagem de livros atualmente emprestados (sem data de devolução)."""
        return self.emprestimos.filter_by(data_devolucao=None).count()
        
    @property
    def tem_emprestimos_atrasados(self):
        """Verifica se o usuário tem algum empréstimo em atraso."""
        emprestimos_sem_devolucao = self.emprestimos.filter_by(data_devolucao=None).all()
        return any(e.esta_atrasado for e in emprestimos_sem_devolucao)

    def pode_emprestar(self):
        """
        Verifica se o usuário pode realizar um novo empréstimo.
        Regras: Não pode ter atingido o limite E não pode ter livros em atraso.
        """
        if self.tem_emprestimos_atrasados:
            return False
        return self.emprestimos_ativos < self.limite_emprestimo
    
    def __repr__(self):
        return f"<Usuario(nome='{self.nome}', tipo='{self.tipo}')>"

# --- SUBCLASSES COM LIMITES ESPECÍFICOS ---

class Aluno(Usuario):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    matricula = db.Column(db.String(20), unique=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'aluno',
    }
    
    @property
    def limite_emprestimo(self):
        """Sobrescreve a propriedade da classe base para definir o limite do aluno."""
        return 3
    
    def __repr__(self):
        return f"<Aluno(nome='{self.nome}', matricula='{self.matricula}')>"

class Professor(Usuario):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    departamento = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'professor',
    }
    
    @property
    def limite_emprestimo(self):
        """Define o limite para professores."""
        return 10

class Funcionario(Usuario):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    cargo = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
    }

    @property
    def limite_emprestimo(self):
        """Define o limite para funcionários."""
        return 5