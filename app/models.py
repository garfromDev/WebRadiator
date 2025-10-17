import enum

from app import db
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Type
from werkzeug.security import generate_password_hash, check_password_hash


class classproperty:
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, obj, owner):
        return self.fget(owner)


class DatedStatus:
    def __init__(self, status: bool = True, expiration_date: Optional[datetime] = None):
        """ Par défaut, les statuts expirent le jour même à minuit et sont actifs """
        self.status = status
        self.expiration_date = expiration_date or datetime.today().replace(hour=23, minute=59, second=0)

    def __composite_values__(self):
        return self.status, self.expiration_date

    def __repr__(self):
        return f"{self.status} until {self.expiration_date}"

    def __eq__(self, other):
        return isinstance(other, DatedStatus) and \
               self.status == other.status and \
               self.expiration_date == other.expiration_date

    def __ne__(self, other):
        return not self.__eq__(other)


class OverMode(str, Enum):
    ECO = "ECO"
    CONFORT = "CONFORT"
    OFF = "OFF"
    UNKNOWN = "UNKNOWN"


@dataclass
class OverruledStatus:
    status: DatedStatus
    overMode: OverMode = OverMode.UNKNOWN

    @classmethod
    def generate(cls, status: bool, exp_date: datetime, overmode: OverMode):
        return OverruledStatus(DatedStatus(status, exp_date), overmode)

    def __composite_values__(self):
        return self.status.__composite_values__(), self.overMode

    def __repr__(self):
        return f"{self.overMode} {self.status.status} until {self.status.expiration_date}"

    def __eq__(self, other):
        return isinstance(other, OverruledStatus) and \
               self.status == other.status and \
               self.overMode == other.overMode

    def __ne__(self, other):
        return not self.__eq__(other)


T = TypeVar('T', bound='UserInteraction')


class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    overruled_status = db.Column(db.Boolean, default=False)
    overruled_exp_date = db.Column(db.DateTime, default=datetime(2021, 1, 1))
    overruled = db.composite(DatedStatus, overruled_status, overruled_exp_date)
    overmode_status = db.Column(db.Enum(OverMode), default=OverMode.UNKNOWN)
    overmode = db.composite(OverruledStatus.generate, overruled_status, overruled_exp_date, overmode_status)
    userbonus_status = db.Column(db.Boolean, default=False)
    userbonus_exp_date = db.Column(db.DateTime, default=datetime(2021, 1, 1))
    userbonus = db.composite(DatedStatus, userbonus_status, userbonus_exp_date)
    userdown_status = db.Column(db.Boolean, default=False)
    userdown_exp_date = db.Column(db.DateTime, default=datetime(2021, 1, 1))
    userdown = db.composite(DatedStatus, userdown_status, userdown_exp_date)
    targettemp = db.Column(db.Float)  # TODO ajouter CST.DEFAULT_TARGET_TEMP ?

    def __repr__(self):
        return self.__dict__.__repr__()

    @classmethod
    def current(cls: Type[T]) -> Optional[T]:
        return cls.query.order_by(UserInteraction.id.desc()).first()


class InUse(enum.Enum):
    true = True


class CalendarInUse(db.Model):
    """ Cette table contient les noms des calendriers disponibles, un seul est le courant """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # un seul calendrier actif à un instant donné
    in_use = db.Column(db.Enum(InUse), unique=True)

    @classmethod
    def set_in_use(cls, calendar: str):
        cal_in_use = db.session.execute(db.select(CalendarInUse)
                                        .filter_by(in_use=InUse.true)).scalar()
        existing_cal = db.session.execute(db.select(CalendarInUse).filter_by(name=calendar)).scalar()
        if cal_in_use and cal_in_use.name == calendar:
            return  # already in use
        elif cal_in_use:
            cal_in_use.in_use = None
            db.session.commit()
        if existing_cal and existing_cal != cal_in_use:
            existing_cal.in_use = InUse.true
            db.session.commit()
        else:
            new_cal = CalendarInUse(name=calendar, in_use=InUse.true)
            db.session.add(new_cal)
            db.session.commit()

    @classproperty
    def current(cls: T) -> T:
        return db.session.execute(
            db.select(CalendarInUse).filter_by(in_use=InUse.true)).scalar() or None
