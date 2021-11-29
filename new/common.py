# coding=utf-8

import os


class SvnError(StandardError):
    """svn错误"""
    pass


DEBUG = False
DEBUG_FILE = '/tmp/svn-hooks-logcheck.log'

if DEBUG:
    def debug(s):
        f = open(DEBUG_FILE, 'a')
        try:
            f.write('%s\n' % s)
        finally:
            f.close()
else:
    def debug(s):
        pass


def capture_output(cmd):
    '''执行一个命令并且获取命令执行结果'''
    cmd = ' '.join(cmd)
    debug('cmd: %s' % cmd)
    output = os.popen(cmd).read()
    debug('cmd output:\n%s' % output)
    return output
