"""unit conversions.

Start very simple:
 - Only allow exact-match units initially (g, ml, item)
 - Reject mismatched units

 Later improvements:
 - Unit conversion table
 - Use a units library like `pint`

    Unit classes have a range of units they can accept, e.g. fluid volume.

    Conversion methods accept input quantity, unit and output unit,
    then convert via a standard internal unit.
    e.g. fl.oz -> L -> mL.
"""

