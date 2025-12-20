# 

# C.R.I.S- ORDEM PARANORMAL

Dentro do rpg de mesa ordem paranormal, a instituição “Ordo Realitas” utiliza-se de um sistema projetado para a organização, que buscamos criar para sua experiência ser interativa e completa, podendo ser armazenada aí mesmo na sua máquina. 

## 🚀 Tecnologias Utilizadas:

- **Python 3**
- **Flask** (framework web)
- **PyMySQL** (conexão com MySQL)
- **MySQL** (banco de dados)
- **XAMPP** (para iniciar o banco de dados)
- **MySQL Workbench** (gerenciamento do banco)
- **HTML / CSS** (templates)

---

## 💻 Instalação Local:

1. AMBIENTE VIRTUAL:
    1. Abra o terminal no Visual Studio Code (Atalho: ctrl+shift+”)
    2. Em seguida coloque:
        
        ```python
        python -m venv venv
        ```
        
        Ou a versão alternativa:
        
        ```python
        py -m venv venv
        ```
        
    3. Após a instalação, entre no ambiente virtual com esse prompt:
        
        ```python
        ./venv/Scripts/Activate.ps1
        ```
        

1. INSTALANDO DEPENDÊNCIAS:
    1. Dentro do ambiente virtual, instale a seguinte dependência:
        
        ```python
        pip install flask
        ```
        
    2. Novamente dentro do ambiente virtual, instale a outra dependência:
        
        ```python
        pip install pymysql
        ```
        

---

## 🛠️ Configuração do Banco de Dados

1. Inicie o **MySQL pelo XAMPP**
2. Abra o **MySQL Workbench**
3. Execute o script abaixo para criar o banco e as tabelas:

```sql
CREATE DATABASE IF NOT EXISTS c.r.i.s
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE c.r.i.s;

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    imagem VARCHAR(255) DEFAULT ''
);

-- Usuário admin padrão
INSERT INTO usuarios (id, username, senha, imagem)
VALUES (1, 'admin', 'verissimo', '');

-- Tabela de agentes
CREATE TABLE agentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sobrenome VARCHAR(100),
    data_nasc DATE,
    contato_emergencia VARCHAR(100),
    elemento VARCHAR(50),
    classe ENUM('ESPECIALISTA','COMBATENTE','OCULTISTA','SOBREVIVENTE','NULO') DEFAULT 'NULO',
    observacoes VARCHAR(500),
    imagem VARCHAR(255),
    status ENUM('VIVO','MORTO') DEFAULT 'VIVO',
    ocupacao VARCHAR(100),
    marca VARCHAR(100),
    equipe VARCHAR(100)
);

-- Tabela de criaturas
CREATE TABLE criaturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    elemento VARCHAR(50),
    local_encontrado VARCHAR(100),
    descricao VARCHAR(500),
    raridade ENUM('COMUM','RARO','MUITO RARO','RELÍQUIA') DEFAULT 'COMUM',
    imagem VARCHAR(255)
);

-- Tabela de itens paranormais
CREATE TABLE itens_paranormais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    elemento VARCHAR(50),
    efeito TEXT,
    num_categorico VARCHAR(100),
    raridade ENUM('COMUM','RARO','MUITO RARO','RELÍQUIA') DEFAULT 'COMUM',
    imagem VARCHAR(255)
);

-- Tabela de relatórios
CREATE TABLE relatorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    equipe VARCHAR(100),
    data DATE NOT NULL,
    texto TEXT NOT NULL,
    autoria VARCHAR(100) NOT NULL
);

```

## ▶️ Como Executar o Projeto

1. Clone o repositório:

```bash
gitclone https://github.com/avmoonlight/ordo-realitas.git
```

1. Acesse a pasta do projeto:

```bash
cd ordo-realitas
```

1. Inicie o servidor Flask:

```bash
python app.py
```

1. Abra no navegador:

```
http://localhost:5000
```

---

## 🔐 Usuário Padrão

- **Usuário:** `admin`
- **Senha:** `verissimo`

> ⚠️ Recomenda-se alterar a senha em ambiente de produção.
> 

---

## 📁 Funcionalidades

- Login de usuários
- Cadastro e listagem de agentes
- Registro de criaturas paranormais
- Gerenciamento de itens paranormais
- Criação de relatórios de missões
- Upload de imagens
- Interface simples e temática

---

## 🧩 Estrutura Geral

```
ordo-realitas/
│── app.py
│── static/
│   ├── css/
│   └── imagens/
│── templates/
│──database.sql
│── README.md
```

---

## 📜 Observações

- O banco deve estar ativo no **XAMPP** antes de iniciar o projeto
- A conexão com o banco é feita usando **PyMySQL**
- O projeto foi desenvolvido para fins educacionais e narrativos