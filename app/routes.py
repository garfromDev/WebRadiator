from app import app, db
from flask import render_template, redirect, flash, url_for, request, jsonify
from app.forms import LoginForm, RadiatorForm, InteractionChoices
from app.models import UserInteraction, OverMode, DatedStatus, CalendarInUse
from app.schemas import WeekSchedule, ScheduleUpdate
from pydantic import ValidationError


app.logger.info("loading  routes")
@app.route('/')
def main_page():
    form = RadiatorForm()
    current_calendar = CalendarInUse.current
    current_interaction = UserInteraction.current()
    current_mode = current_interaction.overmode_status if current_interaction and current_interaction.overruled_status else None
    return render_template('index.html', 
                         title='Radiator',  
                         form=form, 
                         current_calendar=current_calendar.name if current_calendar else None,
                         current_mode=current_mode.value if current_mode else None)


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

@app.route('/calendar/edit')
def edit_calendar():
    """Page d'édition du planning de chauffage"""
    import json
    import os

    if not CalendarInUse.current:
        return jsonify({'error': 'Aucun calendrier sélectionné'}), 400

    calendar_file = f"{CalendarInUse.current.name}.json"
    file_path = os.path.join(app.root_path, '..', calendar_file)
    print("file_path ", file_path)
    # Lecture du planning existant
    try:
        if os.path.exists(file_path):
            print("file_path ", file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Conversion de l'ancien format vers le nouveau
                if 'weekCalendar' in data:
                    # Structure l'ancien format en nouveau format
                    converted_data = {
                        day.lower(): [data['weekCalendar'][day].get(f"{h:02d}:{m:02d}", "ECO")
                                    for h in range(24)
                                    for m in (0, 15, 30, 45)]
                        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    }
                    schedule = WeekSchedule.parse_obj(converted_data)
                else:
                    schedule = WeekSchedule.parse_obj(data)
        else:
            schedule = WeekSchedule.get_default_schedule()
    except Exception as e:
        app.logger.error(f'Erreur lors de la lecture du planning : {str(e)}')
        schedule = WeekSchedule.get_default_schedule()

    # Définit un titre descriptif selon le type de calendrier
    calendar_names = {
        'work': 'Semaine normale',
        'holiday': 'Vacances',
        'off': 'Absence'
    }
    calendar_title = calendar_names.get(CalendarInUse.current.name, CalendarInUse.current.name)
    
    return render_template('calendar_edit.html', 
                         title='Modifier le calendrier', 
                         calendar_name=calendar_title,
                         initial_schedule=schedule.dict())

@app.route('/calendar/set', methods=['POST'])
def set_calendar():
    """Sauvegarde le planning de chauffage"""
    try:
        if not CalendarInUse.current:
            return jsonify({'success': False, 'error': 'Aucun calendrier sélectionné'}), 400

        # Validation des données avec Pydantic
        data = request.get_json()
        schedule_update = ScheduleUpdate.parse_obj(data)

        # Conversion vers l'ancien format pour compatibilité
        old_format = {
            'weekCalendar': {
                'Monday': {},
                'Tuesday': {},
                'Wednesday': {},
                'Thursday': {},
                'Friday': {},
                'Saturday': {},
                'Sunday': {}
            }
        }

        days_map = {
            'monday': 'Monday',
            'tuesday': 'Tuesday',
            'wednesday': 'Wednesday',
            'thursday': 'Thursday',
            'friday': 'Friday',
            'saturday': 'Saturday',
            'sunday': 'Sunday'
        }

        # Conversion du nouveau format vers l'ancien
        for day_lower, day_proper in days_map.items():
            modes = schedule_update.schedule.dict()[day_lower]
            for slot_idx, mode in enumerate(modes):
                hour = slot_idx // 4
                minute = (slot_idx % 4) * 15
                time_key = f"{hour:02d}:{minute:02d}"
                old_format['weekCalendar'][day_proper][time_key] = mode

        # Sauvegarde dans le fichier correspondant au calendrier courant
        import json
        import os

        calendar_file = f"{CalendarInUse.current.name}.json"
        file_path = os.path.join(app.root_path, '..', calendar_file)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(old_format, f, indent=2, ensure_ascii=False)

        return jsonify({'success': True})

    except ValidationError as e:
        # Erreurs de validation Pydantic (format incorrect, valeurs invalides, etc.)
        app.logger.warning(f'Données invalides reçues : {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Données invalides',
            'details': e.errors()
        }), 400

    except Exception as e:
        app.logger.error(f'Erreur lors de la sauvegarde du planning : {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500
