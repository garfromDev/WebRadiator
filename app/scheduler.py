from .models import UserInteraction
from app import appscheduler, app
app.logger.info("loading scheduler")
from Radiator.DecisionMaker import DecisionMaker
from Radiator.UserInteractionManager import UserInteractionManager

decider = DecisionMaker(user_manager=UserInteractionManager(user_interaction_provider=UserInteraction(),
                                                            app=app))
app.logger.info("decider instanciated")


# @scheduler.task('interval', id='make_decision', seconds=20, misfire_grace_time=900)
def periodic_make_decision() -> None:
    with appscheduler.app.app_context():
        print("periodic_make_decision", appscheduler.app.app_context())
        app.logger.info("periodic make decision")
        decider.make_decision()


appscheduler.add_job(id='periodic_make_decision', func=periodic_make_decision, trigger='interval', seconds=10, misfire_grace_time=900 )
app.logger.info("scheduled job added")