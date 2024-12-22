from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy nesnesi burada tanımlanıyor
db = SQLAlchemy()

# Modeller
class tblusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(20), nullable=False)


class tblmediaandtext(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(50), unique=False, nullable=False, default='')
    label = db.Column(db.String(100), unique=False, nullable=True)
    path = db.Column(db.String(50), unique=False, nullable=False, default='')
    file_name = db.Column(db.String(255), nullable=False, default='')
    text1 = db.Column(db.String(5000), nullable=True)
    text2 = db.Column(db.String(5000), nullable=True)

class tblcomputerfiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), unique=False, nullable=True)
    path = db.Column(db.String(50), unique=False, nullable=True)
    videocard = db.Column(db.String(100), unique=False, nullable=True)
    mothercard = db.Column(db.String(100), unique=False, nullable=True)
    freez = db.Column(db.String(100), unique=False, nullable=True)
    mouse = db.Column(db.String(100), unique=False, nullable=True)
    headphone = db.Column(db.String(100), unique=False, nullable=True)
    processor = db.Column(db.String(100), unique=False, nullable=True)
    ram = db.Column(db.String(100), unique=False, nullable=True)
    screen = db.Column(db.String(100), unique=False, nullable=True)
    keyboard = db.Column(db.String(100), unique=False, nullable=True)
    
    
class tblfoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(50), unique=False, nullable=True)
    label = db.Column(db.String(100), unique=False, nullable=True)
    text = db.Column(db.String(5000), unique=False, nullable=True)
    order_index = db.Column(db.Integer, unique=False, nullable=True)

class tblgames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iconpath = db.Column(db.String(50), unique=False, nullable=True)
    photopath = db.Column(db.String(50), unique=False, nullable=True)    
    gamename = db.Column(db.String(100), unique=False, nullable=True)
    text = db.Column(db.String(5000), unique=False, nullable=True)

class tblsteams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iconpath = db.Column(db.String(50), unique=False, nullable=True)
    gamename = db.Column(db.String(100), unique=False, nullable=True)
    steamname = db.Column(db.String(100), unique=False, nullable=True)

class tblservice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagepath = db.Column(db.String(50), unique=False, nullable=True)
    name = db.Column(db.String(100), unique=False, nullable=True)