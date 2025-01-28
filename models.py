from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy nesnesi burada tanımlanıyor
db = SQLAlchemy()

# Modeller
class tblusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(20), nullable=False)

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
    text = db.Column(db.String(5000), unique=False, nullable=False, default=gamename)

class tblsteams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamname = db.Column(db.String(100), unique=False, nullable=True)
    
class tblsteamgame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamid = db.Column(db.Integer, db.ForeignKey('tblsteams.id'), nullable=False)
    gameid = db.Column(db.Integer, db.ForeignKey('tblgames.id'), nullable=False)

class tblservice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagepath = db.Column(db.String(50), unique=False, nullable=True)
    name = db.Column(db.String(100), unique=False, nullable=True)

class tblarsive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagepath = db.Column(db.String(50), unique=False, nullable=True)

class tblsettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False, default="Dost Oyun Merkezi")
    logopath = db.Column(db.String(50), unique=False, nullable=False, default="img/generalsettings/logo.webp")
    number = db.Column(db.String(100), unique=False, nullable=False, default="05302090732")
    mail = db.Column(db.String(100), unique=False, nullable=False, default="posta@teknikdost.com")
    adress = db.Column(db.String(100), unique=False, nullable=False, default="Dost Kafe, Tarabya, Çıra Sk. no 26, 34457 Sarıyer/İstanbul")

class BaseModel(db.Model):
    __abstract__ = True
    page_name = db.Column(db.String(50), unique=False, nullable=True)
    title = db.Column(db.String(100), unique=False, nullable=True)

class tbltext(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    text_message = db.Column(db.String(5000), nullable=True)

class tblmedia(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(50), unique=False, nullable=True)