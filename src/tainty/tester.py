import uncertainties as un
import metrolopy as uc
import timeit
import random
import math

from main import tufloat


def check_addition(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = sum(uns)
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = sum(us)
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_addition_float(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0].n + uns[1] + uns[2].n
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0].n + us[1] + us[2].n
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_multiplication(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0] * uns[1] * uns[2]
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0] * us[1] * us[2]
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_multiplication_float(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0].n * uns[1] * uns[2].n
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0].n * us[1] * us[2].n
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_subtraction(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0] - uns[1] - uns[2]
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0] - us[1] - us[2]
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_subtraction_float(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0].n - uns[1] - uns[2].n
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0].n - us[1] - us[2].n
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_division(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0] / uns[1] / uns[2]
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0] / us[1] / us[2]
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_division_float(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0].n / uns[1] / uns[2].n
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0].n / us[1] / us[2].n
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 9) == round(ua.s, 9), f"{a.s} vs {ua.s}"


def check_power(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0] ** uns[1]  # ** uns[2]
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0] ** us[1]  # ** us[2]
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(a.s, 3) == round(ua.s, 3), f"{a.s} vs {ua.s}"


def check_power_float(ns, ss):
    uns = [un.ufloat(*i) for i in zip(ns, ss)]
    ua = uns[0].n ** uns[1]  # ** uns[2].n
    ub = uns[0] ** uns[1].n
    us = [tufloat(*i) for i in zip(ns, ss)]
    a = us[0].n ** us[1]  # ** us[2].n
    b = us[0] ** us[1].n
    assert round(a.n, 9) == round(ua.n, 9), f"{a.n} vs {ua.n}"
    assert round(b.n, 9) == round(ub.n, 9), f"{b.n} vs {ub.n}"
    assert round(a.s, 3) == round(ua.s, 3), f"{a.s} vs {ua.s}"
    assert round(b.s, 3) == round(ub.s, 3), f"{b.s} vs {ub.s}"


for i in range(100):
    random.seed()
    l = 3
    ns = [random.random() * 10 for i in range(l)]
    ss = [n * random.random() * 0.1 for n in ns]
    check_addition(ns, ss)
    check_addition_float(ns, ss)
    check_multiplication(ns, ss)
    check_multiplication_float(ns, ss)
    check_subtraction(ns, ss)
    check_subtraction_float(ns, ss)
    check_division(ns, ss)
    check_division_float(ns, ss)
    check_power(ns, ss)
    check_power_float(ns, ss)
