from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
import os
import pymysql

app = Flask(__name__)
app.secret_key = 'segredo'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Garante que a pasta de uploads exista
os.makedirs(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER']), exist_ok=True)

# Conexão com o banco MySQL (via XAMPP)
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  # senha padrão do XAMPP
        database='c.r.i.s',
        cursorclass=pymysql.cursors.DictCursor
    )

def salvar_imagem(imagem):
    if imagem and imagem.filename:
        filename = secure_filename(imagem.filename)
        caminho_completo = os.path.join(app.root_path, 'static', 'uploads', filename)

        # Evita sobrescrever imagem existente
        base, ext = os.path.splitext(filename)
        contador = 1
        while os.path.exists(caminho_completo):
            filename = f"{base}_{contador}{ext}"
            caminho_completo = os.path.join(app.root_path, 'static', 'uploads', filename)
            contador += 1

        imagem.save(caminho_completo)
        return f"uploads/{filename}"  # ✅ caminho relativo correto para url_for('static', ...)
    return ''



# LOGIN — acessível por "/" e "/login"
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')

        if not username or not senha:
            flash('Preencha todos os campos!')
            return render_template('login.html')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = %s AND senha = %s', (username, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['usuario'] = user['username']
            session['usuario_id'] = user['id']
            if user['id'] == 1:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('agentes'))
        else:
            flash('Usuário ou senha incorretos!')
    return render_template('login.html')


# DASHBOARD do admin
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session or session['usuario_id'] != 1:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# LISTAR USUÁRIOS
# LISTAR USUÁRIOS
@app.route('/usuarios')
def usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

# CRIAR USUÁRIO
@app.route('/usuarios/criar', methods=['GET', 'POST'])
def criar_usuario():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        imagem = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file.filename != '':
                caminho = os.path.join('static', 'uploads', file.filename)
                file.save(caminho)
                imagem = f'uploads/{file.filename}'
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, senha, imagem) VALUES (%s, %s, %s)", (username, senha, imagem))
        conn.commit()
        conn.close()
        return redirect(url_for('usuarios'))
    return render_template('criar_usuario.html')

# EDITAR USUÁRIO
@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if not usuario:
        conn.close()
        return "Usuário não encontrado."

    if request.method == 'POST':
        username = request.form['username']
        senha = request.form.get('senha', '')
        imagem = usuario['imagem']

        if 'imagem' in request.files:
            file = request.files['imagem']
            if file.filename != '':
                caminho = os.path.join('static', 'uploads', file.filename)
                file.save(caminho)
                imagem = f'uploads/{file.filename}'

        if senha.strip():
            cursor.execute("UPDATE usuarios SET username=%s, senha=%s, imagem=%s WHERE id=%s",
                           (username, senha, imagem, id))
        else:
            cursor.execute("UPDATE usuarios SET username=%s, imagem=%s WHERE id=%s",
                           (username, imagem, id))

        conn.commit()
        conn.close()
        return redirect(url_for('usuarios'))

    conn.close()
    return render_template('editar_usuario.html', usuario=usuario)

# DELETAR USUÁRIO
@app.route('/usuarios/deletar/<int:id>', methods=['POST'])
def deletar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('usuarios'))



# AGENTES
@app.route('/agentes', methods=['GET', 'POST'])
def agentes():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        data_nasc = request.form.get('data_nasc')
        contato = request.form.get('contato_emergencia')
        elemento = request.form.get('elemento')
        classe = request.form.get('classe')
        observacoes = request.form.get('observacoes')
        status = request.form.get('status')
        ocupacao = request.form.get('ocupacao')
        marca = request.form.get('marca')
        equipe = request.form.get('equipe')
        imagem = request.files.get('imagem')
        imagem_path = salvar_imagem(imagem)

        cursor.execute("""
            INSERT INTO agentes 
            (nome, sobrenome, data_nasc, contato_emergencia, elemento, classe,
             observacoes, imagem, status, ocupacao, marca, equipe)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nome, sobrenome, data_nasc, contato, elemento, classe, observacoes,
              imagem_path, status, ocupacao, marca, equipe))
        conn.commit()

    cursor.execute("SELECT * FROM agentes")
    agentes = cursor.fetchall()
    conn.close()

    return render_template('agentes.html', agentes=agentes)

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca os dados atuais do agente
    cursor.execute("SELECT * FROM agentes WHERE id = %s", (id,))
    agente = cursor.fetchone()

    if not agente:
        conn.close()
        flash('Agente não encontrado.', 'error')
        return redirect(url_for('agentes'))

    # Dados do formulário
    nome = request.form.get('nome')
    sobrenome = request.form.get('sobrenome')
    data_nasc = request.form.get('data_nasc')
    contato = request.form.get('contato_emergencia')
    elemento = request.form.get('elemento')
    classe = request.form.get('classe')
    ocupacao = request.form.get('ocupacao')
    marca = request.form.get('marca')
    equipe = request.form.get('equipe')
    status = request.form.get('status')
    observacoes = request.form.get('observacoes')

    # Mantém a imagem antiga por padrão
    imagem_path = agente['imagem']

    # Se enviou nova imagem
    imagem = request.files.get('imagem')
    if imagem and imagem.filename != '':
        imagem_path = salvar_imagem(imagem)  # função que salva e retorna o path relativo

    # Atualiza o agente
    cursor.execute("""
        UPDATE agentes
        SET nome=%s, sobrenome=%s, data_nasc=%s, contato_emergencia=%s,
            elemento=%s, classe=%s, ocupacao=%s, marca=%s, equipe=%s,
            status=%s, observacoes=%s, imagem=%s
        WHERE id=%s
    """, (nome, sobrenome, data_nasc, contato, elemento, classe,
          ocupacao, marca, equipe, status, observacoes, imagem_path, id))
    conn.commit()
    conn.close()

    flash('Agente atualizado com sucesso!', 'success')
    return redirect(url_for('agentes'))




# DELETAR AGENTE (GET -> mostra confirmação; POST -> executa exclusão)
@app.route('/deletar/<int:id>', methods=['GET', 'POST'])
def deletar(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Se for GET, mostra a página de confirmação
    if request.method == 'GET':
        cursor.execute("SELECT id, nome, sobrenome FROM agentes WHERE id = %s", (id,))
        agente = cursor.fetchone()
        conn.close()
        if not agente:
            flash('Agente não encontrado.')
            return redirect(url_for('agentes'))
        return render_template('confirmar_deletar.html', agente=agente)

    # Se for POST, executa a exclusão
    cursor.execute("DELETE FROM agentes WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash('Agente excluído com sucesso.')
    return redirect(url_for('agentes'))



# EQUIPES — geradas automaticamente pelos agentes
@app.route('/equipes')
def equipes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT equipe FROM agentes WHERE equipe IS NOT NULL AND equipe != ''")
    equipes = cursor.fetchall()

    equipes_com_agentes = []
    for e in equipes:
        nome_equipe = e['equipe']
        cursor.execute("SELECT nome, sobrenome, imagem FROM agentes WHERE equipe = %s", (nome_equipe,))
        membros = cursor.fetchall()
        equipes_com_agentes.append({'nome_equipe': nome_equipe, 'membros': membros})

    conn.close()
    return render_template('equipes.html', equipes_com_agentes=equipes_com_agentes)

@app.route('/editar_equipe/<nome_equipe>', methods=['GET', 'POST'])
def editar_equipe(nome_equipe):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca todos os agentes da equipe
    cursor.execute("SELECT * FROM agentes WHERE equipe = %s", (nome_equipe,))
    agentes = cursor.fetchall()

    if request.method == 'POST':
        novo_nome = request.form.get('novo_nome')
        if novo_nome:
            cursor.execute("UPDATE agentes SET equipe = %s WHERE equipe = %s", (novo_nome, nome_equipe))
            conn.commit()
            flash('Equipe renomeada com sucesso!')
            conn.close()
            return redirect(url_for('equipes'))

    conn.close()
    return render_template('editar_equipe.html', nome_equipe=nome_equipe, agentes=agentes)



# ÁREA C.R.I.S — para usuários comuns
@app.route('/area-cris')
def area_cris():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('agentes.html')

# ===============================
# CRUD DE CRIATURAS
# ===============================

@app.route('/criaturas', methods=['GET', 'POST'])
def criaturas():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('nome')
        elemento = request.form.get('elemento')
        local_encontrado = request.form.get('local_encontrado')
        descricao = request.form.get('descricao')
        raridade = request.form.get('raridade')
        imagem = request.files.get('imagem')
        imagem_path = salvar_imagem(imagem)

        cursor.execute("""
            INSERT INTO criaturas (nome, elemento, local_encontrado, descricao, raridade, imagem)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, elemento, local_encontrado, descricao, raridade, imagem_path))
        conn.commit()

    cursor.execute("SELECT * FROM criaturas")
    criaturas = cursor.fetchall()
    conn.close()
    return render_template('criaturas.html', criaturas=criaturas)


@app.route('/editar_criatura/<int:id>', methods=['GET', 'POST'])
def editar_criatura(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca os dados atuais da criatura
    cursor.execute("SELECT * FROM criaturas WHERE id=%s", (id,))
    criatura = cursor.fetchone()

    if not criatura:
        conn.close()
        flash('Criatura não encontrada.', 'error')
        return redirect(url_for('criaturas'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        elemento = request.form.get('elemento')
        local_encontrado = request.form.get('local_encontrado')
        descricao = request.form.get('descricao')
        raridade = request.form.get('raridade')

        # Mantém a imagem antiga por padrão (caso queira adicionar imagem futuramente)
        imagem_path = criatura.get('imagem', None)

        imagem = request.files.get('imagem')
        if imagem and imagem.filename != '':
            imagem_path = salvar_imagem(imagem)

        cursor.execute("""
            UPDATE criaturas
            SET nome=%s, elemento=%s, local_encontrado=%s, descricao=%s, raridade=%s, imagem=%s
            WHERE id=%s
        """, (nome, elemento, local_encontrado, descricao, raridade, imagem_path, id))

        conn.commit()
        conn.close()
        flash('Criatura atualizada com sucesso!', 'success')
        return redirect(url_for('criaturas'))

    conn.close()
    return render_template('editar_criatura.html', criatura=criatura)


@app.route('/deletar_criatura/<int:id>', methods=['GET', 'POST'])
def deletar_criatura(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM criaturas WHERE id=%s", (id,))
        criatura = cursor.fetchone()
        conn.close()
        return render_template('confirmar_deletar_criatura.html', criatura=criatura)

    cursor.execute("DELETE FROM criaturas WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash('Criatura excluída com sucesso!')
    return redirect(url_for('criaturas'))


# ===============================
# CRUD DE ITENS PARANORMAIS
# ===============================

@app.route('/itens', methods=['GET', 'POST'])
def itens():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('nome')
        elemento = request.form.get('elemento')
        efeito = request.form.get('efeito')
        num_categorico = request.form.get('num_categorico')
        raridade = request.form.get('raridade')
        imagem = request.files.get('imagem')
        imagem_path = salvar_imagem(imagem)

        cursor.execute("""
            INSERT INTO itens_paranormais (nome, elemento, efeito, num_categorico, raridade, imagem)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, elemento, efeito, num_categorico, raridade, imagem_path))
        conn.commit()

    cursor.execute("SELECT * FROM itens_paranormais")
    itens = cursor.fetchall()
    conn.close()
    return render_template('itens.html', itens=itens)


@app.route('/editar_item/<int:id>', methods=['GET', 'POST'])
def editar_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca os dados atuais do item
    cursor.execute("SELECT * FROM itens_paranormais WHERE id=%s", (id,))
    item = cursor.fetchone()

    if not item:
        conn.close()
        flash('Item não encontrado.', 'error')
        return redirect(url_for('itens'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        elemento = request.form.get('elemento')
        efeito = request.form.get('efeito')
        num_categorico = request.form.get('num_categorico')
        raridade = request.form.get('raridade')

        # Mantém a imagem antiga por padrão
        imagem_path = item.get('imagem', None)

        imagem = request.files.get('imagem')
        if imagem and imagem.filename != '':
            imagem_path = salvar_imagem(imagem)

        cursor.execute("""
            UPDATE itens_paranormais
            SET nome=%s, elemento=%s, efeito=%s, num_categorico=%s, raridade=%s, imagem=%s
            WHERE id=%s
        """, (nome, elemento, efeito, num_categorico, raridade, imagem_path, id))

        conn.commit()
        conn.close()
        flash('Item atualizado com sucesso!', 'success')
        return redirect(url_for('itens'))

    conn.close()
    return render_template('editar_item.html', item=item)



@app.route('/deletar_item/<int:id>', methods=['GET', 'POST'])
def deletar_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM itens_paranormais WHERE id=%s", (id,))
        item = cursor.fetchone()
        conn.close()
        return render_template('confirmar_deletar_item.html', item=item)

    cursor.execute("DELETE FROM itens_paranormais WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash('Item excluído com sucesso!')
    return redirect(url_for('itens'))

# RELATÓRIOS
# ===============================
# CRUD DE RELATÓRIOS
# ===============================

# LISTAR RELATÓRIOS
@app.route('/relatorios')
def relatorios():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relatorios ORDER BY data DESC")
    relatorios = cursor.fetchall()
    conn.close()
    return render_template('relatorios.html', relatorios=relatorios)


# ADICIONAR RELATÓRIO
@app.route('/adicionar_relatorio', methods=['GET', 'POST'])
def adicionar_relatorio():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        equipe = request.form['equipe']
        data = request.form['data']
        texto = request.form['texto']
        autoria = request.form['autoria']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO relatorios (nome, equipe, data, texto, autoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, equipe, data, texto, autoria))
        conn.commit()
        conn.close()
        return redirect(url_for('relatorios'))

    return render_template('adicionar_relatorio.html')


# EDITAR RELATÓRIO
@app.route('/editar_relatorio/<int:id>', methods=['GET', 'POST'])
def editar_relatorio(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relatorios WHERE id=%s", (id,))
    relatorio = cursor.fetchone()

    if not relatorio:
        conn.close()
        return "Relatório não encontrado."

    if request.method == 'POST':
        nome = request.form['nome']
        equipe = request.form['equipe']
        data = request.form['data']
        texto = request.form['texto']
        autoria = request.form['autoria']

        cursor.execute("""
            UPDATE relatorios
            SET nome=%s, equipe=%s, data=%s, texto=%s, autoria=%s
            WHERE id=%s
        """, (nome, equipe, data, texto, autoria, id))
        conn.commit()
        conn.close()
        return redirect(url_for('relatorios'))

    conn.close()
    return render_template('editar_relatorio.html', relatorio=relatorio)


# EXCLUIR RELATÓRIO
@app.route('/deletar_relatorio/<int:id>', methods=['GET', 'POST'])
def deletar_relatorio(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relatorios WHERE id=%s", (id,))
    relatorio = cursor.fetchone()

    if not relatorio:
        conn.close()
        return "Relatório não encontrado."

    if request.method == 'POST':
        cursor.execute("DELETE FROM relatorios WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('relatorios'))

    conn.close()
    return render_template('deletar_relatorio.html', relatorio=relatorio)

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
