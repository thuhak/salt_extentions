"""
decorators for salt runners
"""
# author: thuhak.zhou@nio.com
from functools import wraps, partial
from datetime import datetime
from copy import deepcopy
import salt.runner
import salt.config

opts = salt.config.master_config('/etc/salt/master')
queue = opts.get('runner_queue', {}).get('queue', None)


def pushback(func=None, queue=queue, delete_after=24):
    """
    push runner to queue if you set retry mark.

    Parameters:

        queue(str):  the salt queue backend, when you specify this parameter, you also need to config schedule task in salt master configuration to consume your queue.

        delete_after(int): how long this request will be keeped in queue, Unit: hour

    Usage:

    .. code-block:: python
        import sys
        if '/srv/libs' not in sys.path:
            sys.path.append('/srv/libs')
        from mydecorators import pushback

        @pushback
        def somerunner():
            ret = {'retry': True}
            return ret

        @pushback(queue='myqueue', delete_after=48)
        def somerunner():
            ret = {'retry': True}
            return ret
    """
    if func is None:
        return partial(pushback, queue=queue)
    func_name = func.__module__.split('.')[-1] + '.' + func.__name__
    queue = queue

    @wraps(func)
    def wrapper(*args, **kwargs):
        for k in kwargs.keys():
            if k.startswith('__pub_'):
                kwargs.pop(k)
        filterd_kw = deepcopy(kwargs)
        current_time = datetime.now()
        if '__pushback_requesttime' in kwargs:
            filterd_kw.pop('__pushback_requesttime')
            timedelta = (current_time - datetime.strptime(kwargs['__pushback_requesttime'],
                                                          '%Y%m%d%H%M')).total_seconds() / 3600
        else:
            kwargs['__pushback_requesttime'] = current_time.strftime('%Y%m%d%H%M')
            timedelta = 0
        ret = func(*args, **filterd_kw)
        try:
            condition = queue and ret['retry'] and timedelta < delete_after
            if condition:
                runner = salt.runner.RunnerClient(opts)
                kw = {'fun': func_name, 'queue': queue, 'args': args, 'kwargs': kwargs}
                runner.cmd('queue.insert_runner', kwarg=kw)
        except KeyError:
            pass
        return ret

    return wrapper
