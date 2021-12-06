# coding=utf-8
# 本文件为管理svn日志格式的规则类
from new.svn_config import Svn_Cmd
from new.common import SvnError
import re


class SVNLogRules:
    """svn配置文件规则模块
    负责日志格式规则相关的处理
    """
    def __init__(self, rules):
        self._rules = rules

    def select_one_rule(self, repo, txn):
        """选取特定规则"""
        self._rules.sort(reverse=True)
        dirs = Svn_Cmd.make_dirs_change(repo=repo, txn=txn)
        for dir_ in dirs:
            rule = self.select_longest_rule(dir_, self._rules)
            if rule:
                return self._rules[rule]
        return None

    @staticmethod
    def select_longest_rule(dir_, rules_):
        """选取最长规则"""
        for rule_ in rules_:
            if dir_.startswith(rule_):
                return rule_
        return None

    @staticmethod
    def check_log_is_ok(log_str, log_rules):
        """检查日志语句与对应的配置文件中定义的规则是否一致
        一致的正常返回
        不一致则返回错误，并打印提示语句
        """
        for log_rule in log_rules:
            if not log_rule.has_key('expr'):
                continue
            expr = log_rule['expr']
            tip = log_rule['tip']
            m = re.search(expr, log_str)
            if not m:
                raise SvnError(tip)
