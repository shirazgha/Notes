from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.secret_key = "Secret Key"

# Configuration de la base de données SqlAlchemy avec Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/notesetudiant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#table data/etudant
#Création d'une table modèle pour notre base de données notesetudiant
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   # Ninscription = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
  # Moyenne_Ninscription = db.Column(db.Integer, Foreign_Key(Data_Ninscription), primary_key=True)
    phone = db.Column(db.String(100))
    NumCin = db.Column(db.Integer)
    age = db.Column(db.Integer)

    def __init__(self, name, email, phone, NumCin, age):
        self.name = name
        self.email = email
        self.phone = phone
        self.NumCin = NumCin
        self.age = age

# requête sur toutes les données de nos etudiants
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", etudiants=all_data)


# cette route est pour insérer des données dans la base de données mysql via des formulaires html
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        NumCin = request.form['NumCin']
        age = request.form['age']

        my_data = Data(name, email, phone, NumCin, age)
        db.session.add(my_data)
        db.session.commit()

        flash("étudiant inséré avec succès")

        return redirect(url_for('Index'))


# c'est notre route de mise à jour où nous allons mettre à jour notre etudiant
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.NumCin = request.form['NumCin']
        my_data.age = request.form['age']

        db.session.commit()
        flash("étudiant modifié avec succès")

        return redirect(url_for('Index'))


# c'est notre route de suppression où nous allons  supprimer notre etudiant
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("étudiant supprimé avec succès  ")

    return redirect(url_for('Index'))

#table matiere
#Création de la table matiere
class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codemat  = db.Column(db.Integer)
    libelle = db.Column(db.String(100))
    coefficient = db.Column(db.Integer)

    def __init__(self, codemat, libelle, coefficient):
        self.codemat = codemat
        self.libelle = libelle
        self.coefficient = coefficient


# requête sur toutes les données des matieres
@app.route('/matiere')
def Home():
    all_matiere = Matiere.query.all()

    return render_template("home.html", matieres=all_matiere)


# cette route est pour insérer des matières
@app.route('/insertmatiere', methods=['POST'])
def insertmatiere():
    if request.method == 'POST':
        codemat = request.form['codemat']
        libelle = request.form['libelle']
        coefficient = request.form['coefficient']

        my_matiere = Matiere(codemat, libelle, coefficient)
        db.session.add(my_matiere)
        db.session.commit()

        flash("matière insérée avec succès")

        return redirect(url_for('Home'))

# c'est notre route de mise à jour où nous allons mettre à jour une matière

@app.route('/updatematiere', methods=['GET', 'POST'])
def updatematiere():
    if request.method == 'POST':
        my_matiere = Matiere.query.get(request.form.get('id'))

        my_matiere.codemat = request.form['codemat']
        my_matiere.libelle = request.form['libelle']
        my_matiere.coefficient = request.form['coefficient']

        db.session.commit()
        flash("matière modifiée avec succès")

        return redirect(url_for('Home'))




# c'est notre route de suppression où nous allons  supprimer une matière
@app.route('/deletematiere/<id>/', methods=['GET', 'POST'])
def deletematiere(id):
    my_matiere = Matiere.query.get(id)
    db.session.delete(my_matiere)
    db.session.commit()
    flash("matiere supprimée avec succès  ")

    return redirect(url_for('Home'))

#table s1note
#Création de la table s1note

class S1Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NoteDs = db.Column(db.Float,nullable=False)
    NoteExam = db.Column(db.Float,nullable=False)
    NoteTp = db.Column(db.Float,nullable=False)
    data=db.Column(db.Integer,db.ForeignKey('data.id'),nullable=False)
    matiere = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)

    def __init__(self, NoteDs, NoteExam, NoteTp, data, matierre):
        self.NoteDs = NoteDs
        self.NoteExam = NoteExam
        self.NoteTp = NoteTp
        self.data=data
        self.matiere=matierre



# requête sur toutes les données des notes
@app.route('/s1note')
def Static():
    all_s1note = S1Note.query.all()
    all_data = Data.query.all()
    all_matiere = Matiere.query.all()
    return render_template("static.html", s1notes=all_s1note, etudiants=all_data, matieres=all_matiere)


# cette route est pour insérer des notes
@app.route('/insertnote', methods=['POST'])
def insertnote():
    if request.method == 'POST':
        NoteDs = request.form['NoteDs']
        NoteExam = request.form['NoteExam']
        NoteTp = request.form['NoteTp']
        data = request.form['data']
        matiere = request.form['matiere']

        my_note = S1Note(NoteDs, NoteExam, NoteTp, data, matiere)
        db.session.add(my_note)
        db.session.commit()

        flash("note insérée avec succès")

        return redirect(url_for('Static'))


# c'est notre route de mise à jour où nous allons mettre à jour une note

@app.route('/updatenote', methods=['GET', 'POST'])
def updatenote():
    if request.method == 'POST':
        my_note = S1Note.query.get(request.form.get('id'))

        my_note.NoteDs = request.form['NoteDs']
        my_note.NoteExam = request.form['NoteExam']
        my_note.NoteTp = request.form['NoteTp']

        db.session.commit()
        flash("note modifiée avec succès")

        return redirect(url_for('Static'))




# c'est notre route de suppression où nous allons  supprimer une note
@app.route('/deletenote/<id>/', methods=['GET', 'POST'])
def deletenote(id):
    my_note = S1Note.query.get(id)
    db.session.delete(my_note)
    db.session.commit()
    flash("note supprimée avec succès  ")

    return redirect(url_for('Static'))





#table spécialité
#Création de la table spécialité
class Specialite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle =db.Column(db.String(100))
    code = db.Column(db.Integer)
    data = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

    def __init__(self, libelle, code, data):
        self.libelle = libelle
        self.code = code
        self.data = data

     # Interface specialité

    # requête sur toutes les données des notes


@app.route('/specialite')
def About():
    all_data = Data.query.all()
    all_specialite = Specialite.query.all()
    return render_template("specialite.html", specialites=all_specialite, etudiants=all_data)



# cette route est pour insérer des notes
@app.route('/insertspecialite', methods=['POST'])
def insertspecialite():
    if request.method == 'POST':
        Libelle = request.form['libelle']
        code = request.form['code']
        data = request.form['data']

        my_specialite = Specialite(Libelle, code, data)
        db.session.add(my_specialite)
        db.session.commit()

        flash("spécialité insérée avec succès")

        return redirect(url_for('About'))







# c'est notre route de mise à jour où nous allons mettre à jour une note

@app.route('/updatespecialite', methods=['GET', 'POST'])
def updatespecialite():
    if request.method == 'POST':
        my_specialite = Specialite.query.get(request.form.get('id'))

        my_specialite.libelle = request.form['libelle']
        my_specialite.code = request.form['code']


        db.session.commit()
        flash("specialité modifiée avec succès")

        return redirect(url_for('About'))




# c'est notre route de suppression où nous allons  supprimer une spécialité
@app.route('/deletespecialite/<id>/', methods=['GET', 'POST'])
def deletespecialite(id):
    my_specialite = Specialite.query.get(id)
    db.session.delete(my_specialite)
    db.session.commit()
    flash("spécialité supprimée avec succès  ")

    return redirect(url_for('About'))





#table s2note
#Création de la table s2note

class S2Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NoteDs = db.Column(db.Float,nullable=False)
    NoteExam = db.Column(db.Float,nullable=False)
    NoteTp = db.Column(db.Float,nullable=False)
    data=db.Column(db.Integer,db.ForeignKey('data.id'),nullable=False)
    matiere = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)

    def __init__(self, NoteDs, NoteExam, NoteTp, data, matierre):
        self.NoteDs = NoteDs
        self.NoteExam = NoteExam
        self.NoteTp = NoteTp
        self.data=data
        self.matiere=matierre



# requête sur toutes les données des notes
@app.route('/s2note')
def Server():
    all_s2note = S2Note.query.all()
    all_data = Data.query.all()
    all_matiere = Matiere.query.all()
    return render_template("page.html", s2notes=all_s2note, etudiants=all_data, matieres=all_matiere)


# cette route est pour insérer des notes
@app.route('/insertnotes2', methods=['POST'])
def insertnotes2():
    if request.method == 'POST':
        NoteDs = request.form['NoteDs']
        NoteExam = request.form['NoteExam']
        NoteTp = request.form['NoteTp']
        data = request.form['data']
        matiere = request.form['matiere']

        my_note = S2Note(NoteDs, NoteExam, NoteTp, data, matiere)
        db.session.add(my_note)
        db.session.commit()

        flash("note insérée avec succès")

        return redirect(url_for('Server'))


# c'est notre route de mise à jour où nous allons mettre à jour une note

@app.route('/updatenotes2', methods=['GET', 'POST'])
def updatenotes2():
    if request.method == 'POST':
        my_note = S2Note.query.get(request.form.get('id'))

        my_note.NoteDs = request.form['NoteDs']
        my_note.NoteExam = request.form['NoteExam']
        my_note.NoteTp = request.form['NoteTp']

        db.session.commit()
        flash("note modifiée avec succès")

        return redirect(url_for('Server'))

# c'est notre route de suppression où nous allons  supprimer une note
@app.route('/deletenotes2/<id>/', methods=['GET', 'POST'])
def deletenotes2(id):
    my_note = S2Note.query.get(id)
    db.session.delete(my_note)
    db.session.commit()
    flash("note supprimée avec succès  ")

    return redirect(url_for('Server'))






@app.route("/moyenne")
@login_required
def Moy(self):
    x = 0
    y = 0
    z = 0
    sommeNotes = 0
    moyen = 0
    u = 0
    s1Notes = S1Note.query.all()
    etudiants = Data.query.all()
    matieres = Matiere.query.all()
    for etudiant in etudiants:
        sommeNotes = 0
        i = etudiant.id
        nbrNotes = S1Note.query.filter_by(data=i).count()
        notesEtudiants = S1Note.query.filter_by(data=i).all()
        for notesEtudiant in notesEtudiants:
            sommeNotes = (((0.2 * float(notesEtudiant.NoteDs)) + (0.3 * float(notesEtudiant.NoteTp)) + (
                    0.5 * float(notesEtudiant.NoteExam))) + float(sommeNotes))

            moyen = sommeNotes / nbrNotes

        print('nombre note', nbrNotes)
        print(z)
        print('somme ', sommeNotes)
        print('moyen ', moyen)

    return render_template('moy.html', x=x, notesEtudiants=notesEtudiants, z=z, nbrNotes=nbrNotes,
                           matieres=matieres, etudiants=etudiants, s1Notes=s1Notes)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('Index'))

        return '<h1>nom ou mot de passe Admin invalide   </h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> Admin ajouté avec succès  !</h1>'

        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)