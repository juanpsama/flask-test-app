from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))

    posts = relationship("Document", back_populates="author")
    def to_dict(self):
        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}   

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    folio = db.Column(db.String(250), nullable = False)
    description = db.Column(db.Text, nullable = False)
    creation_date = db.Column(db.Date, nullable = False) 

    # Property to perform logic elimination
    is_active = db.Column(db.Boolean, nullable = False, default = True)
    
    #Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("User", back_populates="posts")

    files = relationship("File", back_populates="document")

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(250), nullable=False)

    # Create Foreign Key 
    # "documents.id" the users refers to the tablename of User.
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"))

    # Create reference to the Document object, the "files" refers to the files protperty in the Document class.
    document = relationship("Document", back_populates = 'files')
