# -*- coding: utf-8 -*-

from .fee10 import fee10

class fee10pre(fee10):
    # draft-ietf-regext-epp-fees used the bare urn:ietf:params:xml:ns:fee-1.0
    # namespace through revision -12, before renaming it to
    # urn:ietf:params:xml:ns:epp:fee-1.0 in -13 (the name RFC 8748 shipped
    # with, mapped to fee10). The wire format is otherwise identical — this
    # only exists so a registry still running the pre-rename namespace is
    # recognized instead of silently ignored.
    pass
