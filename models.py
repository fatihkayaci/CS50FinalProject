from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy nesnesi burada tanımlanıyor
db = SQLAlchemy()

# Modeller
class users_tbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(20), nullable=False)

class text_tbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), unique=False, nullable=False)
    id_name = db.Column(db.String(50), unique=False, nullable=False)
    text = db.Column(db.String(5000), unique=False, nullable=True)

class media_tbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), db.ForeignKey('text_tbl.group_name'), nullable=False)
    path = db.Column(db.String(50), unique=False, nullable=False)
    file_name = db.Column(db.String(255), nullable=False, default='')
    active = db.Column(db.Boolean, nullable=False, default=True)
    order_index = db.Column(db.Integer, nullable=False, unique=False)