Introduction — what this script is and what it does (English, detailed)

This documentation describes the Python script shell2.py 
.

shell2.py implements a small interactive command-line shell (a REPL) called IndependentShell using Python’s built-in cmd module. Its goal is to provide a tiny, extendable command prompt with a handful of utility commands (open a URL, show time, show system info, reboot/shutdown the host, etc.). On Windows the script re-launches itself in a new console window so the shell runs in a separate window; on other platforms it runs inline.

Key design points and components

cmd.Cmd based shell — Uses class IndependentShell(cmd.Cmd) which gives you do_ methods to define commands, a prompt string, and an intro message.

Built-in commands — Implemented commands:

open <url>: open a URL in the system default browser (adds http:// if protocol is missing).

shutdown: attempt to power off the machine.

reboot: attempt to reboot the machine.

time: print current system time.

sysinfo: print OS, version, platform, and processor information.

exit: exit the shell (returns from the cmdloop).

Cross-platform checks — Uses platform.system() and os.name to select platform-specific shutdown/reboot commands and console behavior.

Separate console on Windows — If running on Windows (os.name == 'nt') and the environment variable INDEPENDENT_SHELL is not set, the script sets that env var and re-launches itself with subprocess.Popen(..., creationflags=subprocess.CREATE_NEW_CONSOLE, env=env) so the user gets a new console window. The original process then exits. This is intended to make the shell "pop out" into its own window.

Only standard library — The script uses only Python standard library modules (os, sys, subprocess, cmd, platform, time, webbrowser) so no extra packages are required.

Security & safety notes (very important)

The shutdown and reboot commands call system shutdown commands directly (shutdown /s /t 1, shutdown now, reboot). These will actually power off or reboot the machine when they succeed. On many systems these require elevated privileges (Administrator on Windows, root or sudo on Linux/macOS). Do not run this script on a machine you cannot or should not reboot/shutdown.

For safe testing, either comment out or replace the shutdown/reboot behavior with a no-op (see the “Safe testing” section below).

Because it opens URLs using the system default browser, be careful not to supply malicious or untrusted URLs.

How to use shell2.py — detailed, step-by-step (English)

Below are step-by-step instructions for installing, running, controlling and customizing the script.

Requirements

Python 3.x installed (the script has a #!/usr/bin/env python3 shebang and uses Python 3 APIs).

No third-party packages needed — only the Python standard library.

Starting the shell

Open a terminal / console and run:

On Linux/macOS:

python3 shell2.py


On Windows (regular command prompt):

python shell2.py


Windows special behavior: By default, when you run it on Windows, the script will re-launch itself into a new console window and the original process will exit. This happens because the script sets the environment variable INDEPENDENT_SHELL=1 and uses subprocess.Popen(..., creationflags=subprocess.CREATE_NEW_CONSOLE, env=env) to spawn a new console. If you prefer to run without spawning a new console, start Python with INDEPENDENT_SHELL already set (so the script will not re-launch):

Windows CMD:

set INDEPENDENT_SHELL=1
python shell2.py


Windows PowerShell:

$env:INDEPENDENT_SHELL = '1'
python shell2.py


Linux/macOS (if you need to force the same env behavior):

export INDEPENDENT_SHELL=1
python3 shell2.py

Interacting with the shell — commands and examples

When the shell starts you will see the intro message (in Chinese in the provided file) and the prompt:

ish>


Available commands (use help inside the shell for short descriptions):

open <url>

Purpose: Open a website in your default browser.

Behavior: If the URL does not start with http:// or https://, the script prefixes it with http://.

Examples:

open baidu.com → opens http://baidu.com

open https://example.com/path → opens exactly that URL

Expected terminal output: "[OPEN] 打开 http://baidu.com" (the script prints a confirmation message).

time

Purpose: Print the current system time.

Example:

time

Example output:

当前时间： 2025-08-14 11:23:45

sysinfo

Purpose: Print basic system information (platform.system(), platform.version(), platform.platform(), platform.processor()).

Example:

sysinfo

Example output (varies by system):

系统: Windows
版本: ...
平台: ...
处理器: Intel64 Family 6 Model ...


shutdown

Purpose: Immediately attempt to shut down the computer.

Warning: This will trigger an actual shutdown command. Requires privileges; use with extreme caution.

Example:

shutdown → on Windows runs shutdown /s /t 1; on Linux/macOS runs shutdown now.

reboot

Purpose: Attempt to reboot the computer.

Example:

reboot → on Windows runs shutdown /r /t 1; on Linux/macOS runs reboot.

Warning: same cautions & privilege requirements as shutdown.

exit

Purpose: Exit the interactive shell.

Example:

exit

The command returns True from do_exit, which ends the cmdloop().

Example session
$ python3 shell2.py
欢迎进入独立弹出窗口的命令 Shell！输入 help 查看可用命令。
ish> time
当前时间： 2025-08-14 11:30:12
ish> open example.com
[OPEN] 打开 http://example.com
ish> sysinfo
系统: Linux
版本: #59-Ubuntu SMP ...
平台: Linux-5.15.0-...
处理器: x86_64
ish> exit
再见！
$

Running with required privileges

On Windows, shutdown / reboot typically require Administrator rights. To run with those rights, open Command Prompt or PowerShell as Administrator and then start python shell2.py.

On Linux/macOS, shutdown now or reboot normally requires root. You can run the script with sudo:

sudo python3 shell2.py


or configure sudoers to allow the current user to run shutdown/reboot without a password (be careful — security implications).

Safe testing and disabling destructive commands

If you want to test without risking a shutdown/reboot, do one of the following:

Modify the script: Replace os.system("shutdown now") and os.system("reboot") with print("Would shut down now (disabled for testing).") or os.system("echo shutdown simulated").

Comment out those methods entirely or change their bodies to warnings.

Run in a virtual machine or disposable environment where shutdowns are safe.

Add a confirmation prompt before executing shutdown/reboot. Example replacement for do_shutdown:

def do_shutdown(self, arg):
    answer = input("Are you sure you want to shutdown the machine? (yes/no): ").strip().lower()
    if answer != 'yes':
        print("Shutdown cancelled.")
        return
    # proceed with platform-specific shutdown...

How to customize / extend

This script is intentionally small and easy to extend.

Add a command: create a new method do_<commandname>(self, arg): and add a docstring. Example:

def do_echo(self, arg):
    """echo <text> : print text back to the console"""
    print(arg)


Change prompt: set prompt = "my-prompt> " inside the IndependentShell class.

Localize messages: The file contains Chinese strings (intro, confirmations). Replace strings with English or another language as needed.

Add tab completion / arg parsing: Use cmd’s complete_<command> methods or integrate argparse inside command methods for richer parsing.

Logging: Add Python logging calls inside command methods to keep an activity log.

Troubleshooting

creationflags not defined on non-Windows — code only calls that branch on Windows. If you copy the Windows subprocess call to other platforms, it will fail; leave the platform check as-is.

webbrowser.open() does not open a browser — some headless or minimal systems may lack a GUI browser or proper DISPLAY/desktop environment. On such systems, open won't work as expected.

shutdown/reboot fail with permission denied — run as Administrator/root or use sudo.

Script immediately exits on Windows — check whether you started it from a console that closes on child launch. The script deliberately re-launches itself and the original process exits; look for a new console window.

Quick reference — commands summary

open <url> — open URL in default browser (adds http:// if missing).

time — print current time.

sysinfo — print OS and processor info.

shutdown — shut down the machine (dangerous).

reboot — reboot the machine (dangerous).

exit — exit the shell.
