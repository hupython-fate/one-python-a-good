#!/usr/bin/env python3
"""
文件分类大师 - File Classification Master
专注于按类型分类文件，支持中英双语目录名
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import stat


class FileClassificationMaster:
    def __init__(self, verbose=False, dry_run=False, log_file=None):
        self.verbose = verbose
        self.dry_run = dry_run
        self.stats = {
            'scanned_files': 0,
            'moved_files': 0,
            'error_files': 0,
            'skipped_files': 0,
            'created_categories': 0,
            'start_time': None,
            'end_time': None
        }

        # 中英双语分类定义
        self.categories = {
            'Images(图片文件)': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.ico', '.raw',
                               '.heic'],
                'description': '图片和图像文件'
            },
            'Documents(文档文件)': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.md',
                               '.epub', '.mobi'],
                'description': '文档和办公文件'
            },
            'Archives(压缩文件)': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg'],
                'description': '压缩和归档文件'
            },
            'Programs(程序文件)': {
                'extensions': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage', '.bat', '.cmd', '.ps1',
                               '.sh'],
                'description': '可执行程序和脚本'
            },
            'Media(媒体文件)': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.mp3', '.wav', '.flac', '.aac', '.m4a',
                               '.wma'],
                'description': '视频和音频文件'
            },
            'Code(代码文件)': {
                'extensions': ['.py', '.java', '.cpp', '.c', '.h', '.hpp', '.js', '.ts', '.html', '.css', '.php',
                               '.json', '.xml', '.yml', '.yaml', '.sql', '.go', '.rs', '.swift'],
                'description': '源代码和配置文件'
            },
            'Data(数据文件)': {
                'extensions': ['.csv', '.tsv', '.sql', '.db', '.sqlite', '.dat', '.xml', '.json', '.xlsx', '.xls'],
                'description': '数据和数据库文件'
            },
            'Fonts(字体文件)': {
                'extensions': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
                'description': '字体文件'
            },
            'Ebooks(电子书)': {
                'extensions': ['.epub', '.mobi', '.azw3', '.fb2', '.chm'],
                'description': '电子书文件'
            },
            'Design(设计文件)': {
                'extensions': ['.psd', '.ai', '.sketch', '.fig', '.xd', '.ae', '.prproj'],
                'description': '设计源文件'
            },
            'System(系统文件)': {
                'extensions': ['.dll', '.sys', '.drv', '.ocx', '.cpl', '.ini', '.cfg', '.conf'],
                'description': '系统相关文件'
            },
            'Backups(备份文件)': {
                'extensions': ['.bak', '.backup', '.old', '.tmp', '.temp'],
                'description': '备份和临时文件'
            }
        }

        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        """配置日志系统"""
        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[]
        )

        self.logger = logging.getLogger('FileClassificationMaster')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if self.verbose else logging.WARNING)
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)

        self.logger.propagate = False

    def create_category_directories(self, base_dir):
        """创建分类目录"""
        print("📁 创建分类目录...")
        for category_name in self.categories.keys():
            category_path = os.path.join(base_dir, category_name)
            if not os.path.exists(category_path):
                if not self.dry_run:
                    os.makedirs(category_path, exist_ok=True)
                self.stats['created_categories'] += 1
                print(f"  ✅ 创建: {category_name}")

        # 创建其他文件目录
        others_path = os.path.join(base_dir, "Others(其他文件)")
        if not os.path.exists(others_path) and not self.dry_run:
            os.makedirs(others_path, exist_ok=True)
            print(f"  ✅ 创建: Others(其他文件)")

    def get_file_category(self, file_ext):
        """根据文件扩展名获取分类"""
        file_ext = file_ext.lower()

        for category_name, category_info in self.categories.items():
            if file_ext in category_info['extensions']:
                return category_name, category_info['description']

        return "Others(其他文件)", "未分类文件"

    def safe_move_file(self, src_path, dst_dir, filename):
        """安全移动文件，处理文件名冲突"""
        try:
            # 确保目标目录存在
            if not self.dry_run:
                os.makedirs(dst_dir, exist_ok=True)

            # 处理文件名冲突
            base_name = Path(filename).stem
            file_ext = Path(filename).suffix
            new_filename = filename
            dst_path = os.path.join(dst_dir, new_filename)

            counter = 1
            while os.path.exists(dst_path):
                new_filename = f"{base_name}_{counter}{file_ext}"
                dst_path = os.path.join(dst_dir, new_filename)
                counter += 1
                if counter > 999:  # 防止无限循环
                    return False, "文件名冲突过多"

            if self.dry_run:
                self.logger.info(f"[模拟移动] {filename} -> {os.path.basename(dst_dir)}")
                return True, "模拟移动成功"
            else:
                shutil.move(src_path, dst_path)
                return True, "移动成功"

        except PermissionError as e:
            return False, f"权限错误: {e}"
        except Exception as e:
            return False, f"移动错误: {e}"

    def scan_and_classify_files(self, directory):
        """扫描并分类文件"""
        print("🔍 扫描并分类文件...")

        # 跳过系统目录和我们创建的分类目录
        skip_dirs = {
            '$Recycle.Bin', 'System Volume Information', 'Windows',
            'Program Files', 'ProgramData', 'Recovery'
        }
        skip_dirs.update(self.categories.keys())
        skip_dirs.add("Others(其他文件)")

        files_to_process = []

        # 第一阶段：收集所有需要处理的文件
        for root, dirs, files in os.walk(directory):
            # 跳过系统目录和分类目录
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                file_path = os.path.join(root, file)
                self.stats['scanned_files'] += 1

                # 跳过系统文件
                if file.lower() in ['desktop.ini', 'thumbs.db', 'autorun.inf']:
                    self.stats['skipped_files'] += 1
                    continue

                files_to_process.append((root, file, file_path))

        print(f"找到 {len(files_to_process)} 个需要分类的文件")

        # 第二阶段：处理文件
        moved_count = 0
        error_count = 0

        for i, (root, file, file_path) in enumerate(files_to_process):
            file_ext = Path(file).suffix.lower()

            # 获取文件分类
            category_name, category_desc = self.get_file_category(file_ext)

            # 目标目录
            target_dir = os.path.join(directory, category_name)

            # 移动文件
            success, message = self.safe_move_file(file_path, target_dir, file)

            if success:
                moved_count += 1
                self.stats['moved_files'] += 1
                if self.verbose and moved_count % 50 == 0:
                    print(f"  📦 已分类 {moved_count} 个文件...")
            else:
                error_count += 1
                self.stats['error_files'] += 1
                if error_count <= 10:  # 只显示前10个错误
                    print(f"  ❌ 错误: {file} -> {category_name} - {message}")

        return moved_count, error_count

    def print_category_info(self):
        """打印分类信息"""
        print("\n📊 文件分类体系:")
        print("=" * 60)
        for category_name, category_info in self.categories.items():
            extensions = ', '.join(category_info['extensions'][:5])  # 只显示前5个扩展名
            if len(category_info['extensions']) > 5:
                extensions += f" ...等{len(category_info['extensions'])}种格式"
            print(f"  {category_name:<25} - {category_info['description']}")
            print(f"    📎 格式: {extensions}")
        print(f"  {'Others(其他文件)':<25} - 未分类文件")
        print("=" * 60)

    def print_summary(self):
        """打印统计摘要"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print("\n" + "=" * 60)
        print("🎯 文件分类完成摘要")
        print("=" * 60)
        print(f"📁 扫描文件总数: {self.stats['scanned_files']:,}")
        print(f"✅ 成功分类文件: {self.stats['moved_files']:,}")
        print(f"❌ 分类失败文件: {self.stats['error_files']:,}")
        print(f"⚡ 跳过系统文件: {self.stats['skipped_files']:,}")
        print(f"📂 创建分类目录: {self.stats['created_categories']:,}")
        print(f"⏱️  总耗时: {duration:.2f} 秒")

        if self.dry_run:
            print("💡 模式: 模拟运行（未实际移动文件）")
        else:
            print("💡 模式: 实际执行")
        print("=" * 60)

    def classify_files(self, directory):
        """主分类函数"""
        self.stats['start_time'] = time.time()

        print(f"🎯 开始文件分类: {directory}")

        # 显示分类体系
        self.print_category_info()

        # 创建分类目录
        self.create_category_directories(directory)

        # 扫描并分类文件
        moved_count, error_count = self.scan_and_classify_files(directory)

        self.stats['end_time'] = time.time()

        # 打印结果
        self.print_summary()

        # 显示分类结果
        if not self.dry_run:
            print(f"\n📊 各分类文件数量:")
            for category_name in list(self.categories.keys()) + ["Others(其他文件)"]:
                category_path = os.path.join(directory, category_name)
                if os.path.exists(category_path):
                    file_count = len(
                        [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))])
                    if file_count > 0:
                        print(f"  {category_name}: {file_count} 个文件")


def get_user_directory():
    """交互式获取用户要操作的目录"""
    print("🚀 文件分类大师 - 目录选择")
    print("=" * 50)

    # 显示可用的磁盘驱动器
    print("可用的磁盘驱动器:")
    for drive in range(65, 91):  # A到Z的ASCII码
        drive_letter = chr(drive) + ":\\"
        if os.path.exists(drive_letter):
            try:
                statvfs = os.statvfs(drive_letter)
                total_gb = (statvfs.f_blocks * statvfs.f_frsize) / (1024 ** 3)
                free_gb = (statvfs.f_bavail * statvfs.f_frsize) / (1024 ** 3)
                usage_percent = ((total_gb - free_gb) / total_gb) * 100
                print(
                    f"  {drive_letter} - 总空间: {total_gb:.1f}GB, 可用: {free_gb:.1f}GB, 使用率: {usage_percent:.1f}%")
            except:
                print(f"  {drive_letter} - 信息获取失败")

    print("\n选项:")
    print("  1. 输入磁盘驱动器 (如: C:, D:, E:)")
    print("  2. 输入完整路径 (如: C:\\Users\\YourName\\Documents)")
    print("  3. 输入当前目录 (.)")
    print("  4. 退出程序 (q)")
    print("-" * 50)

    while True:
        user_input = input("请输入要分类的目录路径: ").strip()

        if user_input.lower() in ['q', 'quit', 'exit']:
            print("程序已退出")
            sys.exit(0)

        if user_input == '.':
            target_dir = os.getcwd()
        elif len(user_input) == 2 and user_input[1] == ':' and user_input[0].isalpha():
            target_dir = user_input.upper() + "\\"
        else:
            target_dir = user_input

        if not os.path.exists(target_dir):
            print(f"❌ 错误: 目录不存在 - {target_dir}")
            continue

        if not os.path.isdir(target_dir):
            print(f"❌ 错误: 这不是一个目录 - {target_dir}")
            continue

        print(f"\n✅ 选择的目录: {target_dir}")
        print(f"   绝对路径: {os.path.abspath(target_dir)}")

        confirm = input("是否确认分类此目录？(y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            return target_dir
        else:
            print("重新选择目录...\n")


def get_classification_options():
    """获取分类选项"""
    print("\n🛠️  分类选项设置")
    print("-" * 30)

    dry_run = input("启用模拟运行模式？(不实际移动文件) (y/N): ").strip().lower()
    dry_run = dry_run in ['y', 'yes']

    if dry_run:
        print("💡 模拟运行模式已启用 - 不会实际移动文件")

    verbose = input("启用详细输出模式？(y/N): ").strip().lower()
    verbose = verbose in ['y', 'yes']

    return dry_run, verbose


def main():
    """主函数"""
    print("=" * 60)
    print("📁 文件分类大师 - File Classification Master")
    print("=" * 60)

    try:
        # 获取目录和选项
        target_directory = get_user_directory()
        dry_run, verbose = get_classification_options()

        # 最终确认
        print(f"\n📋 操作摘要:")
        print(f"   目标目录: {target_directory}")
        print(f"   模式: {'模拟运行' if dry_run else '实际执行'}")
        print(f"   详细输出: {'是' if verbose else '否'}")
        print("-" * 40)

        final_confirm = input("开始执行文件分类？(y/N): ").strip().lower()
        if final_confirm not in ['y', 'yes']:
            print("操作已取消")
            return

        # 执行分类
        print(f"\n🚀 开始文件分类操作...")

        classifier = FileClassificationMaster(
            verbose=verbose,
            dry_run=dry_run,
            log_file="file_classification.log"
        )

        classifier.classify_files(target_directory)

        print(f"\n✅ 文件分类完成！")
        if dry_run:
            print("💡 注意: 本次为模拟运行，未实际移动任何文件")

    except KeyboardInterrupt:
        print("\n\n❌ 操作被用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main()