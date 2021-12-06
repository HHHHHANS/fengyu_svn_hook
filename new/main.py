# coding=utf-8
import sys
from new.common import debug
from new.information import Input
from new.svn_config import SVNConfig, Svn_Cmd
from new.svn_rules import SVNLogRules


def run():
    # 获取输入：包括仓库地址repos、上下文数字txn
    # env = 'online'为线上环境输入; env = 'test' 为获取测试环境输入
    env = 'test'
    try:
        repos, txn = Input.get_input(env=env)
    except Exception as e:
        debug(e)
        sys.exit(1)

    # 获取测试环境的配置文件路径
    test_cfg_path = Input.get_code_view_config_path(env=env)

    # svn日志配置信息，包含变量和规则的预定义
    try:
        svn_config = SVNConfig(repo=repos, txn=txn, directive=test_cfg_path)
        # 检查是否启用了日志检查功能，未启动则推出程序
        if not svn_config.is_logcheck_enable():
            debug('log check is not enabled')
            sys.exit(1)
    except Exception as e:
        debug(e)
        sys.exit(1)

    # 已启用日志检查
    debug('========== LOGCHECK ENABLED ==========')

    # 获取配置文件中规则，并初始化为规则管理类
    rules = SVNLogRules(svn_config.rules())

    #
    sp_rule = rules.select_one_rule(repo=repos, txn=txn)
    if not sp_rule:
        debug('not rule found.')
        sys.exit(1)

    debug('select rule: %s' % sp_rule)
    # 获取特定section下的配置信息
    args = svn_config.extract_args_from_config(sp_rule)
    debug('repository options: %s' % args)
    # 检查是否在该section下启用日志检查规则
    if not svn_config.is_logcheck_enable(args=args):
        debug('{}\'s log check is not enabled'.format(sp_rule))
        sys.exit(1)

    log_str = Svn_Cmd.get_log_str(repo=repos, txn=txn)
    log_rules = SVNConfig.log_rules_in_section(args=args)

    try:
        rules.check_log_is_ok(log_str=log_str, log_rules=log_rules)
    except Exception as e:
        debug(e)
        sys.exit(1)


# class Svn_Log_Checker:
#
#     def __init__(self):
#         self._repos = None
#         self._txn = None
#
#     def get_repo_and_txn(self):
#         """ 获取程序启动参数: 线上环境的仓库地址、上下文数字txn"""
#         repos = sys.argv[1]
#         txn = sys.argv[2]
#         return repos, txn


if __name__ == '__main__':
    # 程序启动
    run()