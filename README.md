# Redis Nagios Checks

## Overview

This is a simple Nagios check script to monitor Redis server

## Authors

### Main Author
 Fedele Mantuano (**Twitter**: [@fedelemantuano](https://twitter.com/fedelemantuano))


## Installation

In your Nagios plugins directory run

<pre><code>git clone https://github.com/fedelemantuano/nagios-plugin-redis.git</code></pre>


## Help

### check_redis.py

```
usage: check_redis.py [-h] [-H HOST] [-P PORT] [-d DB] [-D] [-G] [-C CRITICAL]
                      [-W WARNING] [-v] [--queue-list] [--list _LIST]

Redis Nagios checks

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Server hostname (default: localhost)
  -P PORT, --port PORT  Server port (default: 6379)
  -d DB, --db DB        Database number (default: 0)
  -D, --perf-data       Enable Nagios performance data (default: False)
  -G, --only-graph      Enable Nagios to print only message (default: False)
  -C CRITICAL, --critical CRITICAL
                        Critical threshold (default: None)
  -W WARNING, --warning WARNING
                        Warning threshold (default: None)
  -v, --version         show program's version number and exit
  --queue-list          Check number messagges in queue list (default: False)
  --list _LIST          List name (default: None)

```
