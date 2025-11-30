"""Daily Temperature Range Functions"""


def calculate_dtr(t_min, t_max):
    """
    Calculate Diurnal Temperature Range (DTR)

    DTR = T_max - T_min

    Params
    ------
        t_min: Minimum temperature (in degrees Celsius)
        t_max: Maximum temperature (in degrees Celsius)

    Returns
    -------
        float, array or Series
            Diurnal Temperature Range
    """
    return t_max - t_min
