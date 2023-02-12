from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from HBS import app, db
from HBS.models import *
from HBS.forms import LoginForm, RegisterForm, MaximForm, SettingsForm
from datetime import datetime
import json
import os




@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Giris islemleri
        if user and user.check_password(form.password.data):
            login_user(user, force=True)
            return redirect(url_for('index'))
        else:
            flash('Hata: Kullanıcı adı veya şifre yalnış !', 'danger')
            return redirect(url_for('login'))

       
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Merhaba {user.username} Üyelik işlemi gerçekleşmışır lütfen giriş yapın ', 'success')
        return redirect(url_for('login'))
    
    return render_template('signin.html', form=form)

@app.route('/')
@login_required
def index():
    maxim = Maxim.query
    return render_template('index.html', maxims=maxim)

@app.route('/maxim', methods=['GET','POST'])
def maxim():
    form = MaximForm()
    user = User.query.get(current_user.id)

    maxim_all = Maxim.query.all()
    if form.validate_on_submit():
        maxim = Maxim(
            maxim = form.maxim.data,
            category = form.select.data,
            author = form.author.data,
            show = form.show.data,
            user_id = current_user.id
        )
        current_date = datetime.utcnow().date()
        last_task_date = user.last_task_date.date()
        if current_date > last_task_date:
            user.task_today = 0

        if user and user.tasks_today < user.daily_limit:
            user.tasks_today += 1
            user.last_task_date = datetime.utcnow()
        if user.tasks_today >= user.daily_limit:
            flash('Bugunun limititini doldurdunuz lutfen yarin devam edin', 'warning')
            return redirect(url_for('maxim'))

        db.session.add(maxim)
        db.session.commit()
        flash(maxim.maxim,'success')
        return redirect(url_for('maxim'))

    return render_template('maxim.html', form=form, maxim=maxim_all, user=user)

@app.route('/delete/maxim/<int:maxim_id>')
@login_required
def delete_maxim(maxim_id):
    maxim = Maxim.query.get_or_404(maxim_id)
    db.session.delete(maxim)
    db.session.commit()
    flash('Veritabanında kaldırıldı', 'success')
    return redirect(url_for('database'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    config = get_config()
    form = SettingsForm()
    if form.validate_on_submit():
        config['MAXIM_NUMBER'] = form.maxim_number.data

        update_config(config)
        flash('Ayarlar başarıyla kaydedildi !')

        return redirect(url_for('settings'))

    if request.method == 'GET':
        form.maxim_number.data = config['MAXIM_NUMBER']
    return render_template('settings.html', form=form)


@app.route('/database')
@login_required
def database():
    maxim = Maxim.query
    all_maxim = Maxim.query.order_by(Maxim.id.desc()).all()
    return render_template('database.html', maxims=maxim, all_maxim=all_maxim)

@app.route('/maxims/my')
def my_maxims():
    user = User.query.get(current_user.id)
    print(user.maxims)

    return render_template('my_maxims.html', user_maxim=user.maxims)

@app.route('/clear')
def clear_data():
    maxims = Maxim.query.all()
    for x in maxims:
        db.session.delete(x)
    db.session.commit()
    return redirect(url_for('index'))
# Json Configs
def get_config():
    json_path = os.path.join(app.root_path, 'config.json')
    with open(json_path , "r+") as file:
        json_read = json.load(file)
    return json_read 


def update_config(config):
    json_path = os.path.join(app.root_path, 'config.json')
    with open(json_path , "w") as file:
        json_read = json.dump(config, file)
    return True 