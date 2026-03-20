# Sistema de Gestão de Voluntariado Comunitário

##  Sobre o Projeto

O Sistema de Gestão de Voluntariado Comunitário é uma plataforma web desenvolvida com o objetivo de auxiliar organizações sociais, como igrejas e projetos comunitários, na organização de campanhas, ações sociais e gerenciamento de voluntários.

A aplicação permite centralizar informações, facilitar o cadastro de participantes e otimizar o planejamento de atividades sociais, promovendo maior eficiência na execução de ações comunitárias.

O sistema foi aplicado na **Igreja Batista Comunidade Esperança – Salvador/BA**, como parte de um projeto extensionista voltado à inclusão digital e apoio a iniciativas sociais.

---

##  Funcionalidades

- Cadastro e autenticação de usuários  
- Criação e gerenciamento de campanhas  
- Criação e gerenciamento de ações sociais  
- Inscrição de voluntários em ações  
- Ranking dos voluntários  
- Listagem com filtros e paginação  
- Interface simples e intuitiva  

---

##  Tecnologias Utilizadas

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **HTML**
- **CSS**
- **JavaScript**

---

##  Demonstração da Plataforma

###  Tela Inicial
![Tela Inicial](./docs/home.png)
Página principal com listagem de campanhas e ações disponíveis.

---

###  Cadastro de Campanhas
![Campanhas](./docs/campanhas.png)
Interface para criação e gerenciamento de campanhas sociais.

---

###  Cadastro de Ações
![Ações](./docs/acoes.png)
Tela para criação e gerenciamento de ações.

---

###  Voluntários
![Voluntários](./docs/voluntarios.png)
Gerenciamento de voluntários e inscrição em ações.

---

###  Inscrição em Ações
![Inscrição](./docs/inscricao.png)
Processo de vinculação de voluntários às ações sociais.

---
## ⚙️ Instalação e Configuração

### 1. Clonar o repositório

git clone https://github.com/SarmentoDelano/sistema-voluntariado-comunitario.git

cd sistema-voluntariado-comunitario
### 2. Criar e ativar o ambiente virtual

python -m venv venv
venv\Scripts\activate

### 3. Instalar as dependências

pip install -r requirements.txt

### 4. Aplicar as migrações do banco de dados

python manage.py migrate

### 5. Criar um superusuário

python manage.py createsuperuser

### 6. Executar o servidor de desenvolvimento

python manage.py runserver

### A aplicação estará disponível em: http://127.0.0.1:8000/

## Aplicação do Projeto

### O sistema foi utilizado em um cenário real simulado na Igreja Batista Comunidade Esperança, onde foram cadastradas:

- Campanhas de doação de cestas básicas
- Campanhas de arrecadação de material escolar
- Ações sociais como distribuição de sopas
- Voluntários vinculados às ações
- Demonstrando a viabilidade da plataforma para uso em comunidades locais.

## Demonstração em Vídeo

📌 (Adicione aqui o link do vídeo da sua apresentação)

## Contexto Acadêmico

### Este projeto foi desenvolvido como parte das Atividades Extensionistas, com foco em:

- Inclusão digital
- Impacto social
- Aplicação prática de tecnologia

## Autor

Delano Sarmento
GitHub: https://github.com/SarmentoDelano
