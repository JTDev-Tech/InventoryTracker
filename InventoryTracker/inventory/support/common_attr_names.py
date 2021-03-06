class CommonAttrNamesMeta(type):
    """
    Class that contains common attribute names used throughout the application
    """

    @property
    def Tolerance(cls)->str:
        return "Tolerance"

    @property
    def ValueUnit(cls)->str:
        return "ValueUnit"

    @property
    def Voltage(cls)->str:
        return "Voltage"

class CommonAttrNames(object, metaclass=CommonAttrNamesMeta):
    """
    Class that contains common attribute names used throughout the application
    """
