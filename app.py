from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
import pymysql

app = Flask(__name__)
app.secret_key = 'segredo'
app.config['UPLOAD_FOLDER'] = 'uploads'

# garante que a pasta existe
os.makedirs(os.path.join(app.root_path, 'static', app.config['UPLOAD_FOLDER']), exist_ok=True)

# conexão com o banco
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  # senha padrão do XAMPP
        database='c.r.i.s',
        cursorclass=pymysql.cursors.DictCursor
    )

# salva imagem no static/uploads
def salvar_imagem(imagem):
    if imagem and imagem.filename:
        filename = secure_filename(imagem.filename)
        caminho_relativo = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
        caminho_completo = os.path.join(app.root_path, 'static', caminho_relativo)
        imagem.save(caminho_completo)
        return caminho_relativo
    return ''

# rota de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

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

# dashboard do admin
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session or session['usuario_id'] != 1:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# CRUD de usuários (apenas admin)
@app.route('/usuarios')
def usuarios():
    if 'usuario_id' not in session or session['usuario_id'] != 1:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/criar', methods=['GET', 'POST'])
def criar_usuario():
    if 'usuario_id' not in session or session['usuario_id'] != 1:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        imagem = request.files.get('imagem')
        imagem_path = salvar_imagem(imagem)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, senha, imagem) VALUES (%s, %s, %s)", (username, senha, imagem_path))
        conn.commit()
        conn.close()
        return redirect(url_for('usuarios'))
    return render_template('criar_usuario.html')

# agentes
@app.route('/agentes', methods=['GET', 'POST'])
def agentes():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        data_nasc = request.form['data_nasc']
        contato = request.form['contato_emergencia']
        elemento = request.form['elemento']
        classe = request.form['classe']
        observacoes = request.form['observacoes']
        status = request.form['status']
        ocupacao = request.form['ocupacao']
        marca = request.form['marca']
        equipe = request.form['equipe']
        imagem = request.files.get('imagem')
        imagem_path = salvar_imagem(imagem)

        cursor.execute("""
            INSERT INTO agentes (nome, sobrenome, data_nasc, contato_emergencia, elemento, classe,
                                 observacoes, imagem, status, ocupacao, marca, equipe)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nome, sobrenome, data_nasc, contato, elemento, classe, observacoes, imagem_path, status, ocupacao, marca, equipe))
        conn.commit()

    cursor.execute("SELECT * FROM agentes")
    agentes = cursor.fetchall()
    conn.close()
    return render_template('agentes.html', agentes=agentes)

# equipes (geradas a partir dos agentes)
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

# área C.R.I.S (para usuários comuns)
@app.route('/area-cris')
def area_cris():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('area_cris.html')

# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
