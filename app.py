import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.templating import render_template
from models import db, tblusers, tblmediaandtext, tblfoods, tblcomputerfiles, tblgames, tblsteams
from flask_migrate import Migrate, migrate
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)

# bakılacak
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# burayakadar
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dostcafe.db'

db.init_app(app)

# sessions 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
migrate = Migrate(app, db)

@app.route("/")
def indexp():
    return render_template("indexp.html")

@app.route("/cafeattribute")
def cafeattribute():
    return render_template("cafeattribute.html")

# admin paneli
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            flash("Kullanıcı Adı Giriniz!")
            return render_template("/login.html") 

        if not password:
            flash("Şifrenizi Giriniz!")
            return render_template("/login.html")
        
        user = tblusers.query.filter_by(user_name = username).first()
        if user and user.password == password:
            return render_template("/indexa.html", user = user)
        else:
            return render_template("/login.html")
        
        # profiles = users.query.all()
    return render_template("/login.html")



@app.route("/indexa", methods=["GET", "POST"])
def indexa():                   
    mediawithtext = tblmediaandtext.query.filter_by(page_name = "mainpage").all()
    return render_template("indexa.html", mediawithtext=mediawithtext)


@app.route("/computerfiles")
def cafeattributea():
    computers = tblcomputerfiles.query.all()
    return render_template("/computerfiles.html", computers = computers)

# foods process
@app.route("/foodsadd", methods=['GET', 'POST'])
def foodsadd():
    if request.method == "POST":
        foodname = request.form.get('foodName')
        foodtext = request.form.get('foodText')
        foodimage = request.files.get('image')
        if not foodname and not foodtext and not foodimage:
            return jsonify({"success": False, "message": f"Hata oluştu: hepsi boş kaldı doldurunuz"})
        if foodimage and foodimage.filename:  
            if allowed_file(foodimage.filename):
                filename = secure_filename(foodimage.filename)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'foods/', filename)
                newfood = tblfoods(path=file_path, label=foodname, text=foodtext)
                db.session.add(newfood)
            if not os.path.exists(file_path):
                foodimage.save(file_path)
        elif not foodimage :
            newfood = tblfoods(path="", label=foodname, text=foodtext)
            db.session.add(newfood)

        db.session.commit()        
        return render_template("/foodsadd.html")
    foods = tblfoods.query.all()
    return render_template("/foodsadd.html", foods=foods)

# delete food
@app.route("/deletefood", methods=['GET', 'POST'])
def deletefood():
    if request.method == "POST":
        foodid = request.form.get('foodid')
        if not foodid:  # foodid boşsa hata dön
            return {'status': 'error', 'message': 'Food ID is missing'}, 400
        print(foodid)
        food_to_delete = tblfoods.query.get(foodid)
        if food_to_delete:
            db.session.delete(food_to_delete)
            db.session.commit()
        return 'succesfull'
    return 'str'

#update food
@app.route("/updatefood/<int:id>", methods=['GET', 'POST'])
def updatefood(id):
    if request.method == "POST":
        all_images = []
        target_folder = os.path.join(UPLOAD_FOLDER, 'mainpage')
        if os.path.exists(target_folder):
            all_images = [file for file in os.listdir(target_folder) 
                        if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
        id = request.form.get('id')
        label = request.form.get("label")
        text = request.form.get("text")
        image = request.files.get('image')
        foods = tblfoods.query.filter_by(id = id).first()
        if foods:
            foods.label = label
            foods.text = text
            if image:    
                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'foods/', filename)
                    foods.path = file_path
                if not os.path.exists(file_path):
                    image.save(file_path)

        db.session.commit()
        return render_template('/foodsadd.html')

    foods = tblfoods.query.filter_by(id = id).first()
    if foods is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
    return render_template("/updatepage/updatefood.html", foods=foods)
# games process
def savefilegames(file, upload_folder, subfolder='games/'):
    """Dosyayı güvenli bir şekilde kaydeder ve dosya yolu döner."""
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, subfolder, filename)
    if not os.path.exists(file_path):
        file.save(file_path)
    return file_path

@app.route("/gamesadd", methods=['GET', 'POST'])
def gamesadd():
    if request.method == "POST":
        gamename = request.form.get('gamename')
        gametext = request.form.get('gametext')
        gameimage = request.files.get('image')
        gameicon = request.files.get('icon')

        if not gamename and not gametext and not gameimage and not gameicon:
            return jsonify({"success": False, "message": "Hata oluştu: Lütfen tüm alanları doldurunuz"})
        
        # Yeni oyun kaydı oluştur
        newgame = tblgames(gamename=gamename, text=gametext)

        # Oyun resmi kontrolü ve kaydı
        if gameimage and gameimage.filename and allowed_file(gameimage.filename):
            newgame.photopath = savefilegames(gameimage, app.config['UPLOAD_FOLDER'])

        # Oyun ikonu kontrolü ve kaydı
        if gameicon and gameicon.filename and allowed_file(gameicon.filename):
            newgame.iconpath = savefilegames(gameicon, app.config['UPLOAD_FOLDER'])

        # Eğer hiç resim veya ikon eklenmediyse boş path'li bir kayıt ekle
        if not newgame.photopath and not newgame.iconpath:
            newgame.photopath = ""
            newgame.iconpath = ""

        db.session.add(newgame)
        db.session.commit()

        return jsonify({"success": True, "message": "Oyun başarıyla eklendi."})
    games = tblgames.query.all()
    return render_template("/gamesadd.html", games=games)

@app.route("/deletegame", methods=['GET', 'POST'])
def deletegame():
    if request.method == "POST":
        gameid = request.form.get('gameid')
        if not gameid:  # foodid boşsa hata dön
            return {'status': 'error', 'message': 'Food ID is missing'}, 400
        print(gameid)
        game_to_delete = tblgames.query.get(gameid)
        if game_to_delete:
            db.session.delete(game_to_delete)
            db.session.commit()
        return 'succesfull'
    return 'str'

@app.route("/updategame/<int:id>", methods=['GET', 'POST'])
def updategame(id):
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'mainpage')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
        
    if request.method == "POST":
        id = request.form.get('id')
        gamename = request.form.get('gamename')
        gametext = request.form.get('gametext')
        image = request.files.get('image')
        icon = request.files.get('icon')
        games = tblgames.query.filter_by(id = id).first()
        if games:
            games.gamename = gamename
            games.gametext = gametext
            if image:    
                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/', filename)
                    games.photopath = file_path
                if not os.path.exists(file_path):
                    image.save(file_path)
            if icon:
                if allowed_file(icon.filename):
                    filename = secure_filename(icon.filename)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/icon/', filename)
                    games.iconpath = file_path
                if not os.path.exists(file_path):
                    icon.save(file_path)

        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    games = tblgames.query.filter_by(id = id).first()
    if games is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
    return render_template("/updatepage/updategame.html", games=games)

@app.route("/steamsadd")
def steamsadd():
    steams = tblsteams.query.all()
    return render_template("/steamsadd.html", steams=steams)

# düzenleme kısmı
@app.route("/updatemainpage/<int:id>", methods=['GET', 'POST'])
def updatemainpage(id):        
    if request.method == "POST":
        id = request.form.get('id')
        label = request.form.get('label')
        text1 = request.form.get('text1')
        text2 = request.form.get('text2')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')  
        print(image_name)
        print(image_file)
        mediawithtext = tblmediaandtext.query.filter_by(id = id).first()
        if mediawithtext:
            mediawithtext.label = label
            mediawithtext.text1 = text1
            mediawithtext.text2 = text2
            if image_file:
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'mainpage/', filename)
                    mediawithtext.path = file_path
                if not os.path.exists(file_path):
                    image_file.save(file_path)
            elif image_name:
                if allowed_file(image_name):
                    filename = secure_filename(image_name)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'mainpage/', filename)
                    mediawithtext.path = file_path
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    mediawithtext = tblmediaandtext.query.filter_by(id = id).first()
    if mediawithtext is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
    
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'mainpage')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
        
    return render_template("/updatepage/updatemainpage.html", mediawithtext=mediawithtext, all_images=all_images)
    

@app.route("/updatecomputerfields/<int:id>", methods=['GET', 'POST'])
def updatecomputerfiles(id):
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'computerfields')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
        
    if request.method == "POST":
        id = request.form.get('id')
        label = request.form.get('label')
        videocard = request.form.get('videocard')
        mothercard = request.form.get('mothercard')
        freez = request.form.get('freez')
        mouse = request.form.get('mouse')
        headphone = request.form.get('headphone')
        processor = request.form.get('processor')
        ram = request.form.get('ram')
        screen = request.form.get('screen')
        image = request.files.get('image')
        keyboard = request.form.get('keyboard')

        computerfields = tblcomputerfiles.query.filter_by(id = id).first()
        if computerfields:
            computerfields.label = label
            computerfields.videocard = videocard
            computerfields.mothercard = mothercard
            computerfields.freez = freez
            computerfields.mouse = mouse
            computerfields.headphone = headphone
            computerfields.processor = processor
            computerfields.ram = ram
            computerfields.screen = screen
            computerfields.keyboard = keyboard
            if image:    
                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'computerfields/', filename)
                if os.path.exists(file_path):
                    computerfields.path = file_path
                else:
                    # Eğer dosya yoksa resmi kaydet
                    image.save(file_path)
                    computerfields.path = file_path  # Veritabanındaki path alanını güncelleyin
                    print("Dosya başarıyla kaydedildi.")

        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200


    computerfields = tblcomputerfiles.query.filter_by(id = id).first()
    if computerfields is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
    return render_template("/updatepage/updatecomputerfields.html", computerfields=computerfields)


if __name__ == '__main__':
    app.run(debug=True)
