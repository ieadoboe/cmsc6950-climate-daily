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
    # Error checking
    if hasattr(t_max, "__len__"):  # for arrays
        if (t_max < t_min).any():
            raise ValueError("t_min must be <= t_max for all entries")
    else:  # for scalars
        if (t_max < t_min):
            raise ValueError("t_min must be <= t_max")

    dtr = t_max - t_min
    return dtr
