# coding=utf-8
"""
SVN hook 公共类
"""

import os
import logging

Logger = logging


class SvnError(StandardError):
    """svn错误类"""
    pass


CODEREVIEW_SVN_DIR = '/_codereview'
CODEREVIEW_SVN_CONF_FILE = '%s/codereview.ini' % CODEREVIEW_SVN_DIR
DATA_DIR = os.path.abspath(os.path.dirname(__file__))
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
    """
    执行一个命令并且获取命令执行结果
    """
    cmd = ' '.join(cmd)
    debug('cmd: %s' % cmd)
    output = os.popen(cmd).read()
    debug('cmd output:\n%s' % output)
    return output


def make_svnlook_cmd(directive, repos, txn, file_=None):
    """
    构造一个svnlook命令，将原项目中的两个命令合并
    """
    svnlook_cmd = ['svnlook', directive, '-t', txn, repos]
    if file_ is not None:
        svnlook_cmd.append(file_)
    return svnlook_cmd