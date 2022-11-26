import logging
from datetime import datetime, timedelta
import os
import random


from flask import Flask, render_template, request, flash, abort, redirect, url_for, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import and_, func, literal_column
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

import config
import version
from UserLogin import UserLogin
from sheme_bd import engine, Events, Chanels, MediaContens, TypeMedia, Users, Tags, MediaTags

logging.basicConfig(filename='log.log', format='%(filename)s: %(message)s')

# конфигурация
DEBUG = True
SECRET_KEY = config.SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа"
login_manager.login_message_category = "success"
ERROR_WRITE = "Ошибка формата записи"


class versionGet:
    """класс получает данные версии и передает в базовый шаблон"""

    def __init__(self):
        self.version_web = version.V_STRING
        try:
            with open(f"{config.BASE_DIR}/version", 'r', encoding="utf-8") as file_ver:
                version_spgt = file_ver.read()
        except:
            version_spgt = "????"
        self.version_spgt = version_spgt


# make function available inside jinja template
app.jinja_env.globals.update(versionGet=versionGet())


s = None
@app.before_request
def before_request():
    """Установка соеденения с базой данныйх"""
    global s
    session = sessionmaker(bind=engine)
    s = session()

@app.teardown_appcontext
def close_db(error):
    s.close()



@login_manager.user_loader
def load_user(user_id):
    a = UserLogin().fromDB(user_id)
    return a


def set_password(password):
    password_hash = generate_password_hash(password)
    return password_hash


def check_password(password, password_check):
    # password_hash = set_password(password)
    return check_password_hash(password, password_check)


def psw():
    with open(f"{config.BASE_DIR}/.spk", 'r') as file:
        psw_s = file.read()
    return psw_s


def psw_w(par):
    try:
        with open(f"{config.BASE_DIR}/.spk", 'w') as file:
            file.write(par)
        return True
    except:
        return False


@app.route("/login", methods=["POST", "GET"])
def login():
    app.logger.info("login user")
    if current_user.is_authenticated:
        # Переделать
        return redirect(url_for('index'))

    if request.method == "POST":
        if request.form['email'] == config.USR_NAME and check_password(psw(), request.form['psw']):
            user_id = random.randint(999, 9999)
            userlogin = UserLogin().create(user_id)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("index"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", title="Авторизация")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('index'))



@app.route("/")
@login_required
def index():
    return render_template('index.html')


@app.route("/error")
@login_required
def error():
    return render_template('error.html')


@app.route('/about_chanels', methods=["GET"])
@login_required
def about_chanels():
    """Информация о тлг каналах"""
    chanels = s.query(Chanels).all()
    return render_template('about_chanels.html', info=chanels)


@app.route('/select_channel', methods=["POST", "GET"])
@login_required
def select_channel():
    chanels = s.query(Chanels).all()
    return render_template('select_channel.html', chanels=chanels)


@app.route('/schedule', methods=["POST", "GET"])
@login_required
def schedule():
    if request.method == "POST":
        date_start = datetime.strptime(f"{request.form['date_start']} {request.form['time_start']}", '%Y-%m-%d %H:%M')
        date_stop = datetime.strptime(f"{request.form['date_stop']} {request.form['time_stop']}", '%Y-%m-%d %H:%M')
        records = s.query(Events, MediaContens, TypeMedia, func.string_agg(Tags.name, literal_column("', '")).label("tags")). \
            join(MediaContens, MediaContens.id_media == Events.id_media). \
            join(TypeMedia, TypeMedia.id_type_media == MediaContens.id_type_media). \
            join(MediaTags, MediaTags.id_media == MediaContens.id_media, isouter=True). \
            join(Tags, Tags.id_tag == MediaTags.id_tag, isouter=True). \
            group_by(Events, MediaContens, TypeMedia). \
            filter(and_(Events.id_chanel == request.form['id_chanel'], Events.completed == False,
                        Events.date_start > date_start, Events.date_start < date_stop)).order_by(Events.date_start).all()
        return render_template('schedule.html', records=records)
    return render_template('index.html')


@app.route('/event', methods=["POST", "GET"])
@login_required
def event():
    if request.method == "POST":
        record = s.query(Events, MediaContens, TypeMedia,
                         func.string_agg(Tags.name, literal_column("','")).label("tags")). \
            join(MediaContens, MediaContens.id_media == Events.id_media). \
            join(TypeMedia, TypeMedia.id_type_media == MediaContens.id_type_media). \
            join(MediaTags, MediaTags.id_media == MediaContens.id_media, isouter=True). \
            join(Tags, Tags.id_tag == MediaTags.id_tag, isouter=True). \
            group_by(Events, MediaContens, TypeMedia). \
            filter(Events.id_event == request.form.get('id_event')).one()
        path_media = f"static/media/{record.TypeMedia.path_dir}/{str(record.MediaContens.local_path)}"
        tags = s.query(Tags.name, Tags.id_tag).all()
        if record.tags is None:
            tags_media = ()
        else:
            tags_media = tuple(item for item in record.tags.split(','))
        return render_template('event.html', record=record, path_media=path_media, tags=tags, tags_media=tags_media)
    return render_template('schedule.html')


@app.route('/edit_event', methods=["POST", "GET"])
@login_required
def edit_event():
    if request.method == "POST":
        try:
            record = s.query(Events, MediaContens, TypeMedia). \
                join(MediaContens, MediaContens.id_media == Events.id_media). \
                join(TypeMedia, TypeMedia.id_type_media == MediaContens.id_type_media). \
                filter(Events.id_event == request.form.get('id_event')).one()
            id_chanel = record.Events.id_chanel
            if request.form.get('save'):
                s.query(MediaTags).filter(MediaTags.id_media == record.Events.id_media).delete()
                for id_tag in request.form.getlist('tags'):
                    tags = MediaTags(id_media=record.MediaContens.id_media,
                                     id_tag=id_tag)
                    s.add(tags)
                record.Events.date_start = request.form.get('date_start')
                record.Events.date_stop = request.form.get('date_stop')
                if request.form.get('caption') != 'None':
                    record.Events.caption = request.form.get('caption')
                s.commit()
            elif request.form.get('remove_event'):
                record.Events.date_stop = record.Events.date_start
                if record.Events.id_message == 0:
                    record.Events.id_message = -1
                    record.Events.completed = True
                s.commit()
            elif request.form.get('remove_media'):
                record.MediaContens.remove = True
                s.commit()
            flash("Успешно сохранено", "success")
        except Exception as ex:
            #logging.info(ex)
            return render_template('error.html', info="ERROR SAVE")
        return redirect(url_for('schedule', id_chanel=id_chanel, time=24))


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('No file part', "error")
            file = request.files['file']
            if file.filename is None or file.filename == '':
                flash('No selected file', "error")
                return redirect(url_for('add_event'))
            if request.form.get('date_start') == None or request.form.get('time_start') == None \
                    or request.form.get('date_start') == '' or request.form.get('time_start') == '':
                flash('No enter data or time', "error")
                return redirect(request.url)
            date_start = datetime.strptime(f"{request.form['date_start']} {request.form['time_start']}", '%Y-%m-%d %H:%M')
            if date_start < datetime.now():
                flash('time < time now', "error")
                return redirect(url_for('add_event'))
            if request.form.get('date_stop') == '' or request.form.get('time_stop') == '':
                date_stop = date_start + timedelta(minutes=config.TIME_REMOVE_EVENT)
            else:
                date_stop = datetime.strptime(f"{request.form['date_stop']} {request.form['time_stop']}",
                                               '%Y-%m-%d %H:%M')
            root, ext = os.path.splitext(file.filename[-6:])
            ext = ext.lower()
            try:
                type_media = s.query(TypeMedia).filter(TypeMedia.extension == ext.strip('.')).one()
            except Exception as ex:
                flash('error extension file', "error")
                return redirect(url_for('add_event'))
            suffix = datetime.now().strftime("%y%m%d_%H%M%S")
            gen_name = "_".join([type_media.type_media, suffix])
            file.save(f"{config.PATH_FOR_MEDIA}/{type_media.path_dir}/{gen_name}{ext}")
            id_user = s.query(Users.id_user).filter(Users.name == config.USR_NAME).one()[0]
            media_contents = MediaContens(id_type_media=type_media.id_type_media,
                                          local_path=f'{gen_name}{ext}',
                                          id_user=id_user)
            s.add(media_contents)
            s.commit()
            events = Events(id_media=media_contents.id_media,
                            id_chanel=request.form.get('id_chanel'),
                            date_start=date_start,
                            date_stop=date_stop,
                            caption=request.form.get('caption'),
                            id_user=id_user)
            s.add(events)
            for id_tag in request.form.getlist('tags'):
                tags = MediaTags(id_media=media_contents.id_media,
                             id_tag=id_tag)
                s.add(tags)
            s.commit()
        except Exception as ex:
            flash('error save file', "error")
            #logging.info(ex)
            return redirect(request.url)
        flash('Событие сохранено', "success")
        return redirect(url_for('add_event'))

    return redirect(url_for('add_event'))


@app.route('/add_event', methods=["POST", "GET"])
@login_required
def add_event():
    chanels = s.query(Chanels.id_chanel, Chanels.name_chanel).all()
    tags = s.query(Tags.name, Tags.id_tag).all()
    max_date = s.query(func.max(Events.date_start)).one()
    return render_template('add_event.html', chanels=chanels, tags=tags, max_date=max_date[0])


@app.route('/add_media', methods=["POST", "GET"])
@login_required
def add_media():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', "error")
            return redirect(url_for('add_media'))
        file = request.files['file']
        if file.filename is None or file.filename == '':
            flash('No selected file', "error")
            return redirect(url_for('add_media'))
        if request.form.getlist('tags') == []:
            flash('No selected tags', "error")
            return redirect(url_for('add_media'))
        root, ext = os.path.splitext(file.filename[-6:])
        ext = ext.lower()
        try:
            type_media = s.query(TypeMedia).filter(TypeMedia.extension == ext.strip('.')).one()
        except Exception as ex:
            flash('error extension file', "error")
            return redirect(url_for('add_event'))
        suffix = datetime.now().strftime("%y%m%d_%H%M%S")
        gen_name = "_".join([type_media.type_media, suffix])
        file.save(f"{config.PATH_FOR_MEDIA}/{type_media.path_dir}/{gen_name}{ext}")
        id_user = s.query(Users.id_user).filter(Users.name == config.USR_NAME).one()[0]
        media_contents = MediaContens(id_type_media=type_media.id_type_media,
                                      local_path=f'{gen_name}{ext}',
                                      id_user=id_user,
                                      description=request.form.get('description'))
        s.add(media_contents)
        s.commit()
        for id_tag in request.form.getlist('tags'):
            tags = MediaTags(id_media=media_contents.id_media,
                             id_tag=id_tag)
            s.add(tags)
        s.commit()
    tags = s.query(Tags.name, Tags.id_tag).all()
    return render_template('/add_media.html', tags=tags)


@app.route('/create_schedule', methods=["POST", "GET"])
@login_required
def create_schedule():
    tags = s.query(Tags.name, Tags.id_tag).all()
    if request.method == "POST":
        if request.form.getlist('tags') == []:
            flash('No selected tags', "error")
            return redirect(url_for('create_schedule'))
        date_start = datetime.strptime(f"{request.form['start_date']} {request.form['start_time']}",
                          '%Y-%m-%d %H:%M')
        date_stop = datetime.strptime(f"{request.form['stop_date']} {request.form['stop_time']}",
                                      '%Y-%m-%d %H:%M')
        if date_start < datetime.now() or date_stop < datetime.now() or date_start > date_stop:
            flash('error date time', "error")
            return redirect(url_for('create_schedule'))
        period = timedelta(minutes=int(request.form['period']))
        time_delete = timedelta(minutes=1440)
        count_events = int((date_stop - date_start)/period)
        list_time = []
        next_time_event = date_start
        for i in range(count_events):
            list_time.append(next_time_event)
            next_time_event = next_time_event + period
            list_time.append(next_time_event+time_delete)
        records = s.query(MediaContens, TypeMedia). \
            join(TypeMedia, TypeMedia.id_type_media == MediaContens.id_type_media). \
            join(MediaTags, MediaTags.id_media == MediaContens.id_media, isouter=True). \
            join(Tags, Tags.id_tag == MediaTags.id_tag, isouter=True). \
            filter(and_(MediaTags.id_tag == 33, ~MediaContens.id_media.in_(s.query(Events.id_media).\
            filter(Events.id_chanel == request.form['id_chanel'])))).limit(count_events).all()
        return render_template('new_schedule.html', tags=tags, chanel=request.form['id_chanel'], records=records, list_time=list_time)

    chanels = s.query(Chanels.id_chanel, Chanels.name_chanel).all()
    return render_template('create_schedule.html', tags=tags, chanels=chanels)


@app.route('/save_schedule', methods=["POST", "GET"])
@login_required
def save_schedule():
    if request.method == "POST":
        request_dic = change_and_remove_req(request.form.to_dict())
        id_user = s.query(Users.id_user).filter(Users.name == config.USR_NAME).one()[0]
        for key, value in request_dic.items():
            if value == 'on':
                j = int(key.split("-")[1])
                events = Events(id_media=request_dic[f'id-{j}'],
                            id_chanel=request.form['id-chanel'],
                            date_start=request_dic[f'date_start-{j}'],
                            date_stop=request_dic[f'date_stop-{j}'],
                            caption=request_dic[f'description-{j}'],
                            id_user=id_user)
                s.add(events)
                s.commit()
        flash('Расписание сохранено', "success")
        return render_template('create_schedule.html')
    return render_template('create_schedule.html')


@app.route('/tags', methods=["POST", "GET"])
@login_required
def tags():
    return render_template('tags.html')

def change_and_remove_req(dic_req):
    len_dic = len(dic_req)
    lis_rem = []
    for key, value in dic_req.items():
        if value == 'off':
            j = int(key.split("-")[1])
            a = dic_req[f'date_start-{j}']
            s = dic_req[f'date_stop-{j}']
            lis_rem.append(j)
            for i in range(j, len_dic):
                i = i + 1
                if dic_req.get(f'date_start-{i}'):
                    b = dic_req[f'date_start-{i}']
                    c = dic_req[f'date_stop-{j}']
                    dic_req[f'date_start-{i}'] = a
                    a = b
                    s = c

    for rm in lis_rem:
        dic_req.pop(f'id-{rm}')
        dic_req.pop(f'save-{rm}')
        dic_req.pop(f'date_start-{rm}')
        dic_req.pop(f'date_stop-{rm}')
        dic_req.pop(f'description-{rm}')
    return dic_req

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0')create_schedule
