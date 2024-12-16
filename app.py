import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.templating import render_template
from models import db, users_tbl, text_tbl, media_tbl
from flask_migrate import Migrate, migrate
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)

# bakılacak
UPLOAD_FOLDER = 'static/img/mainpage/'
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
    text = text_tbl.query.all()
    return render_template("indexp.html", text = text)

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
        data = request.form 
        # Veriyi işle
        for key, value in data.items():
            text_entry = text_tbl.query.filter_by(id_name=key).first()  # id_name ile eşleşen kaydı bul
            if text_entry:
                text_entry.text = value  # text sütununu güncelle
            else:
                flash(f"ID {key} için veri bulunamadı.")
        
        db.session.commit()
        flash("Veriler başarıyla güncellendi!")
    
    articles = text_tbl.query.all()
    media = media_tbl.query.order_by(media_tbl.order_index).all()

    return render_template("indexa.html", articles=articles, media=media)

@app.route('/uploadmedia', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"message": "Dosya bulunamadı"}), 400
    
    file = request.files['image']
    data = request.form
    order = data["order"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Dosya adını güvenli hale getir
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Dosya yolu
        try:
            # Dosyayı belirtilen klasöre kaydet
            file.save(file_path)
            
            existing_media = media_tbl.query.filter_by(order_index=order).first()
            existing_media.active = False
            # Veritabanına kaydet
            new_media = media_tbl(group_name="hizmetler", file_name=filename, path=file_path, active=True, order_index=data["order"])
            db.session.add(new_media)
            db.session.commit()
            return jsonify({
                "message": f"{filename} başarıyla yüklendi ve veritabanına kaydedildi.",
                "imageName": filename
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Bir hata oluştu: {str(e)}", "error": repr(e)}), 500

    else:
        return jsonify({"message": "Geçersiz dosya formatı"}), 400


if __name__ == '__main__':
    app.run(debug=True)
