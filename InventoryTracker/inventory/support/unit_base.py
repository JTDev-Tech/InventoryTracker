class UnitBase(object):
    """description of class"""

    def __init__(self, unit:str=None, divider:float = None, parent=None, postfix:str=None,
                 id:int=None):
        self.__Unit = unit
        self.__Divider = divider
        self.__Parent = parent
        self.__Postfix = postfix
        self.__ID = id
        return super().__init__()

    @property
    def Designator(self):
        if self.__Parent is None:
            return self.Postfix
        else:
            return self.__Unit + self.__Parent.Postfix

    @property
    def Postfix(self):
        """
        Postfix unit.
        """
        return self.__Postfix

    @property
    def ID(self):
        return self.__ID
