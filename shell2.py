#!/usr/bin/env python3
# independent_shell.py

import os
import sys
import subprocess
import cmd
import platform
import time
import webbrowser

class IndependentShell(cmd.Cmd):
    intro = "\n欢迎进入独立弹出窗口的命令 Shell！输入 help 查看可用命令。"
    prompt = "ish> "

    def do_open(self, arg):
        """open <网址> : 打开一个网址"""
        if not arg.strip():
            print("请提供一个网址，例如 open baidu.com")
            return
        url = arg.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        webbrowser.open(url)
        print(f"[OPEN] 打开 {url}")

    def do_shutdown(self, arg):
        """shutdown : 关闭计算机"""
        sys_platform = platform.system()
        if sys_platform == "Windows":
            os.system("shutdown /s /t 1")
        elif sys_platform == "Linux" or sys_platform == "Darwin":
            os.system("shutdown now")
        else:
            print("不支持的操作系统")

    def do_reboot(self, arg):
        """reboot : 重启计算机"""
        sys_platform = platform.system()
        if sys_platform == "Windows":
            os.system("shutdown /r /t 1")
        elif sys_platform == "Linux" or sys_platform == "Darwin":
            os.system("reboot")
        else:
            print("不支持的操作系统")

    def do_exit(self, arg):
        """exit : 退出 Shell"""
        print("再见！")
        return True

    def do_time(self, arg):
        """time : 显示当前系统时间"""
        print("当前时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def do_sysinfo(self, arg):
        """sysinfo : 显示系统信息"""
        print("系统:", platform.system())
        print("版本:", platform.version())
        print("平台:", platform.platform())
        print("处理器:", platform.processor())

if __name__ == "__main__":
    if os.name == 'nt' and not os.environ.get('INDEPENDENT_SHELL'): 
        os.environ['INDEPENDENT_SHELL'] = '1'
        subprocess.Popen(
            [sys.executable] + sys.argv,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            env=os.environ
        )
        sys.exit(0)
    IndependentShell().cmdloop()
