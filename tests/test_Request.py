# -*- coding: utf-8 -*-

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock

from heppy.Daemon import Daemon
from heppy.Request import Request

LOGIN_DATA = {
    'command':     'epp:login',
    'login':       'REGISTRAR',
    'pw':          's3cret<&>pw',
    'newPassword': 'n3w-s3cret',
    'objURIs':     ['urn:ietf:params:xml:ns:domain-1.0'],
}

LOGIN_OK = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"><response>'
    '<result code="1000"><msg>Command completed successfully</msg></result>'
    '<trID><clTRID>AA-1</clTRID><svTRID>S-1</svTRID></trID>'
    '</response></epp>'
)


class TestMaskPasswords(unittest.TestCase):
    def test_masks_login_passwords(self):
        xml = Request.prettifyxml(str(Request.build(LOGIN_DATA)))
        masked = Request.mask_passwords(xml)
        self.assertNotIn('s3cret', masked)
        self.assertNotIn('n3w-s3cret', masked)
        self.assertIn('<pw>***</pw>', masked)
        self.assertIn('<newPW>***</newPW>', masked)
        self.assertIn('<clID>REGISTRAR</clID>', masked)

    def test_masks_prefixed_auth_info_password(self):
        xml = ('<domain:authInfo>\n    <domain:pw roid="X-1">abc\ndef</domain:pw>\n</domain:authInfo>'
               '<domain:name>pw.name</domain:name>')
        self.assertEqual(
            '<domain:authInfo>\n    <domain:pw roid="X-1">***</domain:pw>\n</domain:authInfo>'
            '<domain:name>pw.name</domain:name>',
            Request.mask_passwords(xml),
        )

    def test_leaves_other_xml_alone(self):
        xml = '<epp><hello/><pwd>x</pwd><svID>pw</svID></epp>'
        self.assertEqual(xml, Request.mask_passwords(xml))


class TestDaemonLoginOutput(unittest.TestCase):
    def test_login_does_not_print_password(self):
        daemon = Daemon({'epp': {}}, {})
        daemon.login_query = Request.build(LOGIN_DATA).toxml()
        daemon.request = MagicMock(return_value=LOGIN_OK)

        out = io.StringIO()
        with redirect_stdout(out):
            daemon.login()

        self.assertNotIn('s3cret', out.getvalue())
        self.assertIn('<pw>***</pw>', out.getvalue())
        self.assertIn('LOGIN OK', out.getvalue())


if __name__ == '__main__':
    unittest.main()
