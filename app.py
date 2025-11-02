from flask import Flask, render_template, request, redirect, url_for, session, flash
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

# Função para salvar imagens em static/uploads
def salvar_imagem(imagem):
    if imagem and imagem.filename:
        filename = secure_filename(imagem.filename)
        caminho_relativo = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
        caminho_completo = os.path.join(app.root_path, 'static', caminho_relativo)

        # Evita sobrescrever imagem existente
        base, ext = os.path.splitext(filename)
        contador = 1
        while os.path.exists(caminho_completo):
            filename = f"{base}_{contador}{ext}"
            caminho_relativo = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
            caminho_completo = os.path.join(app.root_path, 'static', caminho_relativo)
            contador += 1

        imagem.save(caminho_completo)
        return caminho_relativo
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
                return redirect(url_for('area_cris'))
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
@app.route('/usuarios')
def usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)



# CRIAR USUÁRIO
@app.route('/criar_usuario', methods=['GET', 'POST'])
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
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
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
@app.route('/deletar_usuario/<int:id>')
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

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        elemento = request.form.get('elemento')
        classe = request.form.get('classe')
        status = request.form.get('status')
        ocupacao = request.form.get('ocupacao')
        marca = request.form.get('marca')
        equipe = request.form.get('equipe')
        observacoes = request.form.get('observacoes')

        cursor.execute("""
            UPDATE agentes
            SET nome=%s, sobrenome=%s, elemento=%s, classe=%s, status=%s,
                ocupacao=%s, marca=%s, equipe=%s, observacoes=%s
            WHERE id=%s
        """, (nome, sobrenome, elemento, classe, status, ocupacao, marca, equipe, observacoes, id))
        conn.commit()
        conn.close()
        flash('Agente atualizado com sucesso!')
        return redirect(url_for('agentes'))

    # exibe dados do agente para edição
    cursor.execute("SELECT * FROM agentes WHERE id = %s", (id,))
    agente = cursor.fetchone()
    conn.close()
    return render_template('editar_agente.html', agente=agente)

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
    return render_template('area_cris.html')

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

    if request.method == 'POST':
        nome = request.form.get('nome')
        elemento = request.form.get('elemento')
        local_encontrado = request.form.get('local_encontrado')
        descricao = request.form.get('descricao')
        raridade = request.form.get('raridade')

        cursor.execute("""
            UPDATE criaturas SET nome=%s, elemento=%s, local_encontrado=%s, descricao=%s, raridade=%s
            WHERE id=%s
        """, (nome, elemento, local_encontrado, descricao, raridade, id))
        conn.commit()
        conn.close()
        flash('Criatura atualizada com sucesso!')
        return redirect(url_for('criaturas'))

    cursor.execute("SELECT * FROM criaturas WHERE id=%s", (id,))
    criatura = cursor.fetchone()
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

    if request.method == 'POST':
        nome = request.form.get('nome')
        elemento = request.form.get('elemento')
        efeito = request.form.get('efeito')
        num_categorico = request.form.get('num_categorico')
        raridade = request.form.get('raridade')

        cursor.execute("""
            UPDATE itens_paranormais
            SET nome=%s, elemento=%s, efeito=%s, num_categorico=%s, raridade=%s
            WHERE id=%s
        """, (nome, elemento, efeito, num_categorico, raridade, id))
        conn.commit()
        conn.close()
        flash('Item atualizado com sucesso!')
        return redirect(url_for('itens'))

    cursor.execute("SELECT * FROM itens_paranormais WHERE id=%s", (id,))
    item = cursor.fetchone()
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



# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
