'''
for common use
'''
#author: thuhak.zhou@nio.com

def wrap(name, changes=None, result=True, comment=''):
    '''
    provide a state interface
    '''
    if changes is None:
        changes = dict()
    ret = {'name': name,
           'changes': changes,
           'result': result,
           'comment': comment
            }
    return ret


def execution(name, **kwargs):
    '''
    transfer execution module to state module
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    try:
        result = __salt__[name](**kwargs)
        ret['result'] = result
        ret['comment'] = 'job success'
    except TypeError as e:
        ret['result'] = False
        ret['comment'] = str(e)
    except KeyError:
        ret['result'] = False
        ret['comment'] = 'module or function not valid'
    except Exception as e:
        ret['result'] = False
        ret['comment'] = 'job failed'
    return ret
