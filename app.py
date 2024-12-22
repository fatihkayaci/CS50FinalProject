import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.templating import render_template
from models import db, tblusers, tblmediaandtext, tblfoods, tblcomputerfiles, tblgames, tblsteams, tblservice
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

@app.route("/updatemainpage/<int:id>", methods=['GET', 'POST'])
def updatemainpage(id):        
    if request.method == "POST":
        id = request.form.get('id')
        label = request.form.get('label')
        text1 = request.form.get('text1')
        text2 = request.form.get('text2')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
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
    
# computer fields process
@app.route("/computerfields")
def computerfields():
    computers = tblcomputerfiles.query.all()
    return render_template("/computerfields.html", computers = computers)

@app.route("/updatecomputerfields/<int:id>", methods=['GET', 'POST'])
def updatecomputerfields(id):        
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
        keyboard = request.form.get('keyboard')
        image_file = request.files.get('image')
        image_name = request.form.get('image_name')
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
            if image_file:
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'computerfields/', filename)
                    computerfields.path = file_path
                if not os.path.exists(file_path):
                    image_file.save(file_path)
            elif image_name:
                if allowed_file(image_name):
                    filename = secure_filename(image_name)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'computerfields/', filename)
                    computerfields.path = file_path
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    computerfields = tblcomputerfiles.query.filter_by(id = id).first()
    if computerfields is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'computerfields')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    return render_template("/updatepage/updatecomputerfields.html", computerfields=computerfields, all_images=all_images)

# ------------------------------------------------------foods process start------------------------------------------------------
# foods process
@app.route("/foodsadd", methods=['GET', 'POST'])
def foodsadd():
    if request.method == "POST":
        foodname = request.form.get('foodName')
        foodtext = request.form.get('foodText')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        if not foodname and not foodtext and not (image_name or image_file):
            return jsonify({"success": False, "message": "Hata oluştu: Tüm alanlar boş bırakılamaz. Lütfen doldurunuz."})
        file_path=''
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],'foods/', filename)
            if not os.path.exists(file_path):
                image_file.save(file_path)
        elif image_name and allowed_file(image_name):
            filename = secure_filename(image_name)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],'foods/', filename)
        newfood = tblfoods(path = file_path, label=foodname, text=foodtext)
        db.session.add(newfood)

        db.session.commit()        
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'foods')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    foods = tblfoods.query.all()
    return render_template("/foodsadd.html", foods=foods, all_images=all_images)

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
        id = request.form.get('id')
        label = request.form.get("label")
        text = request.form.get("text")
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        foods = tblfoods.query.filter_by(id = id).first()
        if foods:
            foods.label = label
            foods.text = text
            if image_file:    
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'foods/', filename)
                    foods.path = file_path
                if not os.path.exists(file_path):
                    image_file.save(file_path)
            elif image_name:
                if allowed_file(image_name):
                    filename = secure_filename(image_name)  # Dosya adını güvenli hale getir
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'],'foods/', filename)
                    foods.path = file_path
        
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    foods = tblfoods.query.filter_by(id = id).first()
    if foods is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
        
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'foods')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    return render_template("/updatepage/updatefood.html", foods=foods, all_images=all_images)

# ------------------------------------------------------foods process end------------------------------------------------------

# ------------------------------------------------------ games process start ------------------------------------------------------
@app.route("/gamesadd", methods=['GET', 'POST'])
def gamesadd():
    if request.method == "POST":
        gamename = request.form.get('gamename')
        gametext = request.form.get('gametext')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        icon_file = request.files.get('icon_files')
        icon_name = request.form.get('icon_name')
        if not gamename and not gametext and not (image_file or image_name) and not (icon_file or icon_name):
            return jsonify({"success": False, "message": "Hata oluştu: Tüm alanlar boş bırakılamaz. Lütfen doldurunuz."})
        image_path=''
        icon_path=''
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/images/', filename)
            if not os.path.exists(image_path):
                image_file.save(image_path)
        elif image_name and allowed_file(image_name):
            filename = secure_filename(image_name)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/images/', filename)
        
        if icon_file and allowed_file(icon_file.filename):
            filename = secure_filename(icon_file.filename)
            icon_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/icon/', filename)
            if not os.path.exists(icon_path):
                image_file.save(icon_path)
        elif icon_name and allowed_file(icon_name):
            filename = secure_filename(icon_name)
            icon_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/icon/', filename)

        newgame = tblgames(photopath = image_path, iconpath = icon_path, gamename=gamename, text=gametext)
        db.session.add(newgame)
        db.session.commit()        
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'games/images')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
        
    all_icon = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'games/icon')
    if os.path.exists(target_folder):
        all_icon = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    games = tblgames.query.all()
    return render_template("/gamesadd.html", games=games, all_icon=all_icon, all_images=all_images)

@app.route("/deletegame", methods=['GET', 'POST'])
def deletegame():
    if request.method == "POST":
        gameid = request.form.get('gameid')
        if not gameid:  # foodid boşsa hata dön
            return {'status': 'error', 'message': 'Game ID is missing'}, 400
        print(gameid)
        game_to_delete = tblgames.query.get(gameid)
        if game_to_delete:
            db.session.delete(game_to_delete)
            db.session.commit()
        return 'succesfull'
    return 'str'

@app.route("/updategame/<int:id>", methods=['GET', 'POST'])
def updategame(id):
    if request.method == "POST":
        id = request.form.get('id')
        gamename = request.form.get('gamename')
        gametext = request.form.get('gametext')
        image_name = request.form.get('image_name')
        image_file = request.files.get('image_file')
        icon_name = request.form.get('icon_name')
        icon_file = request.files.get('icon_file')
        games = tblgames.query.filter_by(id = id).first()
        if games:
            games.gamename = gamename
            games.text = gametext
            if image_name and allowed_file(image_name):
                filename = secure_filename(image_name)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/images/', filename)
                games.photopath = file_path
                if not os.path.exists(file_path):
                    image_name.save(file_path)
            elif image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/images/', filename)
                games.photopath = file_path
                if not os.path.exists(file_path):
                    image_name.save(file_path)

            if icon_name and allowed_file(icon_name):
                filename = secure_filename(icon_name)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/icon/', filename)
                games.iconpath = file_path
                if not os.path.exists(file_path):
                    icon_name.save(file_path)
            elif icon_file and allowed_file(icon_file.filename):
                filename = secure_filename(icon_file.filename)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'games/icon/', filename)
                games.iconpath = file_path
                if not os.path.exists(file_path):
                    image_name.save(file_path)

        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'games/images')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
        
    all_icon = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'games/icon')
    if os.path.exists(target_folder):
        all_icon = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    
    games = tblgames.query.filter_by(id = id).first()
    if games is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    return render_template("/updatepage/updategame.html", games=games, all_images=all_images, all_icon=all_icon)
# ------------------------------------------------------ games process end ------------------------------------------------------

# ------------------------------------------------------ steam process start ------------------------------------------------------
@app.route("/steamsadd", methods=['GET', 'POST'])
def steamsadd():
    if request.method == "POST":
        steamname = request.form.get('steamName')
        gamename = request.form.get('gameName')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        if not steamname and not gamename and not (image_name or image_file):
            return jsonify({"success": False, "message": "Hata oluştu: Tüm alanlar boş bırakılamaz. Lütfen doldurunuz."})
        
        file_path=''
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],'steam/', filename)
            if not os.path.exists(file_path):
                image_file.save(file_path)
        elif image_name and allowed_file(image_name):
            filename = secure_filename(image_name)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],'steam/', filename)
        newsteam = tblsteams(iconpath = file_path, gamename=gamename, steamname=steamname)
        db.session.add(newsteam)
        db.session.commit()        
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'steam')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    steams = tblsteams.query.all()
    if steams is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    return render_template("/steamsadd.html", steams=steams, all_images=all_images)

@app.route("/deletesteam", methods=['GET', 'POST'])
def deletesteam():
    if request.method == "POST":
        steamid = request.form.get('steamid')
        if not steamid:  # foodid boşsa hata dön
            return {'status': 'error', 'message': 'Game ID is missing'}, 400
        delete = tblsteams.query.get(steamid)
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return 'succesfull'
    return 'str'

@app.route("/updatesteam/<int:id>", methods=['GET', 'POST'])
def updatesteam(id):
    if request.method == "POST":
        id = request.form.get('id')
        steamname = request.form.get("steamname")
        gamename = request.form.get("gamename")
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        steam = tblsteams.query.filter_by(id = id).first()
        if steam:
            #iconpath
            steam.gamename = gamename
            steam.steamname = steamname
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'steam/', filename)
                steam.iconpath = file_path
                if not os.path.exists(file_path):
                    image_file.save(file_path)
            elif image_name and allowed_file(image_name):
                filename = secure_filename(image_name)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'steam/', filename)
                steam.iconpath = file_path
        
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    steam = tblsteams.query.filter_by(id = id).first()

    if steam is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
        
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'steam')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    return render_template("/updatepage/updatesteam.html", steam=steam, all_images=all_images)
# ------------------------------------------------------ steam process end ------------------------------------------------------

# ------------------------------------------------------ service process start ------------------------------------------------------
@app.route("/service", methods=['GET', 'POST'])
def service():
    if request.method == "POST":
        servicename = request.form.get('servicename')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        
        if not servicename and not (image_name or image_file):
            return jsonify({"success": False, "message": "Hata oluştu: Tüm alanlar boş bırakılamaz. Lütfen doldurunuz."})
        
        file_path=''
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],'service/', filename)
            if not os.path.exists(file_path):
                image_file.save(file_path)
        elif image_name and allowed_file(image_name):
            filename = secure_filename(image_name)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],'service/', filename)
        newservice = tblservice(imagepath = file_path, name=servicename)
        db.session.add(newservice)
        db.session.commit()        
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'service')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    
    services = tblservice.query.all()
    return render_template("/service.html", services=services, all_images=all_images)

@app.route("/deleteservice", methods=['GET', 'POST'])
def deleteservice():
    if request.method == "POST":
        serviceid = request.form.get('serviceid')
        if not serviceid:  # foodid boşsa hata dön
            return {'status': 'error', 'message': 'Game ID is missing'}, 400
        delete = tblservice.query.get(serviceid)
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return 'succesfull'
    return 'str'

@app.route("/updateservice/<int:id>", methods=['GET', 'POST'])
def updateservice(id):
    if request.method == "POST":
        id = request.form.get('id')
        servicename = request.form.get("servicename")
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        service = tblservice.query.filter_by(id = id).first()
        if service:
            service.name = servicename
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'service/', filename)
                service.imagepath = file_path
                if not os.path.exists(file_path):
                    image_file.save(file_path)
            elif image_name and allowed_file(image_name):
                filename = secure_filename(image_name)  # Dosya adını güvenli hale getir
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'service/', filename)
                service.imagepath = file_path
        
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    service = tblservice.query.filter_by(id = id).first()

    if service is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
        
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'service')
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
        
    return render_template("/updatepage/updateservice.html", service=service, all_images=all_images)
# ------------------------------------------------------ service process end ------------------------------------------------------



if __name__ == '__main__':
    app.run(debug=True)
