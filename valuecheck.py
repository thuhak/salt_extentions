#!/usr/bin/env python


def check(name, rule=None, ignorecase=False, dotall=False):
    '''
    check if value match rule, if not specify rule, check if value exists.
    '''
    import re
    ret = { 'name': name, 'changes': {}, 'result': True, 'comment': 'value check pass'}
    if rule is None:
        if not name:
            ret['result'] = False
            ret['comment'] = 'value not match'
    else:
        iflag = re.IGNORECASE if ignorecase else 0
        dflag = re.DOTALL if dotall else 0
        flags = iflag | dflag
        if not re.match(rule, name, flags=flags):
            ret['result'] = False
            ret['comment'] = 'value not match'
    return ret
