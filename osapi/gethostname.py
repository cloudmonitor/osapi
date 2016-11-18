#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import socket

def gethostname():
    sys = os.name
    if sys == 'nt':
        hostname = os.getenv('computername')
        return hostname
    elif sys == 'posix':
        host = os.popen('hostname')
        try:
            hostname = host.read().replace('\n', '')
            return hostname
        finally:
            host.close()
    else:
        return 'Unkwon hostname'


if __name__ == '__main__':
    print gethostname()
    print socket.gethostname()