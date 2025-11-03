#!/usr/bin/env python3
"""
空文件清理大师 - Empty File Cleaner Pro
专注于高效、安全地扫描和删除空文件
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


class EmptyFileCleaner:
    def __init__(self, verbose=False, dry_run=False, log_file=None):
        self.verbose = verbose
        self.dry_run = dry_run
        self.stats = {
            'scanned': 0,
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

        self.logger = logging.getLogger('EmptyFileCleaner')

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

    def is_file_empty(self, file_path):
        """检查文件是否为空（多种方法验证）"""
        try:
            # 方法1: 检查文件大小
            if os.path.getsize(file_path) > 0:
                return False

            # 方法2: 对于文本文件，检查是否有内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_char = f.read(1)
                    if first_char:
                        return False
            except (UnicodeDecodeError, PermissionError):
                # 对于二进制文件或无法读取的文件，只依赖文件大小
                pass

            # 方法3: 对于特定文件类型进行额外验证
            if file_path.endswith(('.gitkeep', '.keep', '.placeholder')):
                self.logger.info(f"跳过占位文件: {file_path}")
                return False

            return True

        except (OSError, PermissionError) as e:
            self.logger.warning(f"无法检查文件: {file_path} - {e}")
            return False
        except Exception as e:
            self.logger.error(f"检查文件时发生意外错误: {file_path} - {e}")
            return False

    def make_file_writable(self, file_path):
        """使文件可写"""
        try:
            os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)
            return True
        except Exception as e:
            self.logger.warning(f"无法修改文件权限: {file_path} - {e}")
            return False

    def safe_delete_file(self, file_path):
        """安全删除文件"""
        try:
            # 在删除前确保文件可写
            self.make_file_writable(file_path)

            if self.dry_run:
                self.logger.info(f"[模拟删除] {file_path}")
                return True, "模拟删除成功"
            else:
                os.remove(file_path)
                self.logger.info(f"[已删除] {file_path}")
                return True, "删除成功"

        except PermissionError as e:
            self.stats['permission_errors'] += 1
            self.logger.error(f"权限拒绝: {file_path} - {e}")
            return False, f"权限错误: {e}"
        except FileNotFoundError:
            self.logger.warning(f"文件不存在: {file_path}")
            return False, "文件不存在"
        except Exception as e:
            self.stats['other_errors'] += 1
            self.logger.error(f"删除失败: {file_path} - {e}")
            return False, f"删除错误: {e}"

    def scan_directory(self, directory, exclude_dirs=None, exclude_extensions=None):
        """扫描目录中的空文件"""
        if exclude_dirs is None:
            exclude_dirs = {
                '$Recycle.Bin', 'System Volume Information', 'Windows',
                'Program Files', 'ProgramData', 'Recovery', 'node_modules',
                '.git', '.svn', '__pycache__', '.idea', '.vscode'
            }

        if exclude_extensions is None:
            exclude_extensions = {'.gitkeep', '.keep', '.placeholder'}

        empty_files = []

        try:
            for root, dirs, files in os.walk(directory):
                # 排除不需要的目录
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                for file in files:
                    file_path = os.path.join(root, file)
                    self.stats['scanned'] += 1

                    # 跳过特定扩展名的文件
                    if Path(file).suffix in exclude_extensions:
                        continue

                    if self.is_file_empty(file_path):
                        empty_files.append(file_path)
                        self.stats['empty_found'] += 1

                        if self.verbose and self.stats['empty_found'] % 100 == 0:
                            self.logger.info(f"已找到 {self.stats['empty_found']} 个空文件...")

        except Exception as e:
            self.logger.error(f"扫描目录时出错: {directory} - {e}")

        return empty_files

    def delete_empty_files(self, empty_files, max_workers=4):
        """删除空文件（支持多线程）"""
        if not empty_files:
            self.logger.info("没有找到空文件需要删除")
            return

        self.logger.info(f"开始处理 {len(empty_files)} 个空文件...")

        deleted_count = 0
        failed_files = []

        # 使用多线程加速删除操作
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self.safe_delete_file, file_path): file_path
                for file_path in empty_files
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    success, message = future.result()
                    if success:
                        deleted_count += 1
                        self.stats['deleted'] += 1
                    else:
                        failed_files.append((file_path, message))
                except Exception as e:
                    failed_files.append((file_path, str(e)))
                    self.logger.error(f"处理文件时出错: {file_path} - {e}")

        return deleted_count, failed_files

    def format_file_size(self, size_bytes):
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def print_summary(self):
        """打印统计摘要"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print("\n" + "=" * 60)
        print("🎯 空文件清理完成摘要")
        print("=" * 60)
        print(f"📁 扫描文件总数: {self.stats['scanned']:,}")
        print(f"🔍 发现空文件数: {self.stats['empty_found']:,}")
        print(f"🗑️  成功删除数: {self.stats['deleted']:,}")
        print(f"🚫 权限错误数: {self.stats['permission_errors']}")
        print(f"❌ 其他错误数: {self.stats['other_errors']}")
        print(f"⏱️  总耗时: {duration:.2f} 秒")

        if self.dry_run:
            print("💡 模式: 模拟运行（未实际删除文件）")
        else:
            print("💡 模式: 实际执行")
        print("=" * 60)

    def clean_directory(self, directory, exclude_dirs=None, exclude_extensions=None, max_workers=4):
        """主清理函数"""
        self.stats['start_time'] = time.time()

        self.logger.info(f"开始扫描目录: {directory}")

        # 扫描空文件
        empty_files = self.scan_directory(directory, exclude_dirs, exclude_extensions)

        if not empty_files:
            self.logger.info("未找到空文件")
            self.stats['end_time'] = time.time()
            self.print_summary()
            return

        self.logger.info(f"找到 {len(empty_files)} 个空文件")

        # 删除空文件
        deleted_count, failed_files = self.delete_empty_files(empty_files, max_workers)

        self.stats['end_time'] = time.time()

        # 打印结果
        self.print_summary()

        # 显示失败的文件
        if failed_files:
            print(f"\n❌ 失败文件列表 ({len(failed_files)} 个):")
            for file_path, error in failed_files[:10]:  # 只显示前10个
                print(f"  {file_path} - {error}")
            if len(failed_files) > 10:
                print(f"  ... 还有 {len(failed_files) - 10} 个失败文件")


def get_user_directory():
    """交互式获取用户要操作的目录"""
    print("🚀 空文件清理大师 - 目录选择")
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
                usage = os.path.splitdrive(drive_letter)
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
    dry_run = input("启用模拟运行模式？(不实际删除文件) (y/N): ").strip().lower()
    dry_run = dry_run in ['y', 'yes']

    if dry_run:
        print("💡 模拟运行模式已启用 - 不会实际删除文件")

    # 详细输出选项
    verbose = input("启用详细输出模式？(y/N): ").strip().lower()
    verbose = verbose in ['y', 'yes']

    # 工作线程数
    workers = input("工作线程数 (默认4，推荐1-8): ").strip()
    try:
        workers = int(workers) if workers else 4
        workers = max(1, min(workers, 16))  # 限制在1-16之间
    except ValueError:
        workers = 4
        print("使用默认线程数: 4")

    return dry_run, verbose, workers


def main():
    """主函数 - 交互式版本"""
    print("=" * 60)
    print("🎯 空文件清理大师 - Empty File Cleaner Pro")
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
        print("-" * 40)

        final_confirm = input("开始执行清理操作？(y/N): ").strip().lower()
        if final_confirm not in ['y', 'yes']:
            print("操作已取消")
            return

        # 步骤4: 执行清理
        print(f"\n🚀 开始清理操作...")
        print("=" * 50)

        # 创建清理器实例
        cleaner = EmptyFileCleaner(
            verbose=verbose,
            dry_run=dry_run,
            log_file="empty_file_cleaner.log"  # 固定日志文件
        )

        cleaner.clean_directory(
            directory=target_directory,
            max_workers=workers
        )

        print(f"\n✅ 清理操作完成！")
        if dry_run:
            print("💡 注意: 本次为模拟运行，未实际删除任何文件")
            print("   如需实际删除，请重新运行并禁用模拟运行模式")

    except KeyboardInterrupt:
        print("\n\n❌ 操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()