from flask import Flask, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from os import path
from flask_babel import Babel
from flask_admin.contrib.sqla import ModelView


# Uygulama ve Veritabanı Yapılandırması
app = Flask(__name__)
babel = Babel(app)
basedir = path.abspath(path.dirname(__file__))
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'site.db')

# Uygulama Eklentileri
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
from app.my_admin.routes import MyAdminIndexView
admin = Admin(app, name='Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3')

# Model ve View İçe Aktarmaları
from app.models import User,Course,Teacher,Student,Newsletter,Contact
from app.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app import views, models
from app import app, db

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Course,db.session))
admin.add_view(ModelView(Teacher,db.session))
admin.add_view(ModelView(Student,db.session))
admin.add_view(ModelView(Newsletter,db.session))
admin.add_view(ModelView(Contact,db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/footer', methods=['POST'])
def add_email_to_newsletter():
    if request.method == 'POST':
        email = request.form['email']
        new_email = Newsletter(email=email)
        try:
            db.session.add(new_email)
            db.session.commit()
            flash('Email added to the newsletter successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error adding email to the newsletter!', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
    
        new_contact = Contact(name=name, email=email, subject=subject, message=message)

        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Message added successfully!', 'success')
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('Error adding the message!', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('contact'))
