# WebRadiator Copilot instructions

## Setup and runtime

- Create/activate the Python environment, then install dependencies with `python3 -m pip install -r requirements.txt`.
- The application entry point is `web_radiator:app`. Flask development can be started with `flask run --host=0.0.0.0 -p 3000`; `launch.sh` is the Raspberry Pi-oriented launcher and exports `RADIATOR_TEST_ENVIRONMENT="false"` before starting Flask on port 3000.
- Set `RADIATOR_TEST_ENVIRONMENT=true` when hardware access must be avoided. `HeatMode.py` and the SIGTERM handler use this flag; it is read in addition to the Flask configuration.
- Configuration is in `config.py`. The database URL is read from `DATABASE_URL` (default: SQLite `app.db`), while `SECRET_KEY` and `RADIATOR_TEST_ENVIRONMENT` are also environment-configurable.
- In this environment, start the app as `RADIATOR_TEST_ENVIRONMENT=true flask run --host=0.0.0.0 -p 5000` when developing or testing the Flask UI locally.

## Build, database migrations, and tests

- There is no separate build step or configured Python linter/formatter.
- Database migrations use Flask-Migrate/Alembic: `flask db migrate -m "description"` creates a migration, and `flask db upgrade` applies it. Existing migrations are under `migrations/versions/`.
- Flask shell context is configured in `web_radiator.py` with `db` and `UserInteraction`.
- Tests are Robot Framework suites under `Radiator/testCases/` with Python libraries under `Radiator/testCases/testLibs/`.
- Run the full suite from the repository root with:
  `cd Radiator/testCases && robot test*.robot`
- Run one suite, for example the calendar suite, with:
  `cd Radiator/testCases && robot testHeatCalendar.robot`
- Run one named Robot test case with:
  `cd Radiator/testCases && robot --test "mode eco" testHeatCalendar.robot`
- The heat/HW suite is hardware-dependent and explicitly warns not to run it against actual hardware unless the GPIO mapping is intended. `testHeatMode.robot` is approximately 20 minutes long. Its library imports `RPi.GPIO`; provide a Raspberry Pi/test environment for that suite rather than assuming local macOS/Linux hardware support.
- The suite does not currently install Robot Framework or RPi.GPIO in `requirements.txt`, so those test dependencies must be available before running Robot tests.

## Architecture

- `app/__init__.py` creates the Flask application and global SQLAlchemy, migration, Bootstrap, and APScheduler objects. It starts a scheduler and imports `app.scheduler` and `app.routes` in the application context.
- `app/routes.py` exposes the web UI and JSON calendar endpoints. `app/scheduler.py` schedules `periodic_make_decision()` every 60 seconds; that method creates and runs the central `Radiator.DecisionMaker.DecisionMaker` decision cycle.
- `app/models.py` contains SQLAlchemy persistence for temporary user overrides (`UserInteraction`) and the active calendar (`CalendarInUse`). User status expiration is checked both through model methods and in `UserInteractionManager`.
- `app/schemas.py` validates calendar updates with Pydantic. A complete week has exactly 96 quarter-hour slots per day (`24 * 4`) and uses `ECO`, `CONFORT`, or `OFF` modes.
- `Radiator/DecisionMaker.py` is the control-path orchestrator: current calendar meta-mode, then user overrule, then bonus/down adjustments, then the `HeatMode` hardware/driver command.
- `Radiator/HeatCalendar.py` reads active-calendar JSON files in the repository root. `app/routes.py` still converts the web editor's 96-slot representation to and from the legacy `weekCalendar` JSON shape, so retain compatibility with both structures in calendar code.
- `Radiator/HeatMode.py` translates decision modes into pilot-wire GPIO states and sequences. Keep hardware writes behind `RADIATOR_TEST_ENVIRONMENT=true`/the `test` module flag.
- `app/templates/` contains Jinja pages and `app/static/js/calendar_edit.js` implements the quarter-hour schedule editor. Calendar saves go through `POST /calendar/set` and Pydantic validation.

## Repository-specific conventions

- Calendar JSON files are stored at repository root (`week.json`, `holiday.json`, `off.json`) and use 15-minute keys in the legacy `weekCalendar` structure. `CalendarInUse.current.name` selects the active calendar file.
- `OverMode` is the shared meta-mode enum across Flask models, the calendar, and the decision engine. Preserve its string values (`ECO`, `CONFORT`, `OFF`, `UNKNOWN`) when crossing JSON, Pydantic, SQLAlchemy, or route boundaries.
- User route `/mode/<heating_mode>` writes dated interaction records; it does not directly change GPIO. Runtime control is applied by the APScheduler decision job.
- Scheduler and Flask code require application context around database access. Preserve `with appscheduler.app.app_context():` patterns for scheduled work.
- Hardware constants and GPIO behavior live in `Radiator/HeatMode.py`; hardware tests and libraries are in `Radiator/testCases/testLibs/` rather than as pytest/unittest modules.
- Flask routes in [app/routes.py](/Users/alistef/workspace/WebRadiator/app/routes.py) use direct module-level SQLAlchemy operations and redirects/JSON responses; follow the existing module style rather than introducing a separate API or service layer for a small route change.
