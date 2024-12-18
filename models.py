from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy nesnesi burada tanımlanıyor
db = SQLAlchemy()

# Modeller
class tblusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(20), nullable=False)

class tblmedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(50), unique=False, nullable=False, default='')
    file_name = db.Column(db.String(255), nullable=False, default='')

class tbltext(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photoid = db.Column(db.Integer, db.ForeignKey('tblmedia.id'), nullable=True)
    label = db.Column(db.String(100), unique=False, nullable=True)
    page_name = db.Column(db.String(50), unique=False, nullable=False, default='')
    id_name = db.Column(db.String(50), unique=False, nullable=False, default='')
    text = db.Column(db.String(5000), unique=False, nullable=True)

class tblfoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(50), unique=False, nullable=False, default='cafeattributepage')
    photopath = path = db.Column(db.String(50), unique=False, nullable=False, default='')
    label = db.Column(db.String(100), unique=False, nullable=True)
    text = db.Column(db.String(5000), unique=False, nullable=True)
    order_index = db.Column(db.Integer, unique=False, nullable=False, default=0 )

