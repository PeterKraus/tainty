from .main import tufloat
from .read import floats_fromstr


def tufloat_fromstr(input):
    return tufloat(*floats_fromstr(input))
