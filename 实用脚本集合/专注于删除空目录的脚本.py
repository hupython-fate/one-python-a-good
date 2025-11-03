#!/usr/bin/env python3
"""
空目录清理大师 - Empty Directory Cleaner Pro
专注于高效、安全地扫描和删除空目录
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import stat
from datetime import datetime


class EmptyDirectoryCleaner:
    def __init__(self, verbose=False, dry_run=False, log_file=None):
        self.verbose = verbose
        self.dry_run = dry_run
        self.stats = {
            'scanned_dirs': 0,
            'empty_found': 0,
            'deleted': 0,
            'permission_errors': 0,
            'other_errors': 0,
            'start_time': None,
            'end_time': None
        }

        # 设置日志
        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        """配置日志系统"""
        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[]
        )

        self.logger = logging.getLogger('EmptyDirectoryCleaner')

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if self.verbose else logging.WARNING)
        self.logger.addHandler(console_handler)

        # 文件处理器（如果指定了日志文件）
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)

        self.logger.propagate = False

    def is_directory_empty(self, dir_path):
        """检查目录是否为空（递归检查）"""
        try:
            # 方法1: 快速检查 - 只看直接子项
            with os.scandir(dir_path) as it:
                for entry in it:
                    # 如果有任何文件或目录，就不是空目录
                    return False
            return True

        except (OSError, PermissionError) as e:
            self.logger.warning(f"无法扫描目录: {dir_path} - {e}")
            return False
        except Exception as e:
            self.logger.error(f"检查目录时发生意外错误: {dir_path} - {e}")
            return False

    def is_directory_safe_to_delete(self, dir_path):
        """检查目录是否安全删除（排除系统关键目录）"""
        dir_name = os.path.basename(dir_path).lower()
        full_path = dir_path.lower()

        # 系统关键目录黑名单
        system_dirs = {
            'windows', 'program files', 'programdata', 'system32', 'syswow64',
            'users', 'documents and settings', 'recovery', 'boot',
            '$recycle.bin', 'system volume information', 'perflogs'
        }

        # 开发相关目录（通常可以安全删除的空目录）
        safe_dirs = {
            '__pycache__', '.pytest_cache', '.mypy_cache', '.hypothesis',
            '.idea', '.vscode', '.vs', 'node_modules', 'build', 'dist',
            'target', '.gradle', '.nuget', 'packages', 'bin', 'obj',
            'out', 'output', 'temp', 'tmp', 'logs', '.git'
        }

        # 检查是否是系统关键目录
        if any(system_dir in full_path for system_dir in system_dirs):
            return False, "系统关键目录"

        # 检查根目录
        if len(dir_path) <= 3:  # 如 C:\
            return False, "根目录"

        # 检查是否是已知的安全目录
        if dir_name in safe_dirs:
            return True, "开发目录"

        return True, "普通目录"

    def make_dir_writable(self, dir_path):
        """使目录可写"""
        try:
            os.chmod(dir_path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
            return True
        except Exception as e:
            self.logger.warning(f"无法修改目录权限: {dir_path} - {e}")
            return False

    def safe_delete_directory(self, dir_path):
        """安全删除空目录"""
        try:
            # 安全检查
            is_safe, reason = self.is_directory_safe_to_delete(dir_path)
            if not is_safe:
                return False, f"安全限制: {reason}"

            # 确保目录可写
            self.make_dir_writable(dir_path)

            if self.dry_run:
                self.logger.info(f"[模拟删除] 空目录: {dir_path}")
                return True, "模拟删除成功"
            else:
                os.rmdir(dir_path)
                self.logger.info(f"[已删除] 空目录: {dir_path}")
                return True, "删除成功"

        except PermissionError as e:
            self.stats['permission_errors'] += 1
            self.logger.error(f"权限拒绝: {dir_path} - {e}")
            return False, f"权限错误: {e}"
        except FileNotFoundError:
            self.logger.warning(f"目录不存在: {dir_path}")
            return False, "目录不存在"
        except OSError as e:
            # 目录不为空或其他OS错误
            self.stats['other_errors'] += 1
            self.logger.warning(f"目录删除失败（可能不为空）: {dir_path} - {e}")
            return False, f"目录不为空: {e}"
        except Exception as e:
            self.stats['other_errors'] += 1
            self.logger.error(f"删除失败: {dir_path} - {e}")
            return False, f"删除错误: {e}"

    def scan_empty_directories(self, directory, exclude_dirs=None):
        """扫描空目录（从最深层的开始）"""
        if exclude_dirs is None:
            exclude_dirs = {
                '$Recycle.Bin', 'System Volume Information', 'Windows',
                'Program Files', 'ProgramData', 'Recovery', 'Boot'
            }

        empty_dirs = []

        try:
            # 使用深度优先搜索，从最深层开始
            for root, dirs, files in os.walk(directory, topdown=False):
                self.stats['scanned_dirs'] += 1

                # 排除不需要的目录
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                # 检查当前目录是否为空
                if self.is_directory_empty(root):
                    # 安全检查
                    is_safe, reason = self.is_directory_safe_to_delete(root)
                    if is_safe:
                        empty_dirs.append(root)
                        self.stats['empty_found'] += 1

                        if self.verbose and self.stats['empty_found'] % 50 == 0:
                            self.logger.info(f"已找到 {self.stats['empty_found']} 个空目录...")

        except Exception as e:
            self.logger.error(f"扫描目录时出错: {directory} - {e}")

        return empty_dirs

    def delete_empty_directories(self, empty_dirs, max_workers=2):
        """删除空目录（支持多线程，但线程数较少以避免竞争条件）"""
        if not empty_dirs:
            self.logger.info("没有找到空目录需要删除")
            return [], []

        self.logger.info(f"开始处理 {len(empty_dirs)} 个空目录...")

        deleted_count = 0
        failed_dirs = []

        # 按路径长度排序，先删除最深层的目录
        empty_dirs.sort(key=len, reverse=True)

        # 使用多线程（但线程数较少，避免文件系统竞争）
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_dir = {
                executor.submit(self.safe_delete_directory, dir_path): dir_path
                for dir_path in empty_dirs
            }

            for future in as_completed(future_to_dir):
                dir_path = future_to_dir[future]
                try:
                    success, message = future.result()
                    if success:
                        deleted_count += 1
                        self.stats['deleted'] += 1
                    else:
                        failed_dirs.append((dir_path, message))
                except Exception as e:
                    failed_dirs.append((dir_path, str(e)))
                    self.logger.error(f"处理目录时出错: {dir_path} - {e}")

        return deleted_count, failed_dirs

    def print_summary(self):
        """打印统计摘要"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print("\n" + "=" * 60)
        print("📁 空目录清理完成摘要")
        print("=" * 60)
        print(f"🔍 扫描目录总数: {self.stats['scanned_dirs']:,}")
        print(f"📂 发现空目录数: {self.stats['empty_found']:,}")
        print(f"🗑️  成功删除数: {self.stats['deleted']:,}")
        print(f"🚫 权限错误数: {self.stats['permission_errors']}")
        print(f"❌ 其他错误数: {self.stats['other_errors']}")
        print(f"⏱️  总耗时: {duration:.2f} 秒")

        if self.dry_run:
            print("💡 模式: 模拟运行（未实际删除目录）")
        else:
            print("💡 模式: 实际执行")
        print("=" * 60)

    def clean_directories(self, directory, exclude_dirs=None, max_workers=2):
        """主清理函数"""
        self.stats['start_time'] = time.time()

        self.logger.info(f"开始扫描目录: {directory}")

        # 扫描空目录
        empty_dirs = self.scan_empty_directories(directory, exclude_dirs)

        if not empty_dirs:
            self.logger.info("未找到可删除的空目录")
            self.stats['end_time'] = time.time()
            self.print_summary()
            return

        self.logger.info(f"找到 {len(empty_dirs)} 个空目录")

        # 显示前10个空目录（供用户确认）
        if self.verbose:
            print("\n📋 发现的空目录示例:")
            for i, dir_path in enumerate(empty_dirs[:10]):
                print(f"  {i + 1}. {dir_path}")
            if len(empty_dirs) > 10:
                print(f"  ... 还有 {len(empty_dirs) - 10} 个空目录")

        # 删除空目录
        deleted_count, failed_dirs = self.delete_empty_directories(empty_dirs, max_workers)

        self.stats['end_time'] = time.time()

        # 打印结果
        self.print_summary()

        # 显示失败的文件
        if failed_dirs:
            print(f"\n❌ 失败目录列表 ({len(failed_dirs)} 个):")
            for dir_path, error in failed_dirs[:10]:  # 只显示前10个
                print(f"  {dir_path} - {error}")
            if len(failed_dirs) > 10:
                print(f"  ... 还有 {len(failed_dirs) - 10} 个失败目录")


def get_user_directory():
    """交互式获取用户要操作的目录"""
    print("🚀 空目录清理大师 - 目录选择")
    print("=" * 50)

    # 显示可用的磁盘驱动器
    print("可用的磁盘驱动器:")
    drives = []
    for drive in range(65, 91):  # A到Z的ASCII码
        drive_letter = chr(drive) + ":\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
            try:
                # 获取磁盘使用情况
                if os.path.exists(drive_letter):
                    statvfs = os.statvfs(drive_letter)
                    total_gb = (statvfs.f_blocks * statvfs.f_frsize) / (1024 ** 3)
                    free_gb = (statvfs.f_bavail * statvfs.f_frsize) / (1024 ** 3)
                    used_gb = total_gb - free_gb
                    usage_percent = (used_gb / total_gb) * 100
                    print(
                        f"  {drive_letter} - 总空间: {total_gb:.1f}GB, 可用: {free_gb:.1f}GB, 使用率: {usage_percent:.1f}%")
                else:
                    print(f"  {drive_letter} - 无法访问")
            except:
                print(f"  {drive_letter} - 信息获取失败")

    print("\n选项:")
    print("  1. 输入磁盘驱动器 (如: C:, D:, E:)")
    print("  2. 输入完整路径 (如: C:\\Users\\YourName\\Documents)")
    print("  3. 输入当前目录 (.)")
    print("  4. 退出程序 (q)")
    print("-" * 50)

    while True:
        user_input = input("请输入要清理的目录路径: ").strip()

        if user_input.lower() in ['q', 'quit', 'exit']:
            print("程序已退出")
            sys.exit(0)

        if user_input == '.':
            target_dir = os.getcwd()
        elif len(user_input) == 2 and user_input[1] == ':' and user_input[0].isalpha():
            # 处理 D: 这样的输入
            target_dir = user_input.upper() + "\\"
        else:
            target_dir = user_input

        # 验证目录是否存在
        if not os.path.exists(target_dir):
            print(f"❌ 错误: 目录不存在 - {target_dir}")
            print("请重新输入有效的目录路径")
            continue

        if not os.path.isdir(target_dir):
            print(f"❌ 错误: 这不是一个目录 - {target_dir}")
            print("请重新输入有效的目录路径")
            continue

        # 显示确认信息
        print(f"\n✅ 选择的目录: {target_dir}")
        print(f"   绝对路径: {os.path.abspath(target_dir)}")

        # 确认选择
        confirm = input("是否确认清理此目录？(y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            return target_dir
        else:
            print("重新选择目录...\n")


def get_cleanup_options():
    """获取清理选项"""
    print("\n🛠️  清理选项设置")
    print("-" * 30)

    # 模拟运行选项
    dry_run = input("启用模拟运行模式？(不实际删除目录) (y/N): ").strip().lower()
    dry_run = dry_run in ['y', 'yes']

    if dry_run:
        print("💡 模拟运行模式已启用 - 不会实际删除目录")

    # 详细输出选项
    verbose = input("启用详细输出模式？(y/N): ").strip().lower()
    verbose = verbose in ['y', 'yes']

    # 工作线程数（目录删除用较少线程）
    workers = input("工作线程数 (默认2，推荐1-4): ").strip()
    try:
        workers = int(workers) if workers else 2
        workers = max(1, min(workers, 8))  # 限制在1-8之间
    except ValueError:
        workers = 2
        print("使用默认线程数: 2")

    return dry_run, verbose, workers


def main():
    """主函数 - 交互式版本"""
    print("=" * 60)
    print("📁 空目录清理大师 - Empty Directory Cleaner Pro")
    print("=" * 60)

    try:
        # 步骤1: 获取用户要操作的目录
        target_directory = get_user_directory()

        # 步骤2: 获取清理选项
        dry_run, verbose, workers = get_cleanup_options()

        # 步骤3: 最终确认
        print(f"\n📋 操作摘要:")
        print(f"   目标目录: {target_directory}")
        print(f"   模式: {'模拟运行' if dry_run else '实际执行'}")
        print(f"   详细输出: {'是' if verbose else '否'}")
        print(f"   工作线程: {workers}")
        print("💡 注意: 只会删除完全空的目录")
        print("-" * 40)

        final_confirm = input("开始执行清理操作？(y/N): ").strip().lower()
        if final_confirm not in ['y', 'yes']:
            print("操作已取消")
            return

        # 步骤4: 执行清理
        print(f"\n🚀 开始清理操作...")
        print("=" * 50)

        # 创建清理器实例
        cleaner = EmptyDirectoryCleaner(
            verbose=verbose,
            dry_run=dry_run,
            log_file="empty_directory_cleaner.log"  # 固定日志文件
        )

        cleaner.clean_directories(
            directory=target_directory,
            max_workers=workers
        )

        print(f"\n✅ 清理操作完成！")
        if dry_run:
            print("💡 注意: 本次为模拟运行，未实际删除任何目录")
            print("   如需实际删除，请重新运行并禁用模拟运行模式")

    except KeyboardInterrupt:
        print("\n\n❌ 操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()