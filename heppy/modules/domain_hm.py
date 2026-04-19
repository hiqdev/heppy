# -*- coding: utf-8 -*-

from domain import domain

from ..TagData import TagData

class domain_hm(domain):
    CONTACT_TYPES = (
        'admin',
        'tech',
    )

    def render_info(self, request, data):
        command = self.render_command_with_fields(request, 'info', [
            TagData('name', data.get('name'), {})
        ])
        if 'pw' in data:
            self.render_auth_info(request, command, data['pw'])
