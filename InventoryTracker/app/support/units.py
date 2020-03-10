from typing import Dict, List, Tuple
import re

from .unit_base import UnitBase

_ResistorIDBase = 100
_CIDB = 200

_ReExp = re.compile(r'^(\d+)(\D*)$')

class _UnitManager(object):
    """
    Manager class for units
    """

    def __init__(self, *args, **kwargs):
        self._MasterListCache = None;
        return super().__init__(*args, **kwargs)

    @property
    def AmpUnit(self):
        return UnitBase(postfix='A', id=1)

    @property
    def VoltUnit(self):
        return UnitBase(postfix='v', id=20)

    @property
    def FaradUnit(self):
        return UnitBase(postfix='F', id=_CIDB)

    @property
    def MilliFaradUnit(self):
        return UnitBase('m', 1.0e-3, self.FaradUnit, id=_CIDB + 1)

    @property
    def MicroFaradUnit(self):
        return UnitBase('u', 1.0e-6, self.FaradUnit, id=_CIDB + 2)

    @property
    def NanoFaradUnit(self):
        return UnitBase('n', 1.0e-9, self.FaradUnit, id=_CIDB + 3)

    @property
    def PicoFaradUnit(self):
        return UnitBase('p', 1.0e-12, self.FaradUnit, id=_CIDB + 4)

    @property
    def OhmsUnit(self):
        return UnitBase(postfix='Ω', id=_ResistorIDBase + 0)

    @property
    def KOhmsUnit(self):
        return UnitBase('K', 1000, self.OhmsUnit, id=_ResistorIDBase + 1)

    @property
    def MOhmsUnit(self):
        return UnitBase('M', 1000000, self.OhmsUnit, id=_ResistorIDBase + 2)

    @property
    def ResistorUnits(self):
        return (self.OhmsUnit,
                self.KOhmsUnit,
                self.MOhmsUnit)

    @property
    def CapacitorUnits(self):
        return (self.FaradUnit,
            self.MilliFaradUnit,
            self.MicroFaradUnit,
            self.NanoFaradUnit,
            self.PicoFaradUnit)

    @property
    def CapacitorChoices(self):
        Res = list()

        for x in self.CapacitorUnits:
            Res.append((x.ID, x.Designator))

        return Res

    @property
    def ResistorChoices(self):
        """
        Get a list of choices for resistor values
        """

        Res = list()
        for x in self.ResistorUnits:
            Res.append((x.ID, x.Designator))

        return Res

    @property
    def MasterUnitList(self)->List[UnitBase]:
        """
        Returns a master list of all units
        """
        if self._MasterListCache is None:
            Res = [self.AmpUnit, self.VoltUnit]
            Res = Res + list(self.CapacitorUnits) + list(self.ResistorUnits)
            self._MasterListCache = tuple(Res)

        return self._MasterListCache


    def GetUnitFromID(self, id:int)->UnitBase:
        """
        Given a unit ID, Attempt to find the unit
        """
        for x in self.MasterUnitList:
            if id == x.ID:
                return x

        return None

    def SplitValue(self, value:str):
        M = _ReExp.match(value)
        return (M[1], M[2])

    def FindUnit(self, post:str, units:List[UnitBase]) -> UnitBase:
        """
        Find a unit base
        """
        post = post.lower()

        for u in units:
            if post == u.Postfix.lower():
                return u

        return None


UnitManager = _UnitManager()