import calculate_internal_forces as cf

def test_calc_factored_load():
    result = cf.calc_factored_load(5, 8)
    assert result == 18.75

def test_calc_moment_shear_beam_udl():
    result = cf.calc_moment_shear_beam_udl(8, 7.2, 4)
    assert result == (0, 57.6)
