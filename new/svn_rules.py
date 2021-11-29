# coding=utf-8
# 本文件为管理svn日志格式的规则类


class SVNLogRules:

    def __init__(self, rules):
        self._rules = rules

    def select_one_rule(self, repo, txn):
        pass