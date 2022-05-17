import os
import json
import yaml


def _json_load(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def _json_dump(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, ident=True).replace('\\\\', '\\')

def _yaml_load(filename):
    with open(filename) as f:
        d = f.read()
    data = yaml.load(d, Loader=yaml.SafeLoader)
    return data

def _yaml_dump(filename, data):
    data = json.loads(json.dumps(data).replace('\\\\', '\\'))
    with open(filename, 'w') as f:
        data = yaml.dump(data, f, Dumper=yaml.SafeDumper, default_flow_style=False)


def dump(name, data, key=None, format='yaml'):
    """
    dump data to
    """
    if key:
        data = {key: data}
    ret = {'name': name, 'result': True, 'comment': '', 'changes': {}}
    if format == 'json':
        loader = _json_load
        dumper = _json_dump
    elif format == 'yaml':
        loader = _yaml_load
        dumper = _yaml_dump
    else:
        ret = {'result': False, 'comment': 'format only in json or yaml'}
        return ret
    if os.path.isfile(name):
        olddata = loader(name)
        if olddata == data:
            return ret
    dumper(name, data)
    ret['changes'] = {'data': data}

    return ret
