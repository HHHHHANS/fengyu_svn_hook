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

    def is_logcheck_enable(self, args=None):
        """检查配置文件是否启用了日志检查
        args为空的时候，默认检查admin下的enable_logcheck;
        args不为空的时候，检查args中的enable_logcheck
        """
        if not args:
            try:
                enable = self.getboolean('admin', 'enable_logcheck')
            except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
                enable = False
        else:
            enable = args.get('enable_logcheck', False)
        return enable

    def rules(self):
        """读取配置文件中的规则并返回"""
        rules = {}
        for section in self.sections():
            if section.startswith('/'):
                rules['%s/' % section.strip('/')] = section
        return rules

    def extract_args_from_config(self, rule_section):
        """获取某条规则的内容"""
        args = {}

        def extract_args_boolean(sec, opt, cfg_=self, args_=args):
            if cfg_.has_option(sec, opt):
                args_[opt] = cfg_.getboolean(sec, opt)

        def extract_args_log(sec, cfg_=self, args_=args):
            extract_args_boolean(sec, 'enable_logcheck')
            if not cfg_.has_option(sec, 'log_expr_num'):
                return
            args_['log_rules'] = []
            rules = args_['log_rules']
            num = cfg_.get_int(sec, 'log_expr_num')
            for i in range(1, num):
                rule = {}
                title = ('log_expr_%s' % i)
                if cfg_.has_option(sec, title):
                    rule['expr'] = str(cfg_.get(sec, title))
                title = ('log_tip_%s' % i)
                if cfg_.has_option(sec, title):
                    rule['tip'] = str(cfg_.get(sec, title))
                rules[i] = rule

        args['enable_logcheck'] = False
        args['log_rules'] = []

        if self.has_section('general'):
            extract_args_log('general')

        extract_args_log(rule_section)

        return args

    @staticmethod
    def log_rules_in_section(args):
        log_rules = args.get('log_rules', None)
        return log_rules


class Svn_Cmd:
    """管理、操作svn相关命令，并获取输出"""
    def __init__(self):
        pass

    @staticmethod
    def make_dirs_change(repo, txn):
        """执行dirs-changed命令"""
        svn_cmd = make_svnlook_cmd(directive='dirs-changed', repos=repo, txn=txn)
        cmd_inst = Cmd(svn_cmd)
        return cmd_inst.output()

    @staticmethod
    def get_log_str(repo, txn):
        """根据仓库地址和上下文数字，获取需要被检查的日志语句"""
        svm_cmd = make_svnlook_cmd(directive='log', repos=repo, txn=txn)
        cmd_inst = Cmd(svm_cmd)
        return cmd_inst.output()

