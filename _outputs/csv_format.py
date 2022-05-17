#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
csv output
=====================

csv output for grains or pillars format as csv
Example:

    .. code-block:: bash

        salt '*' grains.item os id dnsnameservers --hide-timeout --output=raw | /srv/salt/_output/csv_format.py

        salt-call grains.item os id dnsnameservers --output=csv
"""
from __future__ import absolute_import
from collections import Iterable
import sys

__virtualname__ = 'csv'


def __virtual__():
    return __virtualname__


def _parse_data(rawdata):
    columns = []
    data = []

    def _check_merge(l):
        for i in l:
            if isinstance(i, (str, unicode)):
                continue
            elif isinstance(i, Iterable):
                return False
        return True

    def worker(d, column=''):
        if isinstance(d, dict):
            for k in d.keys():
                if column:
                    col = ':'.join([column, k])
                else:
                    col = k
                worker(d[k], col)
        elif isinstance(d, list):
            if _check_merge(d):
                v = '|'.join([str(x) for x in d])
                columns.append(column)
                data.append(v)
            else:
                for i, j in enumerate(d):
                    if column:
                        col = ':'.join([column, str(i)])
                    else:
                        col = str(i)
                    worker(j, col)
        else:
            columns.append(column)
            data.append(str(d))

    worker(rawdata)
    return dict(zip(columns, data))


def output(data, **kwargs):
    """
    Output the data in csv format
    """
    ret = ''
    columns = set()
    nodes = []
    for k in data:
        sub = _parse_data(data[k])
        columns |= set(sub.keys())
        sub['saltminion_id'] = k
        nodes.append(sub)
    header = list(columns)
    header.insert(0, 'saltminion_id')
    ret += ','.join(header) + '\n'
    for node in nodes:
        line = ','.join([node.get(x, 'Null') for x in header]) + '\n'
        ret += line
    return ret


def main():
    raw = sys.stdin
    ret = ''
    columns = set()
    nodes = []
    for l in raw:
        try:
            data = eval(l.strip())
        except:
            continue
        for k in data:
            sub = _parse_data(data[k])
            columns |= set(sub.keys())
            sub['saltminion_id'] = k
            nodes.append(sub)
    header = list(columns)
    header.insert(0, 'saltminion_id')
    ret += ','.join(header) + '\n'
    for node in nodes:
        line = ','.join([node.get(x, 'Null') for x in header]) + '\n'
        ret += line
    print(ret)


if __name__ == "__main__":
    main()
