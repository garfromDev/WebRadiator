# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Protocol, Dict, Any, cast
from app.models import UserInteraction, OverMode
from .logger_provider import logger


class UserInteractionProvider(Protocol):
    @classmethod
    def current(cls) -> UserInteraction:
        pass


class UserManager(Protocol):
    ...


class UserInteractionManager(object):
    """
      this module allows interfacing with user about
      overruling the calendar (vacation, day at home, ...)
      it will fetch the user decision in a json file
    """

    def __init__(self, user_interaction_provider: UserInteractionProvider, app):
        self._userInputs = None
        self._user_interaction_provider = user_interaction_provider
        self._app = app
        app.logger.debug("Init  UserInteractionManager with app %s", bool(app is not None))

    def update(self) -> None:
        self._userInputs = self._getUserInputs()

    def overruled(self) -> bool:
        """
          return: true if user has decided to temporary overrule the heatCalendar
        """
        logger.debug("overruled will return %s" % self._isValid(self._userInputs["overruled"]))
        return self._isValid(self._userInputs["overruled"])

    def over_mode(self) -> OverMode:
        """
          return: the metamode choosen by the user (ECO, CONFORT, ..)
          It is the consumer responsability to check overrule validity, no check done here
          In case the userInputs dictionary do not contains key, return UNKNOW
        """
        try:
            return cast(OverMode, self._userInputs["overruled"]["overMode"])
        except KeyError:
            return OverMode.UNKNOWN

    def userBonus(self) -> bool:
        """
          return: true if user has requested to increase temperature
        """
        return self._isValid(self._userInputs["userBonus"])

    def userDown(self) -> bool:
        """
          return: true if user has requested to decrease temperature
        """
        return self._isValid(self._userInputs["userDown"])

    def _getUserInputs(self) -> Dict[str, Any]:
        """
          return userInteraction dictionary from the database
          if database access fails or database empty, return a stub dict
        """
        default = {"overruled": {"status": False, "expirationDate": "01-01-2000", "overMode": "UNKNOW"},
                   "userBonus": {"status": False, "expirationDate": "01-01-2000"},
                   "userDown": {"status": False, "expirationDate": "01-01-2000"},
                   }
        try:
            with self._app.app_context():
                user_interaction: UserInteraction = self._user_interaction_provider.current()
                res = user_interaction and {
                    "overruled": {"status": user_interaction.overruled_status,
                                  "expirationDate": user_interaction.overruled_exp_date,
                                  "overMode": user_interaction.overmode_status},
                    "userBonus": {"status": user_interaction.userbonus_status,
                                  "expirationDate": user_interaction.userbonus_exp_date},
                    "userDown": {"status": user_interaction.userdown_status,
                                 "expirationDate": user_interaction.userdown_exp_date},
                } or default
        except Exception as err:
            # soit le fichier n'a pu être lu, soit le calendrier n'est pas complet
            logger.error(err)
            res = default
        logger.debug("== _getUserInputs %s" % res)
        return res

    @staticmethod
    def _is_valid_date(date_to_check: datetime) -> bool:
        """
          return true if the date_to_check is in the future
        """
        return date_to_check >= datetime.now()

    def _isValid(self, decision_bloc: Dict[str, Any]) -> bool:
        """
          return true if the status is true and the expiration date not met
          will return False if decisionBloc dictionnary do not contain appropriate keys
        """
        try:
            return bool(decision_bloc["status"] and self._is_valid_date(decision_bloc["expirationDate"]))
        except Exception as err:
            logger.error(err)
            return False

    def targetTemp(self) -> float:
        """
          return: the target temp chosen by the user or None
        """
        return cast(float, self._userInputs['targetTemp'])


if __name__ == '__main__':
    from app import app
    print("testing UserInteractionManager manually")
    # logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    # FIXME: fournir un mock qui n'accède pas à la base pour le test
    test = UserInteractionManager(UserInteraction(), app)
    print("overruled : {}  userBonus : {}  userDown : {}  mode : {}".format(test.overruled(), test.userBonus(),
                                                                            test.userDown(), test.over_mode()))
