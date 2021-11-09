"""
string -> (nominal_value, std_dev) parsing functions from the uncertainties package
by Eric O. Legibot, adapted by P. Kraus. See original License below:

Copyright (c) 2010-2020, Eric O. LEBIGOT (EOL).
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
    * The names of its contributors may not be used to endorse or promote products 
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re

POSITIVE_DECIMAL_UNSIGNED_OR_NON_FINITE = r"((\d*)(\.\d*)?|nan|NAN|inf|INF)"

NUMBER_WITH_UNCERT_RE_STR = u"""
    ([+-])?  # Sign
    %s  # Main number
    (?:\\(%s\\))?  # Optional uncertainty
    (?:
        (?:[eE]|\\s*×\\s*10)
        (.*)
    )?  # Optional exponent
    """ % (
    POSITIVE_DECIMAL_UNSIGNED_OR_NON_FINITE,
    POSITIVE_DECIMAL_UNSIGNED_OR_NON_FINITE,
)

NUMBER_WITH_UNCERT_RE_MATCH = re.compile(
    u"%s$" % NUMBER_WITH_UNCERT_RE_STR, re.VERBOSE
).match


NUMBER_WITH_UNCERT_GLOBAL_EXP_RE_MATCH = re.compile(
    u"""
    \\(
    (?P<simple_num_with_uncert>.*)
    \\)
    (?:[eE]|\\s*×\\s*10) (?P<exp_value>.*)
    $""",
    re.VERBOSE,
).match


def parse_error_in_parentheses(representation):
    # !!!! The code seems to handle superscript exponents, but the
    # docstring doesn't reflect this!?
    """
    Return (value, error) from a string representing a number with
    uncertainty like 12.34(5), 12.34(142), 12.5(3.4), 12.3(4.2)e3, or
    13.4(nan)e10.  If no parenthesis is given, an uncertainty of one
    on the last digit is assumed.
    The digits between parentheses correspond to the same number of digits
    at the end of the nominal value (the decimal point in the uncertainty
    is optional). Example: 12.34(142) = 12.34±1.42.

    Raises ValueError if the string cannot be parsed.
    """

    match = NUMBER_WITH_UNCERT_RE_MATCH(representation)

    if match:
        # The 'main' part is the nominal value, with 'int'eger part, and
        # 'dec'imal part.  The 'uncert'ainty is similarly broken into its
        # integer and decimal parts.
        (
            sign,
            main,
            _,
            main_dec,
            uncert,
            uncert_int,
            uncert_dec,
            exponent,
        ) = match.groups()
    else:
        raise NotParenUncert(
            "Unparsable number representation: '%s'."
            " See the documentation of ufloat_fromstr()." % representation
        )

    # Global exponent:
    if exponent:
        factor = 10.0 ** int(exponent)
    else:
        factor = 1

    # Nominal value:
    value = float((sign or "") + main) * factor

    if uncert is None:
        # No uncertainty was found: an uncertainty of 1 on the last
        # digit is assumed:
        uncert_int = "1"  # The other parts of the uncertainty are None

    # Do we have a fully explicit uncertainty?
    if uncert_dec is not None or uncert in {"nan", "NAN", "inf", "INF"}:
        uncert_value = float(uncert)
    else:
        # uncert_int represents an uncertainty on the last digits:

        # The number of digits after the period defines the power of
        # 10 that must be applied to the provided uncertainty:
        if main_dec is None:
            num_digits_after_period = 0
        else:
            num_digits_after_period = len(main_dec) - 1

        uncert_value = int(uncert_int) / 10.0 ** num_digits_after_period

    # We apply the exponent to the uncertainty as well:
    uncert_value *= factor

    return (value, uncert_value)


def floats_fromstr(representation):
    match = NUMBER_WITH_UNCERT_GLOBAL_EXP_RE_MATCH(representation)
    if match:
        exp_value_str = match.group("exp_value")
        exponent = int(exp_value_str)
        factor = 10.0 ** exponent
        representation = match.group("simple_num_with_uncert")
    else:
        factor = 1  # No global exponential factor

    match = re.match(u"(.*)(?:\\+/-|±)(.*)", representation)
    if match:

        (nom_value, uncert) = match.groups()

        # Simple form 1234.45+/-1.2 or 1234.45±1.2, or 1.23e-10+/-1e-23
        # or -1.2×10⁻¹²±1e23:
        parsed_values = (float(nom_value) * factor, float(uncert) * factor)

    else:
        # Form with error parentheses or no uncertainty:
        parsed_values = parse_error_in_parentheses(representation)

    return parsed_values
