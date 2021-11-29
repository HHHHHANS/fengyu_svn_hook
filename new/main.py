# coding=utf-8
import sys
from common import debug
from information import get_input
from information import get_code_view_config_path
from svn_config import SVNConfig
from svn_rules import SVNLogRules

def run():
    # 获取输入：包括仓库地址repos、上下文数字txn
    # env = 'online'为线上环境输入; env = 'test' 为获取测试环境输入
    env = 'test'
    try:
        repos, txn = get_input(env=env)
    except Exception as e:
        debug(e)
        sys.exit(1)

    # 获取测试环境的配置文件路径
    test_cfg_path = get_code_view_config_path(env=env)

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





if __name__ == '__main__':
    run()