# -*- coding: utf-8 -*-

from .fee import fee

class fee10(fee):
    # fee IS the RFC 8748 / epp:fee-1.0 behaviour now (see fee.py) — this
    # exists only so callers that explicitly type "fee10:" (rather than the
    # bare "fee:" that also resolves here) keep working the same way.
    pass
