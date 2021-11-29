# coding=utf-8
import sys
from common import debug


def get_test_input():
    """ todo 测试环境中，获取仓库地址repos和上下文数字txn"""
    repos = '/'
    txn = 1
    return repos, txn


def get_online_input():
    """ 获取线上环境的仓库地址和上下文数字txn"""
    repos = sys.argv[1]
    txn = sys.argv[2]
    return repos, txn


def get_input(env='test'):
    """根据主程序/配置文件中的环境标示来获取不同仓库地址repos和上下文txn"""
    if env == 'test':
        return get_test_input()
    elif env == 'online':
        return get_online_input()
    else:
        raise ValueError('unrecognized env str')


def _main():
    # 获取输入：包括仓库地址repos、上下文数字txn
    try:
        repos, txn = get_input('test')
    except Exception as e:
        debug(e)
        sys.exit(1)


