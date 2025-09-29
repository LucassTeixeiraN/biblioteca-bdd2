# Sistema de Gestão de Biblioteca
Bem-vindo ao Sistema de Gestão de Biblioteca! Esta é uma aplicação web desenvolvida em Flask para administrar os recursos de uma biblioteca acadêmica, incluindo o cadastro de livros, autores, usuários (leitores) e o controle de empréstimos.

## ✨ Funcionalidades Principais
* **Gestão de Livros:** Adicione, edite e remova livros do acervo.

* **Gestão de Autores:** Mantenha um registo centralizado de autores.

* **Gestão de Usuários (Leitores):** Administre os leitores da biblioteca, categorizados como Alunos, Professores e Funcionários, cada um com regras de empréstimo específicas.

* **Controle de Empréstimos:** Registe novos empréstimos, marque devoluções e controle o status de cada livro (disponível, emprestado, atrasado).

* **Interface Dinâmica:** Todas as operações são realizadas numa interface de painel único, que se comunica com uma API RESTful, proporcionando uma experiência de uso fluida e sem recarregamentos de página.

* **Filtros Avançados:** A página inicial permite a busca e filtragem de livros por autor e ano de publicação.

## 🛠️ Tecnologias Utilizadas
* **Backend:** Python 3, Flask, SQLAlchemy

* **Base de Dados:** SQLite

* **Frontend:** HTML5, CSS3, JavaScript (puro)

* **Ambiente:** Python Virtual Environment (venv)

## 🚀 Guia de Instalação e Execução
Siga os passos abaixo para configurar e executar o projeto no seu ambiente local.

### **1. Pré-requisitos**
Antes de começar, certifique-se de que tem o seguinte software instalado na sua máquina:

Python 3.8+

pip (geralmente vem instalado com o Python)

### **2. Instalação**

**a. Clone o repositório:**
Abra o seu terminal ou git bash e clone o projeto para o seu computador.

```git
git clone https://github.com/LucassTeixeiraN/biblioteca-bdd2.git
cd biblioteca-bdd2
```

**b. Crie e Ative um Ambiente Virtual (venv):**
É uma boa prática isolar as dependências do projeto num ambiente virtual.

```
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

O seu terminal deverá agora mostrar (venv) no início da linha.

**c. Instale as Dependências:**
Com o ambiente virtual ativo, instale todas as bibliotecas Python necessárias com um único comando.

```
pip install -r requirements.txt
```

### **3. Como Executar**

Com o ambiente virtual ainda ativo e a base de dados criada, inicie o servidor de desenvolvimento do Flask:

```
flask run
```

A aplicação estará agora a ser executada! Abra o seu navegador e acesse a:
http://127.0.0.1:5000/
