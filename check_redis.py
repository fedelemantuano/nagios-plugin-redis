#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import redis
import sys

VERSION = 0.1


def is_number(x):
    return isinstance(x, (int, long, float, complex))


def check_status(
    value,
    message,
    only_graph=False,
    critical=None,
    warning=None,
    ok=None,
):
    if only_graph:
        print("{}".format(message))
        sys.exit(0)

    if (is_number(value) and is_number(critical) and is_number(warning)):
        if value >= critical:
            print("CRITICAL - {}".format(message))
            sys.exit(2)
        elif value >= warning:
            print("WARNING - {}".format(message))
            sys.exit(1)
        else:
            print("OK - {}".format(message))
            sys.exit(0)
    else:
        if value in critical:
            print("CRITICAL - {}".format(message))
            sys.exit(2)
        elif value in warning:
            print("WARNING - {}".format(message))
            sys.exit(1)
        elif value in ok:
            print("OK - {}".format(message))
            sys.exit(0)
        else:
            print("UNKNOWN - Unexpected value: {}".format(value))
            sys.exit(3)


def parser_command_line():
    parser = argparse.ArgumentParser(
        description='Redis Nagios checks',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Common args
    parser.add_argument(
        '-H',
        '--host',
        default='localhost',
        help='Server hostname',
        dest='host',
    )

    parser.add_argument(
        '-P',
        '--port',
        default='6379',
        help='Server port',
        dest='port',
    )

    parser.add_argument(
        '-d',
        '--db',
        default='0',
        help='Database number',
        dest='db',
    )

    parser.add_argument(
        '-D',
        '--perf-data',
        action='store_true',
        help='Enable Nagios performance data',
        dest='perf_data',
    )

    parser.add_argument(
        '-G',
        '--only-graph',
        action='store_true',
        help='Enable Nagios to print only message',
        dest='only_graph',
    )

    parser.add_argument(
        '-C',
        '--critical',
        default=None,
        help='Critical threshold',
        dest='critical',
    )

    parser.add_argument(
        '-W',
        '--warning',
        default=None,
        help='Warning threshold',
        dest='warning',
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {}'.format(VERSION)
    )

    parser.add_argument(
        '--queue-list',
        action='store_true',
        help='Check number messagges in queue list',
        dest='queue_list',
    )

    parser.add_argument(
        '--list',
        default=None,
        help='List name',
        dest='_list',
    )

    return parser.parse_args()


def check_queue_list(
    result,
    _list,
    perf_data=None,
    only_graph=False,
    critical=None,
    warning=None,
):
    critical = critical or 50
    warning = warning or 25
    message = 'The queue for list {} is {}'.format(_list, result)
    if perf_data:
        message += " | queue={}".format(result)
    check_status(
        result,
        message,
        only_graph,
        critical,
        warning,
    )


if __name__ == '__main__':
    args = parser_command_line()

    host = args.host
    port = args.port
    db = args.db

    r = redis.StrictRedis(
        host=host,
        port=port,
        db=db,
    )

    if args.queue_list:
        _list = args._list
        if not _list:
            print("Error! Enter the list name.")
            sys.exit(3)
        result = r.llen(_list)
        check_queue_list(
            result,
            _list,
            args.perf_data,
            args.only_graph,
            int(args.critical) if args.critical else None,
            int(args.warning) if args.warning else None,
        )
