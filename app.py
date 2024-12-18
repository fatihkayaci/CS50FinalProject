import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.templating import render_template
from models import db, tblusers, tbltext, tblmedia, tblfoods
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
    text = tbltext.query.all()
    media = tblmedia.query.all()
    return render_template("indexp.html", text = text, media = media)

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
        
        user = users_tbl.query.filter_by(user_name = username).first()
        if user and user.password == password:
            return render_template("/indexa.html", user = user)
        else:
            return render_template("/login.html")
        
        # profiles = users.query.all()
    return render_template("/login.html")



@app.route("/indexa", methods=["GET", "POST"])
def indexa():
    if request.method == "POST":
        try:
            data = request.get_json()  
            updated_records = 0  
            id_name = data.get("id_name")
            value = data.get("value")
            print(data)
            for key, value in data.items():
                text_entry = tbltext.query.filter_by(id_name=id_name).first()
                if text_entry:  
                    text_entry.text = value  # Güncelleme
                    updated_records += 1

            db.session.commit()  # Tek seferde commit
            return jsonify({"message": f"{updated_records} kayıt başarıyla güncellendi!"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Bir hata oluştu: {str(e)}"}), 500

    # GET isteği için veri çekme
    articles = tbltext.query.filter_by(page_name="mainpage").all()
    media = tblmedia.query.filter_by(page_name="mainpage").order_by(tblmedia.order_index).all()
    counter = 0
    return render_template("indexa.html", articles=articles, media=media, counter=counter)


@app.route('/uploadmedia', methods=['POST'])
def upload_image():
    if len(request.form) == 0:
        return jsonify({"message": "Dosya bulunamadı"}), 400
    
    data = request.form
    order = data["order"]
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Dosya adını güvenli hale getir
            if data['photopath'] == "mainpage":
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'mainpage/', filename)  # Dosya yolu
            elif data['photopath'] == "computerfiles":
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],'computerfiles/', filename)  # Dosya yolu

            try:
                file.save(file_path)
                existing_media = tblmedia.query.filter_by(order_index=order).all()
                for ex in existing_media:
                    ex.active = False

                existing_media = tblmedia.query.filter_by(file_name = filename).all()
                if len(existing_media) < 1:
                    new_media = tblmedia(group_name="hizmetler", file_name=filename, path=file_path, active=True, order_index=data["order"])
                    db.session.add(new_media)
                else:
                    for ex in existing_media:
                        ex.order_index = order
                        ex.active = True
                return 'str'
            
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": f"Bir hata oluştu: {str(e)}", "error": repr(e)}), 500
        else:
            return jsonify({"message": "Geçersiz dosya formatı"}), 400
    elif data and allowed_file(data["imageName"]):
        existing_media = tblmedia.query.filter_by(order_index=order).all()
        for ex in existing_media:
            ex.active = False
        existing_media = tblmedia.query.filter_by(file_name = data["imageName"]).all()
        for ex in existing_media:
            ex.order_index = order
            ex.active = True            
    db.session.commit()


@app.route("/computerfiles")
def cafeattributea():
    articles = tbltext.query.filter_by(page_name = "cafeattributepage").all()
    media = tblmedia.query.filter_by(page_name="cafeattributepage").order_by(tblmedia.order_index).all()

    return render_template("/computerfiles.html", articles = articles, media = media)


# deneme
@app.route("/foodsadd")
def tblfoodsadd():
    food = tblfoods.query.all()
    return render_template("/tblfoodsadd.html", tblfoods = food)

if __name__ == '__main__':
    app.run(debug=True)
