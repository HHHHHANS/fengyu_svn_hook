#!/usr/bin/env python
# coding=utf-8

import base64
import cookielib
import ConfigParser
import os
import re
import sys
import shelve
import StringIO
import urllib2
import urlparse

try:
    import json
except ImportError:
    import simplejson as json

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


class SvnError(StandardError):
    pass


def capture_output(cmd):
    cmd = ' '.join(cmd)
    debug('cmd: %s' % cmd)
    output = os.popen(cmd).read()
    debug('cmd output:\n%s' % output)
    return output


def make_svnlook_cmd(directive, repos, txn):
    """

    :param directive:
    :param repos:
    :param txn:
    :return:
    """
    svnlook_cmd = ['svnlook', directive, '-t', txn, repos]
    return svnlook_cmd


def make_svnlook_cmd_2(directive, repos, file_, txn):
    """

    :param directive:
    :param repos:
    :param file_:
    :param txn:
    :return:
    """
    svnlook_cmd = ['svnlook', directive, '-t', txn, repos, file_]
    return svnlook_cmd


def select_rule(repos, txn, rules):
    rules.sort(reverse=True)

    def select_longest_rule(dir_, rules_=rules[:]):
        for rule_ in rules_:
            if dir_.startswith(rule_):
                return rule_
        return None

    cmd = make_svnlook_cmd('dirs-changed', repos, txn)
    dirs = capture_output(cmd).split('\n')
    for dir_ in dirs:
        rule = select_longest_rule(dir_)
        if rule:
            return rule
    return None


def extract_args_from_config(config, section):
    args = {}

    def extract_args_boolean(sec, opt, cfg_=config, args_=args):
        if cfg_.has_option(sec, opt):
            args_[opt] = cfg_.getboolean(sec, opt)

    def extract_args_log(sec, cfg_=config, args_=args):
        extract_args_boolean(sec, 'enable_logcheck')
        if not cfg_.has_option(sec, 'log_expr_num'):
            return
        args_['log_rules'] = []
        rules = args_['log_rules']
        num = config.get_int(sec, 'log_expr_num')
        for i in range(i, num):
            rule = {}
            title = ('log_expr_%s' % i)
            if cfg_.has_option(sec, title):
                log_rule['expr'] = str(cfg_.get(sec, title))
            title = ('log_tip_%s' % i)
            if cfg_.has_option(sec, title):
                log_rule['tip'] = str(cfg_.get(sec, title))
            rules[i] = rule

    args['enable_logcheck'] = False
    args['log_rules'] = []

    if config.has_section('general'):
        extract_args_log('general')

    extract_args_log(section)

    return args


def _main():
    # 实际程序入口

    # 获取程序启动参数
    repos = sys.argv[1]
    txn = sys.argv[2]

    cmd = make_svnlook_cmd_2('cat', repos, CODEREVIEW_SVN_CONF_FILE, txn)
    config = ConfigParser.ConfigParser()
    config.readfp(StringIO.StringIO(capture_output(cmd)))

    try:
        enable_logcheck = config.getboolean('admin', 'enable_logcheck')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        enable_logcheck = False
    if not enable_logcheck:
        return

    debug('========== LOGCHECK ENABLED ==========')

    rules = {}
    for section in config.sections():
        if section.startswith('/'):
            rules['%s/' % section.strip('/')] = section
    rule_key = select_rule(repos, txn, rules.keys())
    if not rule_key:
        return

    rule = rules[rule_key]
    debug('select rule: %s' % rule)
    args = extract_args_from_config(config, rule)
    debug('repository options: %s' % args)

    if not args['enable_logcheck']:
        return

    cmd = make_svnlook_cmd('log', repos, txn)
    log_str = capture_output(cmd)

    log_rules = args['log_rules']
    for log_rule in log_rules:
        if not log_rule.has_key('expr'):
            continue
        expr = log_rule['expr']
        tip = log_rule['tip']
        m = re.search(expr, log_str)
        if not m:
            raise SvnError(tip)


def main():
    # 程序入口
    try:
        _main()
    except SvnError, e:
        debug('SvnError: %s' % str(e))
        print >> sys.stderr, str(e)
        sys.exit(1)
    except Exception, e:
        debug('Exception: %s' % str(e))
        print >> sys.stderr, str(e)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
