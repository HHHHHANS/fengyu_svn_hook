# coding=utf-8
"""
svn命令的输出单元测试
"""

import mock
import unittest
from new.svn_config import Svn_Cmd
from new.svn_config import Cmd
from new.svn_config import CMDStringDangerousError, CMDOutputNotIllegalError


class Test_Svn_Cmd(unittest.TestCase):

    def __init__(self):
        super(Test_Svn_Cmd, self).__init__()
        self.svn_cmd = Svn_Cmd()

    def test_make_dirs_change_cmd_not_safe(self):
        """模拟进行dirschange命令时候发现命令不安全,得到空的命令输出"""
        cmd = Cmd()
        cmd.cmd_is_checked = mock.Mock(return_value=False)
        cmd_output = self.svn_cmd.make_dirs_change(repo='/mock', txn=123456)
        self.assertEqual(cmd_output, None)

    def test_make_dirs_change_cmd_is_safe_output_not_safe(self):
        """模拟进行dirschange命令命令本身正确，但命令输出错误,得到空的命令输出"""
        cmd = Cmd()
        cmd.cmd_is_checked = mock.Mock(return_value=True)
        cmd.output_is_checked = mock.Mock(return_value=False)
        cmd_output = self.svn_cmd.make_dirs_change(repo='/mock', txn=123456)
        self.assertEqual(cmd_output, None)

    def test_make_dirs_change_not_safe(self):
        """模拟获取日志语句时候指令本身和输出均正确，获取预期输出"""
        cmd = Cmd()
        cmd.cmd_is_checked = mock.Mock(return_value=False)
        cmd.output_is_checked = mock.Mock(return_value=True)
        cmd.output = mock.Mock(return_value='test_output')
        cmd_output = self.svn_cmd.make_dirs_change(repo='/mock', txn=123456)
        self.assertEqual(cmd_output, 'test_output')

    def test_get_log_str_cmd_not_safe(self):
        """模拟获取日志语句命令时候发现命令不安全,得到空的命令输出"""
        cmd = Cmd()
        cmd.cmd_is_checked = mock.Mock(return_value=False)
        cmd_output = self.svn_cmd.get_log_str(repo='/mock', txn=123456)
        self.assertEqual(cmd_output, None)

    def test_get_log_str_cmd_is_safe_output_not_safe(self):
        """模拟获取日志语句命令本身正确，但命令输出错误,得到空的命令输出"""
        cmd = Cmd()
        cmd.cmd_is_checked = mock.Mock(return_value=True)
        cmd.output_is_checked = mock.Mock(return_value=False)
        cmd_output = self.svn_cmd.get_log_str(repo='/mock', txn=123456)
        self.assertEqual(cmd_output, None)

    def test_get_log_str_not_safe(self):
        """模拟获取日志语句时候指令本身和输出均正确，获取预期输出"""
        cmd = Cmd()
        cmd.cmd_is_checked = mock.Mock(return_value=False)
        cmd.output_is_checked = mock.Mock(return_value=True)
        cmd.output = mock.Mock(return_value='test_output')
        cmd_output = self.svn_cmd.get_log_str(repo='/mock', txn=123456)
        self.assertEqual(cmd_output, 'test_output')


if __name__ == '__main__':
    unittest.main()