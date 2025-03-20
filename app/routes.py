from app import app, db
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RadiatorForm, InteractionChoices
from app.models import UserInteraction, OverMode, DatedStatus, CalendarInUse


app.logger.info("loading  routes")
@app.route('/')
def main_page():
    form = RadiatorForm()
    return render_template('index.html', title='Radiator',  form=form)


@app.route('/mode/<heating_mode>')
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
    CalendarInUse.set_in_use(calendar_type)
    return redirect(url_for('main_page'))
