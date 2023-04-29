def calc_moment_shear_beam_udl(length, load, distance):
    """
    Doc strings
    """
    shear = length * load / 2 - load * distance
    moment = length * load * distance / 2 - load * distance ** 2 / 2
    return shear, moment

def calc_factored_load(dead_load, live_load):
    """
    Doc strings
    """
    return 1.35 * dead_load + 1.5 * live_load

