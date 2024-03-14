import os 
from datetime import datetime

from flask import Flask, render_template, flash, url_for, redirect, request, send_from_directory
from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

from forms import loginForm, DocumentForm
from models import db, User, Document, File

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY', 'secretkey1234423')

app.config['UPLOADS_DEFAULT_DEST'] =  'files/'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL',"sqlite:///posts.db")
db.init_app(app)

migrate = Migrate(app, db, command='migrate')


# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app) 

def redirect_unauthorized():
    flash('Registrate antes de acceder a la pagina !!')
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect_unauthorized()

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, user_id)
    return user

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('get_documents'))
    return redirect(url_for('login'))


@app.route('/login', methods = ['POST', 'GET'])
def login():
    login_form = loginForm()
    if login_form.validate_on_submit():

        # Get form data 
        username = login_form.username.data
        password = login_form.password.data

        # Retrieve a user from the database based on their name 
        user = db.session.execute(db.select(User).where(User.name == username)).scalar()
        if user:

            if check_password_hash(user.password, password):
                # Create user session
                login_user(user)
                return redirect(url_for('get_documents'))
            
            flash('Contraseña incorrecta, porfavor intenta de nuevo.')
        flash('Ese email no esta registrado, porfavor intenta de nuevo!!')

    return render_template('login.html', form = login_form, action = url_for('login'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    register_form = loginForm()
    if register_form.validate_on_submit():

        # Get form data 
        username = register_form.username.data
        password = register_form.password.data
       
        user = db.session.execute(db.select(User).where(User.name == username)).scalar()
        if user:
            flash('Ese nombre de usuario ya existe porfavor log in.')
            return redirect(url_for('login'))
        
        # Use Werkzeug to hash the user's password when creating a new user.
        hash_password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8) 

        # Create new User object to the database
        new_user = User(
            name = username,
            password = hash_password,
        )

        db.session.add(new_user)

        # Commit changues to the db 
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('login.html', form = register_form, action = url_for('register'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# CRUD operations with documents
@app.route('/get-document/<int:document_id>')
@login_required
def get_single_document(document_id):

    # Get document requested from the db
    document = db.get_or_404(Document, document_id)
    return render_template('single_document.html', document = document )

@app.route('/delete-document/<int:document_id>')
@login_required
def delete_document(document_id):

    # Get document requested from the db
    document_to_delete = db.get_or_404(Document, document_id)

    # Logic elimination
    document_to_delete.is_active = False

    # Complete elimination
    # db.session.delete(document_to_delete)

    db.session.commit()
    return redirect(url_for('get_documents'))

@app.route('/update-document/<int:document_id>', methods = ['POST', 'GET'])
@login_required
def update_document(document_id):
    document_to_update = db.get_or_404(Document, document_id)

    # Prefill form with the database data
    form = DocumentForm(
        name = document_to_update.name,
        folio = document_to_update.folio,
        description = document_to_update.description,
        date = document_to_update.creation_date 
    )

    if form.validate_on_submit():
        document_to_update.name = form.name.data
        document_to_update.description = form.description.data
        document_to_update.creation_date = form.date.data
        document_to_update.folio = form.folio.data

        files = form.file.data 

        # Create filenames based of the original name and the current date
        file_paths = [os.path.join(
                        app.config['UPLOADS_DEFAULT_DEST'], 
                        f'{str(datetime.now()).replace(" ", "_").replace(":",".")}{current_user.id}{os.path.splitext(file.filename)[1]}') 
                        for file in files]
        
        # Save all the files 
        for i in range(len(files)):
            files[i].save(file_paths[i])

        # Store file paths in the database
        for path in file_paths:
            new_file = File(
                file_url = path,
                document = document_to_update
            )
            db.session.add(new_file)    

        db.session.commit()
        return redirect(url_for('get_documents'))

    return render_template('new_document.html', form = form, action = url_for('update_document', document_id = document_to_update.id))


@app.route('/documents')
@login_required
def get_documents():
    # Get all documents with is_active set on True
    documents = db.session.execute(db.select(Document).where(Document.is_active == True)).scalars().all()
    return render_template("get_documents.html", documents=documents)

@app.route('/new-document', methods = ['GET', 'POST'])
@login_required
def new_document():
    form = DocumentForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        date = form.date.data
        folio = form.folio.data
        files = form.file.data

        new_document = Document(
            name = name,
            description = description,
            creation_date = date,
            folio = folio,
            author = current_user,
            is_active = True
        )

        db.session.add(new_document)

        # Create filenames based of the original name and the current date
        file_paths = [os.path.join(
                        app.config['UPLOADS_DEFAULT_DEST'], 
                        f'{str(datetime.now()).replace(" ", "_").replace(":",".")}{current_user.id}{os.path.splitext(file.filename)[1]}') 
                        for file in files]
        
        # Save all the files 
        for i in range(len(files)):
            files[i].save(file_paths[i])
        # Store file paths in the database
        for path in file_paths:
            new_file = File(
                file_url = path,
                document = new_document
            )
            db.session.add(new_file)    

        db.session.commit()
        return redirect(url_for('get_documents'))

    return render_template('new_document.html', form = form, action = url_for('new_document'))

@app.route('/file/<int:file_id>')
@login_required
def serve_file(file_id):
    filename = db.get_or_404(File, file_id)
    uploads = app.root_path
    # filename = db.session.execute(db.select(File).where(File.file_url == file_name)).scalars().all()

    # Store the files in the project directory
    return send_from_directory(uploads, filename.file_url)

if __name__ == '__main__':
    app.run(port=3000, debug=True)