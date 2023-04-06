from crypt import methods
from mailbox import NotEmptyError
from flask import Flask, render_template, request, redirect, url_for, flash
from TOKEN import ApiMovies
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

frutas = []


class cursos(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch
    


@app.route('/', methods=["GET", "POST"])
def principal():

    if request.method == 'POST':
        if request.form.get('fruta'):
            frutas.append(request.form.get('fruta'))

    return render_template('index.html', frutas=frutas)



notas = {}


@app.route('/sobre', methods=["POST", "GET"])
def sobre():

    if request.method == 'POST':
        if request.form.get('nome') and request.form.get('nota'):
            notas[request.form.get('nome')] = request.form.get('nota')

    return render_template('sobre.html', notas=notas)


@app.route('/filmes/<propriedade>')
def filmes(propriedade):

    opt = {'populares':'/discover/movie?sort_by=popularity.desc',
            'best_2010':'/discover/movie?primary_release_year=2010&sort_by=vote_average.desc',
            'drama':'/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10'}

    filmes = ApiMovies(opt[propriedade]).list_filmes()
    return render_template("filmes.html", filmes=filmes)



@app.route('/cursos')
def lista_cursos():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    todos_cursos = cursos.query.paginate(page, per_page)


    return render_template('cursos.html', cursos=todos_cursos)
    
@app.route('/cria_curso', methods=['GET', 'POST'])
def cria_curso():

    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == 'POST':
        if not nome or not descricao or not ch:
            flash('Preencha Todos os campos do formulário', 'error')
        else:
            curso = cursos(nome, descricao, ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))
    
    return render_template('novo_curso.html')

@app.route('/<int:id>/atualiza_curso', methods=['POST', 'GET'])
def atualiza_curso(id):

    curso = cursos.query.filter_by(id=id).first()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        ch = request.form['ch']

        cursos.query.filter_by(id=id).update({'nome':nome, 'descricao': descricao, 'ch': ch})
        db.session.commit()

        return redirect(url_for('lista_cursos'))

    return render_template('atualiza_curso.html', curso=curso)

@app.route('/<int:id>/remove_curso', methods=['POST', 'GET'])
def remove_curso(id):

    curso = cursos.query.filter_by(id=id).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('lista_cursos'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)