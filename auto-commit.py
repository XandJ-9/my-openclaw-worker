# -*- coding: utf-8 -*-
"""
自动提交脚本 - 定期检查并提交workspace变更
"""

import os
import subprocess
import time
from datetime import datetime
import sys

def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def get_git_status():
    """获取git状态"""
    returncode, stdout, stderr = run_command("git status --porcelain", cwd="C:/Users/18352/.openclaw/workspace")

    if returncode != 0:
        return False, f"Git error: {stderr}"

    if not stdout.strip():
        return False, "No changes detected"

    return True, stdout.strip()

def git_add_all():
    """添加所有变更到暂存区"""
    returncode, stdout, stderr = run_command("git add .", cwd="C:/Users/18352/.openclaw/workspace")
    return returncode == 0

def git_commit(message):
    """提交变更"""
    cmd = f'git commit -m "{message}"'
    returncode, stdout, stderr = run_command(cmd, cwd="C:/Users/18352/.openclaw/workspace")
    return returncode == 0

def git_push():
    """推送到远程"""
    returncode, stdout, stderr = run_command("git push", cwd="C:/Users/18352/.openclaw/workspace")
    return returncode == 0

def main():
    print("=" * 60)
    print("自动提交脚本启动")
    print("=" * 60)

    # 检查是否有变更
    has_changes, status_msg = get_git_status()

    if not has_changes:
        print(f"[INFO] {status_msg}")
        print("[INFO] 没有需要提交的变更")
        return 0

    print(f"\n[INFO] 检测到变更:")
    print(status_msg)
    print()

    # 添加所有变更
    print("[INFO] 正在添加变更到暂存区...")
    if git_add_all():
        print("[OK] 变更已添加到暂存区")
    else:
        print("[ERROR] 添加变更失败")
        return 1

    # 创建提交
    commit_msg = f"Auto commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"\n[INFO] 正在提交: {commit_msg}")
    if git_commit(commit_msg):
        print("[OK] 提交成功")
    else:
        print("[ERROR] 提交失败")
        return 1

    # 自动推送到远程
    print("\n[INFO] 正在推送到远程仓库...")
    if git_push():
        print("[OK] 推送成功")
    else:
        print("[ERROR] 推送失败")
        return 1

    print("\n" + "=" * 60)
    print("自动提交完成")
    print("=" * 60)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[INFO] 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 发生错误: {str(e)}")
        sys.exit(1)
