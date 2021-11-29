# coding=utf-8
# 用于获取线上或构造测试环境的repo仓库地址、txn上下文数字信息、配置文件路径等信息模块
import sys
from new.common import CODEREVIEW_SVN_CONF_FILE


def get_test_input():
    """ TODO 构造测试用的仓库地址repos和上下文数字txn"""
    repos = '/'
    txn = 1
    return repos, txn


def get_online_input():
    """ 获取程序启动参数: 线上环境的仓库地址、上下文数字txn"""
    repos = sys.argv[1]
    txn = sys.argv[2]
    return repos, txn


def get_input(env):
    """根据主程序/配置文件中的环境标示来获取不同仓库地址repos和上下文txn"""
    # 测试环境信息
    if env == 'test':
        return get_test_input()
    # 线上环境信息
    elif env == 'online':
        return get_online_input()
    # 输入错误则报错
    else:
        raise ValueError('unrecognized env str')


def mock_test_config_path():
    """测试环境下的配置文件路径"""

    return '/mock_info/config.json'


def online_config_path():
    """获取线上环境的配置文件路径"""

    return CODEREVIEW_SVN_CONF_FILE


def get_code_view_config_path(env):
    """根据主程序/配置文件中的环境标示来获取不同配置文件路径"""
    # 测试环境
    if env == 'text':
        return mock_test_config_path()
    elif env == 'online':
        return online_config_path()
    else:
        raise ValueError('unrecognized env str')