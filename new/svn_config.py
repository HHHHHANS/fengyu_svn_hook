# coding=utf-8

"""本模块为SVN日志匹配规则配置模块
包括
"""

import ConfigParser
import StringIO
from new.common import capture_output


class Cmd:
    """命令类

    接收一个字符串，对内容进行安全性检查，输出其作为指令的输出内容
    """
    def __init__(self, cmd):
        try:
            # 指令安全检查
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
        pass

    @staticmethod
    def output_safety(output):
        # TODO 指令输出安全检查；内容大小、敏感信息等检查
        pass


class SvnFp:
    """SvnFp类
    接收一个命令输出类，转化为一个fp类
    """
    def __init__(self, cmd_output):
        if not isinstance(cmd_output, Cmd):
            raise TypeError(type(cmd_output))
        self._fp = StringIO.StringIO(cmd_output.output())

    def fp(self):
        return self._fp


class SVNConfig(ConfigParser.ConfigParser):
    """svn配置文件类
    继承自ConfigParser.ConfigParser()配置文件标准类，享受所有标准库的方法
    接收一个SVN_fp类,默认
    """
    def __init__(self, svn_fp):
        super(SVNConfig, self).__init__()
        if not isinstance(svn_fp, SvnFp):
            raise TypeError(type(svn_fp))
        self.readfp(svn_fp.fp())






