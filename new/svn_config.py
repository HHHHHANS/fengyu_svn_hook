# coding=utf-8

"""本模块为SVN日志匹配规则配置模块
包括
"""

import ConfigParser
import StringIO
from new.common import capture_output
from new.common import make_svnlook_cmd
from new.common import Logger


class Cmd:
    """命令类

    接收一个字符串，对内容进行安全性检查，输出其作为指令的输出内容
    """
    def __init__(self, cmd):
        try:
            # 指令本身安全检查
            self.cmd_safety(cmd)
            output = capture_output(cmd)
            # 指令输出内容安全检查
            if not self.output_safety(output):
                raise IOError('unsafe cmd output')
            self._output = output
        except Exception as e:
            raise e

    def output(self):
        return self._output

    @staticmethod
    def cmd_safety(cmd):
        # TODO 指令本身安全性检查；高危操作、指令类型、指令有效性检查
        # raise 指令错误
        pass

    @staticmethod
    def output_safety(output):
        # TODO 指令输出安全检查；内容大小、敏感信息等检查
        # raise 指令输出错误
        pass


class SvnFp:
    """SvnFp类
    接收一个命令输出类，转化为一个fp类
    """
    def __init__(self, directive, repo, txn, file_=None):
        # 构造svn命令并获取输出
        try:
            self._cmd_output = Cmd(make_svnlook_cmd(directive=directive,
                                                    repos=repo,
                                                    txn=txn,
                                                    file_=file_))
        except Exception as e:
            raise e
        self._fp = StringIO.StringIO(self._cmd_output.output())

    def fp(self):
        return self._fp


class SVNConfig(ConfigParser.ConfigParser):
    """svn配置文件类
    继承自ConfigParser.ConfigParser()配置文件标准类，享受所有标准库的方法
    接收一个SVN_fp类,默认
    """
    def __init__(self, repo, txn, directive='cat', file_=None):
        super(SVNConfig, self).__init__()
        try:
            self._svn_fp = SvnFp(directive=directive, repo=repo, txn=txn, file_=file_)
        except Exception as e:
            raise e
        self.readfp(self._svn_fp.fp())

    def is_logcheck_enable(self):
        """检查配置文件是否启用了日志检查"""
        try:
            enable = self.getboolean('admin', 'enable_logcheck')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            enable = False
        return enable

    def rules(self):
        """读取配置文件中的规则并返回"""
        rules = {}
        for section in self.sections():
            if section.startswith('/'):
                rules['%s/' % section.strip('/')] = section
        return rules


