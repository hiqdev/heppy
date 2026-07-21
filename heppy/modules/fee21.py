# -*- coding: utf-8 -*-

from .fee import fee

class fee21(fee):
    # Per draft-ietf-regext-epp-fees, <fee:cd> identifies the checked object
    # with a plain-text <fee:objID> (not fee11/12's <fee:object><domain:name>,
    # nor a bare <fee:name>) and nests price fields inside <fee:command
    # name="...">, not as siblings of it. fee.parse_cd (parse_cd_tag_extension)
    # only reads direct children of <cd> and keys the result on 'name', so it
    # neither finds objID under 'name' nor descends into <command> — it must
    # not be inherited unchanged here.
    def parse_cd(self, response, tag):
        return self.parse_cd_nested_command(response, tag, object_id=True)

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency',  {}, data.get('currency', 'USD'))
        request.add_subtag(ext, 'fee:command', {'name': data.get('action', 'create')})
