# Sistema da ordo realitas

Dentro do universo do RPG de mesa **Ordem Paranormal**, a instituição Ordo Realitas muito provavelmente deve utilizar um sistema interno para organização de agentes, criaturas, itens e relatórios.

O **C.R.I.S** foi desenvolvido para proporcionar uma experiência interativa e imersiva, permitindo que tudo seja armazenado localmente na sua própria máquina.

---

# Tecnologias Utilizadas

- **Python 3**
- **Flask** (framework web)
- **PyMySQL** (conexão com MySQL)
- **MySQL** (banco de dados)
- **XAMPP** (para iniciar o MySQL)
- **MySQL Workbench** (gerenciamento do banco)
- **HTML / CSS**

---

# Instalação Completa do Zero

## Instalando o Visual Studio Code

1. Acesse o site oficial:
    
    https://code.visualstudio.com/
    
2. Baixe a versão para seu sistema operacional.
3. Instale normalmente.
4. Após instalar, abra o VSCode.

---

## Instalando o Python

1. Acesse:
    
    https://www.python.org/downloads/
    
2. Baixe o **Python 3 (versão mais recente)**.
3. **IMPORTANTE:** marque a opção
    
    ✅ *Add Python to PATH*
    
4. Finalize a instalação.
5. Para testar, abra o terminal e digite:

```
python--version
```

Se aparecer a versão do Python, está funcionando.

---

## Instalando o XAMPP

1. Acesse:
    
    https://www.apachefriends.org/
    
2. Baixe a versão para seu sistema.
3. Instale normalmente.
4. Abra o **XAMPP Control Panel**.
5. Clique em **Start** no módulo **MySQL**.

O MySQL precisa estar com o status **verde (Running)**.

---

## Instalando o MySQL Workbench

1. Acesse:
    
    https://dev.mysql.com/downloads/workbench/
    
2. Baixe e instale.
3. Abra o programa.
4. Crie uma nova conexão:
    - Hostname: `localhost`
    - Username: `root`
    - Password: (deixe vazio, padrão do XAMPP)

---

# Clonando o Projeto

```
git clone https://github.com/avmoonlight/ordo-realitas.git
cd ordo-realitas
```

---

# Criando o Ambiente Virtual

No VSCode:

1. Abra o terminal (CTRL + SHIFT + `)
2. Execute:

```
python-m venv venv
```

ou

```
py-m venv venv
```

1. Ative o ambiente virtual:

```
./venv/Scripts/Activate.ps1
```

Se aparecer `(venv)` no terminal, está ativo.

---

# Instalando Dependências

Dentro do ambiente virtual:

```
pip install flask
pip install pymysql
```

---

# Configuração do Banco de Dados

## Inicie o MySQL no XAMPP

Abra o **XAMPP Control Panel**

- Vá ao explorador de arquivos;
- Entre em “este computador”;
- Entre em “Disco Local”;
- Procure (dentro de disco local) a pasta xampp;
- Dentro da pasta xampp arraste até o final até encontrar o xampp control painel;
- Ao abrir marque a opção start apenas a frente de onde está escrito mysql workbench.

Clique em **Start** no MySQL.

---

## Criando o Banco no MySQL Workbench

Abra o Workbench e execute o script abaixo:

```
CREATE DATABASEIFNOTEXISTS cris
CHARACTERSET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE cris;

CREATETABLE usuarios (
    idINT AUTO_INCREMENTPRIMARYKEY,
    usernameVARCHAR(100)NOTNULLUNIQUE,
    senhaVARCHAR(255)NOTNULL,
    imagemVARCHAR(255)DEFAULT''
);

INSERTINTO usuarios (id, username, senha, imagem)
VALUES (1,'admin','verissimo','');

CREATETABLE agentes (
    idINT AUTO_INCREMENTPRIMARYKEY,
    nomeVARCHAR(100)NOTNULL,
    sobrenomeVARCHAR(100),
    data_nascDATE,
    contato_emergenciaVARCHAR(100),
    elementoVARCHAR(50),
    classe ENUM('ESPECIALISTA','COMBATENTE','OCULTISTA','SOBREVIVENTE','NULO')DEFAULT'NULO',
    observacoesVARCHAR(500),
    imagemVARCHAR(255),
    status ENUM('VIVO','MORTO')DEFAULT'VIVO',
    ocupacaoVARCHAR(100),
    marcaVARCHAR(100),
    equipeVARCHAR(100)
);

CREATETABLE criaturas (
    idINT AUTO_INCREMENTPRIMARYKEY,
    nomeVARCHAR(100)NOTNULL,
    elementoVARCHAR(50),
    local_encontradoVARCHAR(100),
    descricaoVARCHAR(500),
    raridade ENUM('COMUM','RARO','MUITO RARO','RELÍQUIA')DEFAULT'COMUM',
    imagemVARCHAR(255)
);

CREATETABLE itens_paranormais (
    idINT AUTO_INCREMENTPRIMARYKEY,
    nomeVARCHAR(100)NOTNULL,
    elementoVARCHAR(50),
    efeito TEXT,
    num_categoricoVARCHAR(100),
    raridade ENUM('COMUM','RARO','MUITO RARO','RELÍQUIA')DEFAULT'COMUM',
    imagemVARCHAR(255)
);

CREATETABLE relatorios (
    idINT AUTO_INCREMENTPRIMARYKEY,
    nomeVARCHAR(100)NOTNULL,
    equipeVARCHAR(100),
dataDATENOTNULL,
    texto TEXTNOTNULL,
    autoriaVARCHAR(100)NOTNULL
);
```

---

# Executando o Projeto

Com o MySQL rodando:

```
python app.py
```

Abra no navegador:

```
http://localhost:5000
```

---

# Usuário Padrão

- Usuário: `admin`
- Senha: `verissimo`

---

# Funcionalidades

- Sistema de login
- CRUD de usuários
- Cadastro de agentes
- Gerenciamento de equipes
- Registro de criaturas
- Gerenciamento de itens paranormais
- Sistema de relatórios
- Upload de imagens
- Sistema administrativo

---

# Estrutura do Projeto

```
ordo-realitas/
│── app.py
│── static/
│   ├── uploads/
│   └── css/
│── templates/
│── README.md
```

---

# Aviso de Responsabilidade

Este projeto:

- Não contém código malicioso
- Não executa nenhuma ação externa ao sistema local
- Não coleta dados do usuário
- Não realiza conexões externas além do banco local

**Toda responsabilidade sobre downloads, instalações e execuções é do próprio usuário.**

O projeto é de código aberto, voltado para fins educacionais e narrativos dentro do universo de RPG.

Recomenda-se sempre:

- Baixar dependências apenas de fontes oficiais
- Verificar o código antes de executar
- Utilizar ambientes virtuais
- Não utilizar em ambiente de produção sem melhorias de segurança

---

# Observações Finais

- O MySQL deve estar ativo no XAMPP antes de rodar o projeto.
- O banco precisa estar corretamente configurado.
- O projeto foi desenvolvido para fins educacionais e entretenimento.