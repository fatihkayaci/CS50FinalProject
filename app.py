import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.templating import render_template
from models import db, tblusers, tblfoods, tblcomputerfiles, tblgames, tblsteams, tblservice, tblsettings, tblarsive, tblsteamgame, tbltext, tblmedia, tblmediaandtext
from flask_migrate import Migrate, migrate
from werkzeug.utils import secure_filename
from helpers import login_required
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


# sessions 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
migrate = Migrate(app, db)

db.init_app(app)
@app.route("/")
def indexp():
    return render_template("users/indexp.html")

@app.route("/cafeattribute")
def cafeattribute():
    # burası düzeltilecek veritabanı unutma
    computerfields= tblcomputerfiles.query.all()
    foods = tblfoods.query.all()
    games = tblgames.query.all()
    steams = tblsteams.query.all()
    services = tblservice.query.all() 
    query_result = (
    db.session.query(
        tblsteamgame.id,
        tblsteams.steamname,
        tblgames.gamename,
        tblgames.iconpath
    )
    .join(tblsteams, tblsteamgame.steamid == tblsteams.id)
    .join(tblgames, tblsteamgame.gameid == tblgames.id)
    .order_by(tblsteams.steamname)
    .all()
    )
    steamgames = [
        {
            "id": steamgame_id,  # tblsteamgame.steamid
            "steamname": steamname,  # tblsteams.steamname
            "gamename": gamename,  # tblgames.gamename
            "imagepath": iconpath  # tblgames.iconpath
        }
        for steamgame_id, steamname, gamename, iconpath in query_result
    ]
    return render_template("users/cafeattribute.html", computerfields=computerfields, foods=foods, games=games, steams=steams, steamgames=steamgames, services=services)

@app.route('/arsiv')
def arsiv():
    arsives = tblarsive.query.all()
    return render_template("users/arsiv.html", arsives=arsives)
# admin paneli
# ------------------------------------------------------General Methods Starts------------------------------------------------------
def get_all_images(filename):
    all_images = []
    target_folder = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(target_folder):
        all_images = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    return all_images
def add_file(file, image_file, image_name):
    file_path = ''
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file, filename)
        if not os.path.exists(file_path):
            image_file.save(file_path)
    elif image_name and allowed_file(image_name):
        filename = secure_filename(image_name)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file, filename)
    return file_path
# ------------------------------------------------------General Methods Finals------------------------------------------------------
# ------------------------------------------------------Welcome Page Start------------------------------------------------------
@app.route("/welcome")
def welcome():
    return render_template("welcome.html")
# ------------------------------------------------------Welcome Page Finish------------------------------------------------------
# ------------------------------------------------------login start------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            flash("Kullanıcı Adı Giriniz!")
            return render_template("admin/login.html")

        if not password:
            flash("Şifrenizi Giriniz!")
            return render_template("admin/login.html")
        
        user = tblusers.query.filter_by(user_name = username).first()
        if user and user.password == password:
            session["user_id"] = user.id
            query_result = (
                db.session.query(
                    tblmediaandtext.id,
                    tblmediaandtext.page_name,
                    tblmediaandtext.title,
                    tblmediaandtext.label,
                    tbltext.text_message,
                    tblmedia.image_path
                )
                .join(tbltext, tblmediaandtext.textid == tbltext.id)
                .join(tblmedia, tblmediaandtext.mediaid == tblmedia.id)
                .all()
            )

            mediawithtext = [
                {
                    "id": id,
                    "page_name": page_name,
                    "title": title,
                    "label": label,
                    "text_message": text_message,
                    "image_path": image_path
                }
                for id, page_name, title, label, text_message, image_path in query_result
            ]
            return render_template("admin/welcome.html", mediawithtext=mediawithtext)
        else:
            return render_template("admin/login.html")
        
    return render_template("admin/login.html")
# ------------------------------------------------------login end------------------------------------------------------
# ------------------------------------------------------Mainpage process start------------------------------------------------------
@app.route("/indexa", methods=["GET", "POST"])
@login_required
def indexa():              
    query_result = (
        db.session.query(
            tblmediaandtext.id,
            tblmediaandtext.page_name,
            tblmediaandtext.title,
            tblmediaandtext.label,
            tbltext.text_message,
            tblmedia.image_path
        )
        .join(tbltext, tblmediaandtext.textid == tbltext.id)
        .join(tblmedia, tblmediaandtext.mediaid == tblmedia.id)
        .all()
    )

    mediawithtext = [
        {
            "id": id,
            "page_name": page_name,
            "title": title,
            "label": label,
            "text_message": text_message,
            "image_path": image_path
        }
        for id, page_name, title, label, text_message, image_path in query_result
    ]
    all_images = get_all_images("generalimage")
    return render_template("admin/indexa.html", mediawithtext=mediawithtext, all_images=all_images)


@app.route("/updatetextandmedia/<int:id>", methods=['GET', 'POST'])
@login_required
def updatetextandmedia(id):
    mediawithtext = (
        db.session.query(
            tblmediaandtext.id,
            tblmediaandtext.textid,
            tblmediaandtext.mediaid,
            tblmediaandtext.page_name,
            tblmediaandtext.title,
            tblmediaandtext.label,
            tbltext.text_message,
            tblmedia.image_path,
            tbltext.id.label('text_id'),
            tblmedia.id.label('media_id')
        )
        .join(tbltext, tblmediaandtext.textid == tbltext.id)
        .join(tblmedia, tblmediaandtext.mediaid == tblmedia.id)
        .filter(tblmediaandtext.id == id)
        .first()
    )
    if mediawithtext:
        text = tbltext.query.filter(tblmediaandtext.textid == id).first()
        media = tblmedia.query.filter(tblmediaandtext.mediaid == id).first()
        tbltextandmedia = tblmediaandtext.query.filter(tblmediaandtext.id == id).first()

    if request.method == "POST":
        label = request.form.get('label')
        text_message = request.form.get('text')
        image_file = request.files.get('image')
        image_name = request.form.get('image_name')
        file_path = add_file('generalimage', image_file, image_name)
        if file_path:
            media.image_path = file_path
        text.text_message=text_message
        tbltextandmedia.label = label
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    all_images = get_all_images("generalimage")
    return render_template("admin/updatepage/updatetextandmedia.html", mediawithtext=mediawithtext, all_images=all_images)

# ------------------------------------------------------Mainpage process end------------------------------------------------------
# ------------------------------------------------------computer fields process start------------------------------------------------------

@app.route("/computerfields")
@login_required
def computerfields():
    computers = tblcomputerfiles.query.all()
    return render_template("admin/computerfields.html", computers = computers)

@app.route("/updatecomputerfields/<int:id>", methods=['GET', 'POST'])
@login_required
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
            file_path = add_file('computerfields', image_file, image_name)
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
            computerfields.path = file_path
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    computerfields = tblcomputerfiles.query.filter_by(id = id).first()
    if computerfields is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    all_images = get_all_images("computerfields")
    return render_template("/admin/updatepage/updatecomputerfields.html", computerfields=computerfields, all_images=all_images)
# ------------------------------------------------------computer fields process end------------------------------------------------------
# ------------------------------------------------------foods process start------------------------------------------------------
# foods process
@app.route("/foodsadd", methods=['GET', 'POST'])
@login_required
def foodsadd():
    if request.method == "POST":
        foodname = request.form.get('foodName')
        foodtext = request.form.get('foodText')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        if not foodname and not foodtext and not (image_name or image_file):
            return jsonify({"success": False, "message": "Hata oluştu: Tüm alanlar boş bırakılamaz. Lütfen doldurunuz."})
        
        file_path = add_file("foods", image_file, image_name)
        newfood = tblfoods(path = file_path, label=foodname, text=foodtext)
        db.session.add(newfood)

        db.session.commit()        
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    all_images = get_all_images("foods")
    foods = tblfoods.query.all()
    return render_template("/admin/foodsadd.html", foods=foods, all_images=all_images)

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
@login_required
def updatefood(id):
    if request.method == "POST":
        id = request.form.get('id')
        label = request.form.get("label")
        text = request.form.get("text")
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        foods = tblfoods.query.filter_by(id = id).first()
        if foods:
            file_path = add_file('foods', image_file, image_name)
            foods.label = label
            foods.text = text
            foods.path = file_path
        
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    foods = tblfoods.query.filter_by(id = id).first()
    if foods is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")
     

    all_images = get_all_images("foods")
    return render_template("/admin/updatepage/updatefood.html", foods=foods, all_images=all_images)

# ------------------------------------------------------foods process end------------------------------------------------------

# ------------------------------------------------------ games process start ------------------------------------------------------
@app.route("/gamesadd", methods=['GET', 'POST'])
@login_required
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
        
        image_path = add_file('games/images', image_file, image_name)
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
    
    all_images = get_all_images("games/images")
    all_icon = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'games/icon')
    if os.path.exists(target_folder):
        all_icon = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    games = tblgames.query.all()
    return render_template("/admin/gamesadd.html", games=games, all_icon=all_icon, all_images=all_images)

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
@login_required
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
            file_path = add_file('games/images', image_file, image_name)
            games.gamename = gamename
            games.text = gametext
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
    
    all_images = get_all_images("games/images")
        
    all_icon = []
    target_folder = os.path.join(UPLOAD_FOLDER, 'games/icon')
    if os.path.exists(target_folder):
        all_icon = [file for file in os.listdir(target_folder) 
                    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))]
    
    games = tblgames.query.filter_by(id = id).first()
    if games is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    return render_template("/admin/updatepage/updategame.html", games=games, all_images=all_images, all_icon=all_icon)
# ------------------------------------------------------ games process end ------------------------------------------------------

# ------------------------------------------------------ steam process start ------------------------------------------------------
@app.route("/steamsadd", methods=['GET', 'POST'])
@login_required
def steamsadd():
    if request.method == "POST":
        steamname = request.form.get('steamName')
        steamid = request.form.get('steamid')
        gameid = request.form.get('gameid')
        
        if not steamname and not steamid and not gameid:
            return jsonify({"success": False, "message": "Hata oluştu: Tüm alanlar boş bırakılamaz. Lütfen doldurunuz."})
        
        if steamname:
            newsteam = tblsteams(steamname=steamname)
            db.session.add(newsteam)
        if steamid and gameid:
            newsteamgame = tblsteamgame(steamid=steamid, gameid=gameid)
            db.session.add(newsteamgame)
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    

    steams = tblsteams.query.all()
    games = tblgames.query.all()
    query_result = (
        db.session.query(tblsteamgame, tblsteams, tblgames)
        .join(tblsteams, tblsteamgame.steamid == tblsteams.id)
        .join(tblgames, tblsteamgame.gameid == tblgames.id)
        .order_by(tblsteams.steamname)
        .all()
    )
    steamgame = [
        {
            "id": steamgame.id,  # tblsteamgame.steamid
            "steamname": steam.steamname,  # tblsteams.steamname
            "gamename": game.gamename  # tblgames.gamename
        }
        for steamgame, steam, game in query_result
    ]
    if steams is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    return render_template("/admin/steamsadd.html", steams=steams, games=games, steamgame=steamgame)


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

@app.route("/deletesteamgame", methods=['GET', 'POST'])
def deletesteamgame():
    if request.method == "POST":
        steamgameid = request.form.get('steamgameid')
        if not steamgameid:
            return {'status': 'error', 'message': 'Game ID is missing'}, 400
        delete = tblsteamgame.query.get(steamgameid)
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return 'succesfull'
    return 'str'

@app.route("/updatesteam/<int:id>", methods=['GET', 'POST'])
@login_required
def updatesteam(id):
    if request.method == "POST":
        id = request.form.get('id')
        steamname = request.form.get("steamname")
        gamename = request.form.get("gamename")
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        steam = tblsteams.query.filter_by(id = id).first()
        if steam:
            file_path = add_file('steam', image_file, image_name)
            steam.gamename = gamename
            steam.steamname = steamname
            steam.iconpath = file_path
        
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    steam = tblsteams.query.filter_by(id = id).first()

    if steam is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    all_images = get_all_images("steam")
    return render_template("/admin/updatepage/updatesteam.html", steam=steam, all_images=all_images)
# ------------------------------------------------------ steam process end ------------------------------------------------------

# ------------------------------------------------------ service process start ------------------------------------------------------
@app.route("/service", methods=['GET', 'POST'])
@login_required
def service():
    if request.method == "POST":
        servicename = request.form.get('servicename')
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        print(servicename)
        print(image_file)
        print(image_name)
        if not servicename and not (image_name or image_file):
            return jsonify({"success": False, "message": "Hata oluştu: Tüm alanlar boş bırakılamaz. Lütfen doldurunuz."})
        
        file_path = add_file("service", image_file, image_name)
        newservice = tblservice(imagepath = file_path, name=servicename)
        db.session.add(newservice)
        db.session.commit()        
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    
    all_images = get_all_images("service")    
    services = tblservice.query.all()
    return render_template("/admin/service.html", services=services, all_images=all_images)

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
@login_required
def updateservice(id):
    if request.method == "POST":
        id = request.form.get('id')
        servicename = request.form.get("servicename")
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        service = tblservice.query.filter_by(id = id).first()
        if service:
            file_path = add_file('service', image_file, image_name)
            service.name = servicename
            service.imagepath = file_path
        
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200

    service = tblservice.query.filter_by(id = id).first()

    if service is None:
        print("böyle bir veri yok: not bunlar için bir şey yap fatih 404 için")

    all_images = get_all_images("service")    
        
    return render_template("/admin/updatepage/updateservice.html", service=service, all_images=all_images)
# ------------------------------------------------------ service process end ------------------------------------------------------
# ------------------------------------------------------ arsive process start ------------------------------------------------------
@app.route("/arsive", methods=['GET', 'POST'])
@login_required
def arsive():
    if request.method == "POST":
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        file_path = add_file('arsive', image_file, image_name)
        newarsive = tblarsive(imagepath = file_path)
        db.session.add(newarsive)
        db.session.commit()        
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    
    all_images = get_all_images("arsive")
    arsives = tblarsive.query.all()
    return render_template("/admin/arsive.html", arsives=arsives, all_images=all_images)

@app.route("/deletearsive", methods=['GET', 'POST'])
def deletearsive():
    if request.method == "POST":
        arsiveid = request.form.get('arsiveid')
        if not arsiveid:  # foodid boşsa hata dön
            return {'status': 'error', 'message': 'Game ID is missing'}, 400
        delete = tblarsive.query.get(arsiveid)
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return 'succesfull'
    return 'str'
# ------------------------------------------------------ arsive process end ------------------------------------------------------
# ------------------------------------------------------ settings process start ------------------------------------------------------
@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    all_images = get_all_images("generalsettings")
    setting = tblsettings.query.first()
    user = tblusers.query.filter_by(id = session['user_id']).first()
    return render_template("/admin/settings.html", all_images=all_images, setting=setting, user=user)

@app.route("/updatesettings", methods=['GET', 'POST'])
@login_required
def updatesettings():
    if request.method == "POST":   
        id = session['user_id']
        username = request.form.get("username")
        password = request.form.get("password")
        passwordagain = request.form.get("passwordagain")

        companyname = request.form.get("companyname")
        image_file = request.files.get('image_file')
        image_name = request.form.get('image_name')
        phonenumber = request.form.get("phonenumber")
        email = request.form.get("mail")
        adress = request.form.get("address")

        if password != passwordagain: return jsonify({"message": "Şifreler Aynı Değil Lütfen Tekrar Kontrol Ediniz.", "status": "error"}), 400
        if not companyname and not (image_file or image_name) and not phonenumber and not email and not adress and not username:return jsonify({"message": "Bütün alanlar boş kaldı lütfen doldurunuz", "status": "error"}), 400
        if not id: return jsonify({"message": "Kullanıcıyı Kontrol ediniz.", "status": "error"}), 400
        
        user = tblusers.query.filter_by(id = id).first()
        if user:
            user.user_name = username
            if password == passwordagain:user.password = password

        settings = tblsettings.query.first()
        if settings:
            file_path = add_file('generalsettings', image_file, image_name)
            settings.name = companyname
            settings.number = phonenumber
            settings.mail = email
            settings.adress = adress
            settings.logopath = file_path
        
        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    return 'str'
# ------------------------------------------------------ settings process end ------------------------------------------------------
# ------------------------------------------------------ users process start ------------------------------------------------------
@app.route("/useradd", methods=['GET', 'POST'])
@login_required
def useradd():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return jsonify({"message": "Kullanıcı Kaydedilemedi: Eksik Bilgi.", "status": "error"}), 400
        
        existing_user = tblusers.query.filter_by(user_name=username).first()
        if existing_user:
            return jsonify({"message": "Kullanıcı Zaten Mevcut.", "status": "error"}), 400
        
        # Yeni kullanıcı oluşturma
        new_user = tblusers(user_name=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Kullanıcı Başarıyla Kaydedildi.", "status": "success"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Hata: {str(e)}", "status": "error"}), 500
    users = tblusers.query.filter(tblusers.id != session['user_id']).all()
    return render_template("admin/useradd.html", users=users)

@app.route("/deleteuser", methods=['GET', 'POST'])
def deleteuser():
    if request.method == "POST":
        userid = request.form.get('userid')
        if not userid:
            return {'status': 'error', 'message': 'Game ID is missing'}, 400
        delete = tblusers.query.get(userid)
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return 'succesfull'
    return 'str'

@app.route("/updateuser/<int:id>", methods=['GET', 'POST'])
@login_required
def updateuser(id):
    if request.method == "POST":   
        id = request.form.get("id")
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password :return jsonify({"message": "Bütün alanlar boş kaldı lütfen doldurunuz", "status": "error"}), 400
        if not id: return jsonify({"message": "Kullanıcıyı Kontrol ediniz.", "status": "error"}), 400
        
        user = tblusers.query.filter_by(id = id).first()
        if user:
            user.user_name = username
            user.password = password

        db.session.commit()
        return jsonify({"message": "Güncelleme başarılı", "status": "success"}), 200
    user = tblusers.query.filter_by(id = id).first()
    return render_template("/admin/updatepage/updateuser.html", user=user)
# ------------------------------------------------------ logut process start ------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
# ------------------------------------------------------ logut process end ------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
