from .models import UserInteraction
from app import appscheduler, app
from Radiator.DecisionMaker import DecisionMaker
from Radiator.UserInteractionManager import UserInteractionManager

decider = DecisionMaker(user_manager=UserInteractionManager(user_interaction_provider=UserInteraction(),
                                                            app=app))


def periodic_make_decision() -> None:
    with appscheduler.app.app_context():
        decider.make_decision()


appscheduler.add_job(id='periodic_make_decision', func=periodic_make_decision, trigger='interval', seconds=60, misfire_grace_time=900 )
app.logger.debug("scheduled job added")