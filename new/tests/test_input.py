# coding=utf-8
"""
svn项目中input模块的单元测试
"""


import mock
import unittest
from new.information import Input


class Test_Input(unittest.TestCase):
    """测试代码仓库地址和上下文数字的输入类"""
    def __init__(self):
        super(Test_Input, self).__init__()
        self.input = Input()

    def test_input_succeed(self):
        # 模拟线上环境的输入成功的情景
        self.input.get_online_input = mock.Mock(return_value=('/online_repo', 123456))
        result = self.input.get_input(env='online')
        # 验证测试结果是否与预期一致
        self.assertEqual(('/online_repo', 123456), result)

    def test_offline(self):
        # 模拟测试环境下的输入
        self.input.get_test_input = mock.Mock(return_value=('/test_repo', 234567))
        result = self.input.get_test_input(env='test')
        # 验证测试结果是否与预期一致
        self.assertEqual(('/test_repo', 123456), result)


if __name__ == '__main__':
    unittest.main()

