from app import app, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
import random
from app.forms import LoginForm, RadiatorForm, InteractionChoices
from app.models import User, UserInteraction, OverMode, DatedStatus


@app.route('/')
# @login_required
def main_page():
    form = RadiatorForm()
    return render_template('index.html', title='Radiator',  form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            # domain is a full domain, not an inside domain  of my site -> forbidden
            next_page = url_for('main_page')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/mode/<heating_mode>')
#@login_required
def mode(heating_mode: str):
    """ Ecrit en base un enregistrement de UserInteaction pour le choix de l'utilisateur """
    usi = None
    if heating_mode == "eco":
        usi = UserInteraction(overruled=DatedStatus(True), overmode_status=OverMode.ECO)
    elif heating_mode == "minus1":
        usi = UserInteraction(overruled=DatedStatus(True), overmode_status=OverMode.CONFORT)
    elif heating_mode == InteractionChoices.off.name:
        pass  # FIXME: not implemented, décider ce qu'on en fait  ?
    elif heating_mode == "confort":
        usi = UserInteraction(overruled=DatedStatus(True), overmode_status=OverMode.CONFORT,
                              userbonus=DatedStatus(True))
    elif heating_mode == "minus2":
        usi = UserInteraction(overruled=DatedStatus(True), overmode_status=OverMode.CONFORT,
                              userdown=DatedStatus(True))
    if usi:
        db.session.add(usi)
        db.session.commit()

    return redirect(url_for('main_page'))


@app.route('/calendar/<calendar_type>')
def calendar(calendar_type: str):
    """ Bascule le calendrier  :
    semaine  : la  semaine  définie par week.json
    vacance : la semaine définie par holiday.json
    absence: mode  eco  permanent (calendrier nobody.json)
    a terme, on pourra mettre en  base le calendrier et modifier HeatCalendar pour  lire dans la base
    puis ensuite ajouter une interface de modification des calendriers
    """
    # TODO: implement
    return redirect(url_for('main_page'))

