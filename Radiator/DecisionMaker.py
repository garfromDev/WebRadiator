# -*- coding: utf-8 -*-
import logging
from typing import Optional, Any
from app import models
from app.models import OverMode
from .CST import CST
from .HeatCalendar import HeatCalendar
from .HeatMode import HeatMode, ComfortMode
from .UserInteractionManager import UserInteractionManager
from .logger_provider import logger


class DecisionMaker(object):
    """Central decision point of Radiator
    will be called every x min by main sequencer
    Create and parameterize during init() the different objects needed
    decide meta-mode based on HeatCalendar and user overrule
    in metaComfort, decide heating mode based on
      - ext temp
      - sun
      - felt internal temp (combine heat and humidity)
    """

    _userManager: Any

    @property
    def user_bonus(self) -> bool:
        return self._userManager.userBonus()

    @property
    def user_down(self) -> bool:
        return self._userManager.userDown()

    @property
    def overruled(self) -> bool:
        return self._userManager.overruled()

    @property
    def overmode(self) -> OverMode:
        return self._userManager.over_mode()

    def __init__(
        self,
        calendar=HeatCalendar(calFile=CST.WEEKCALJSON),
        user_manager: Optional[UserInteractionManager] = None,
    ):
        self._calendar = calendar
        self.metaMode = self._calendar.getCurrentMode()
        self._heater = HeatMode()
        self._userManager = user_manager or UserInteractionManager(
            user_interaction_provider=models.UserInteraction()
        )

    def make_decision(self, app) -> str:
        # 0 get meta mode from calendar
        meta_mode: OverMode = self._calendar.getCurrentMode()
        self._userManager.update(app)
        info = "mode from calendar : " + str(meta_mode)
        logger.debug(
            "makeDecision metamode = {}  Bonus = {} "
            "  userDown = {} overruled = {} overMode = {}".format(
                meta_mode,
                self.user_bonus,
                self.user_down,
                self.overruled,
                self.overmode,
            )
        )

        #  1 apply overrule by user
        if self.overruled:
            meta_mode = self.overmode
            info = info + "  applied overruled " + str(meta_mode)
        #  2 eco mode
        if meta_mode != OverMode.CONFORT:
            # UNKNOWN will apply eco
            self._heater.set_eco_mode()
            info = info + "  make decision setEcoMode"
            logger.info(info)
            return str(meta_mode)

        # metaMode == CONFORT:
        comfort_mode = ComfortMode()
        #  3 adaptation of comfort mode according user bonus
        if self.user_bonus:
            comfort_mode = ComfortMode("confort")
        elif self.user_down:
            comfort_mode = ComfortMode("minus2")

        # 5 application of comfort mode
        self._heater.set_from_confort_mode(comfort_mode)
        info = info + "  Heating mode applied : {}".format(comfort_mode)
        logger.info(info)
        return str(comfort_mode)


if __name__ == "__main__":
    print("testing DecisionMaker manually")
    test = DecisionMaker()
    print("decision  taken : " + test.make_decision())
    print("Decision taken can be inspected in log file or through StateDisplay")
