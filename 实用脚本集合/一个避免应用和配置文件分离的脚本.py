#!/usr/bin/env python3
"""
智能文件分类大师 - Smart File Classification Master
能够识别和保护应用程序文件结构，避免破坏程序运行
"""

import os
import sys
import shutil
import logging
from pathlib import Path
import json
import time


class SmartFileClassifier:
    def __init__(self, verbose=False, dry_run=False, log_file=None):
        self.verbose = verbose
        self.dry_run = dry_run
        self.stats = {
            'scanned_files': 0,
            'moved_files': 0,
            'protected_files': 0,
            'protected_dirs': 0,
            'error_files': 0,
            'skipped_files': 0,
            'start_time': None,
            'end_time': None
        }

        # 应用程序相关文件扩展名（需要保持在一起）
        self.app_related_extensions = {
            '.exe', '.dll', '.so', '.dylib', '.ini', '.cfg', '.config', '.conf',
            '.xml', '.json', '.yml', '.yaml', '.properties', '.setting', '.settings',
            '.dat', '.db', '.sqlite', '.mdb', '.log', '.tmp', '.cache'
        }

        # 应用程序目录特征
        self.app_directory_patterns = {
            'bin', 'lib', 'libs', 'library', 'libraries', 'runtime', 'runtimes',
            'plugins', 'addons', 'extensions', 'modules', 'components',
            'config', 'configuration', 'conf', 'settings', 'data', 'database',
            'logs', 'temp', 'tmp', 'cache', 'resources', 'assets'
        }

        # 已知的应用程序目录（不移动这些目录中的文件）
        self.known_app_directories = set()

        # 中英双语分类定义
        self.categories = {
            'Images(图片文件)': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.ico', '.raw',
                               '.heic'],
                'description': '图片和图像文件',
                'safe_to_move': True  # 图片文件通常可以安全移动
            },
            'Documents(文档文件)': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.md',
                               '.epub', '.mobi'],
                'description': '文档和办公文件',
                'safe_to_move': True
            },
            'Archives(压缩文件)': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg'],
                'description': '压缩和归档文件',
                'safe_to_move': True
            },
            'Media(媒体文件)': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.mp3', '.wav', '.flac', '.aac', '.m4a',
                               '.wma'],
                'description': '视频和音频文件',
                'safe_to_move': True
            },
            'Code(代码文件)': {
                'extensions': ['.py', '.java', '.cpp', '.c', '.h', '.hpp', '.js', '.ts', '.html', '.css', '.php',
                               '.json', '.xml', '.yml', '.yaml', '.sql', '.go', '.rs', '.swift'],
                'description': '源代码和配置文件',
                'safe_to_move': True
            },
            'App-Data(应用程序数据)': {
                'extensions': ['.ini', '.cfg', '.config', '.conf', '.setting', '.settings', '.properties', '.dat',
                               '.db', '.sqlite', '.log'],
                'description': '应用程序配置和数据文件',
                'safe_to_move': False  # 这些文件通常不能移动
            },
            'App-Executables(应用程序)': {
                'extensions': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage', '.bat', '.cmd', '.ps1',
                               '.sh'],
                'description': '可执行程序和脚本',
                'safe_to_move': False  # 应用程序文件不能移动
            },
            'App-Libraries(程序库文件)': {
                'extensions': ['.dll', '.so', '.dylib', '.ocx', '.cpl', '.jar'],
                'description': '程序库和依赖文件',
                'safe_to_move': False  # 库文件不能移动
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

        self.logger = logging.getLogger('SmartFileClassifier')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if self.verbose else logging.WARNING)
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)

        self.logger.propagate = False

    def is_app_directory(self, dir_path):
        """判断是否是应用程序目录"""
        dir_name = os.path.basename(dir_path).lower()

        # 检查目录名特征
        if dir_name in self.app_directory_patterns:
            return True

        # 检查目录内容特征
        try:
            items = os.listdir(dir_path)
            has_exe = any(item.lower().endswith('.exe') for item in items)
            has_dll = any(item.lower().endswith('.dll') for item in items)
            has_config = any(item.lower().endswith(('.ini', '.cfg', '.config')) for item in items)

            # 如果包含可执行文件和配置文件，很可能是应用程序目录
            if has_exe and (has_dll or has_config):
                return True

            # 检查是否有典型的应用程序结构
            subdirs = [d for d in items if os.path.isdir(os.path.join(dir_path, d))]
            has_bin = any('bin' in d.lower() for d in subdirs)
            has_lib = any('lib' in d.lower() for d in subdirs)
            has_config_dir = any('config' in d.lower() for d in subdirs)

            if has_bin and (has_lib or has_config_dir):
                return True

        except (PermissionError, OSError):
            pass

        return False

    def scan_for_app_directories(self, directory):
        """扫描并识别应用程序目录"""
        print("🔍 扫描应用程序目录...")

        app_dirs = set()

        for root, dirs, files in os.walk(directory):
            # 跳过已经识别的应用程序目录的子目录
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in app_dirs]

            if self.is_app_directory(root):
                app_dirs.add(root)
                # 将其所有父目录也标记为受保护
                parent = root
                while parent != directory:
                    parent = os.path.dirname(parent)
                    app_dirs.add(parent)
                    if parent == directory:
                        break

        return app_dirs

    def should_protect_file(self, file_path, app_directories):
        """判断文件是否应该被保护（不移动）"""
        file_dir = os.path.dirname(file_path)
        file_ext = Path(file_path).suffix.lower()

        # 如果文件在应用程序目录中，保护它
        for app_dir in app_directories:
            if file_path.startswith(app_dir):
                return True, "位于应用程序目录中"

        # 检查文件扩展名
        if file_ext in self.app_related_extensions:
            # 检查同目录是否有可执行文件
            file_dir = os.path.dirname(file_path)
            try:
                siblings = os.listdir(file_dir)
                has_exe = any(f.lower().endswith('.exe') for f in siblings)
                if has_exe:
                    return True, "与可执行文件在同一目录"
            except OSError:
                pass

        # 检查是否是应用程序的配置文件
        if file_ext in ['.ini', '.cfg', '.config', '.conf']:
            file_dir = os.path.dirname(file_path)
            dir_name = os.path.basename(file_dir).lower()
            if any(pattern in dir_name for pattern in ['bin', 'app', 'program']):
                return True, "应用程序配置文件"

        return False, "可以安全移动"

    def get_file_category(self, file_path, app_directories):
        """获取文件分类，考虑应用程序保护"""
        file_ext = Path(file_path).suffix.lower()

        # 首先检查是否需要保护
        should_protect, reason = self.should_protect_file(file_path, app_directories)
        if should_protect:
            return "Protected(受保护文件)", reason

        # 然后正常分类
        for category_name, category_info in self.categories.items():
            if file_ext in category_info['extensions']:
                if not category_info['safe_to_move']:
                    return "Protected(受保护文件)", "应用程序相关文件"
                return category_name, category_info['description']

        return "Others(其他文件)", "未分类文件"

    def create_category_directories(self, base_dir):
        """创建分类目录"""
        print("📁 创建分类目录...")
        for category_name in self.categories.keys():
            category_path = os.path.join(base_dir, category_name)
            if not os.path.exists(category_path):
                if not self.dry_run:
                    os.makedirs(category_path, exist_ok=True)
                print(f"  ✅ 创建: {category_name}")

        # 创建其他目录
        others_path = os.path.join(base_dir, "Others(其他文件)")
        protected_path = os.path.join(base_dir, "Protected(受保护文件)")

        if not os.path.exists(others_path) and not self.dry_run:
            os.makedirs(others_path, exist_ok=True)
        if not os.path.exists(protected_path) and not self.dry_run:
            os.makedirs(protected_path, exist_ok=True)

    def safe_move_file(self, src_path, dst_dir, filename, reason=""):
        """安全移动文件"""
        try:
            if not self.dry_run:
                os.makedirs(dst_dir, exist_ok=True)

            base_name = Path(filename).stem
            file_ext = Path(filename).suffix
            new_filename = filename
            dst_path = os.path.join(dst_dir, new_filename)

            counter = 1
            while os.path.exists(dst_path):
                new_filename = f"{base_name}_{counter}{file_ext}"
                dst_path = os.path.join(dst_dir, new_filename)
                counter += 1

            if self.dry_run:
                self.logger.info(f"[模拟移动] {filename} -> {os.path.basename(dst_dir)} ({reason})")
                return True, "模拟移动成功"
            else:
                shutil.move(src_path, dst_path)
                return True, "移动成功"

        except Exception as e:
            return False, f"移动错误: {e}"

    def classify_files_safely(self, directory, app_directories):
        """安全地分类文件"""
        print("🔄 开始安全文件分类...")

        # 跳过系统目录和分类目录
        skip_dirs = {
            '$Recycle.Bin', 'System Volume Information', 'Windows',
            'Program Files', 'ProgramData', 'Recovery'
        }
        skip_dirs.update(self.categories.keys())
        skip_dirs.add("Others(其他文件)")
        skip_dirs.add("Protected(受保护文件)")
        skip_dirs.update([os.path.basename(d) for d in app_directories])

        files_to_process = []

        # 收集文件
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                file_path = os.path.join(root, file)
                self.stats['scanned_files'] += 1

                if file.lower() in ['desktop.ini', 'thumbs.db', 'autorun.inf']:
                    self.stats['skipped_files'] += 1
                    continue

                files_to_process.append((root, file, file_path))

        print(f"找到 {len(files_to_process)} 个需要处理的文件")

        # 处理文件
        for root, file, file_path in files_to_process:
            category_name, reason = self.get_file_category(file_path, app_directories)

            if category_name == "Protected(受保护文件)":
                self.stats['protected_files'] += 1
                if self.verbose:
                    print(f"  🛡️  保护: {file} - {reason}")
                continue

            target_dir = os.path.join(directory, category_name)
            success, message = self.safe_move_file(file_path, target_dir, file, reason)

            if success:
                self.stats['moved_files'] += 1
                if self.verbose and self.stats['moved_files'] % 50 == 0:
                    print(f"  📦 已分类 {self.stats['moved_files']} 个文件...")
            else:
                self.stats['error_files'] += 1
                if self.stats['error_files'] <= 10:
                    print(f"  ❌ 错误: {file} -> {category_name} - {message}")

    def print_protection_report(self, app_directories):
        """打印保护报告"""
        if app_directories:
            print("\n🛡️  应用程序保护报告:")
            print("=" * 60)
            print(f"发现 {len(app_directories)} 个应用程序目录受保护:")
            for app_dir in sorted(app_directories)[:10]:  # 只显示前10个
                print(f"  📁 {app_dir}")
            if len(app_directories) > 10:
                print(f"  ... 还有 {len(app_directories) - 10} 个应用程序目录")
            print("=" * 60)

    def print_summary(self):
        """打印统计摘要"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print("\n" + "=" * 60)
        print("🎯 智能文件分类完成摘要")
        print("=" * 60)
        print(f"📁 扫描文件总数: {self.stats['scanned_files']:,}")
        print(f"✅ 成功分类文件: {self.stats['moved_files']:,}")
        print(f"🛡️  受保护文件: {self.stats['protected_files']:,}")
        print(f"❌ 分类失败文件: {self.stats['error_files']:,}")
        print(f"⚡ 跳过系统文件: {self.stats['skipped_files']:,}")
        print(f"⏱️  总耗时: {duration:.2f} 秒")

        if self.dry_run:
            print("💡 模式: 模拟运行（未实际移动文件）")
        else:
            print("💡 模式: 实际执行")
        print("=" * 60)

    def classify_files(self, directory):
        """主分类函数"""
        self.stats['start_time'] = time.time()

        print(f"🎯 开始智能文件分类: {directory}")

        # 扫描应用程序目录
        app_directories = self.scan_for_app_directories(directory)
        self.stats['protected_dirs'] = len(app_directories)

        # 显示保护报告
        self.print_protection_report(app_directories)

        # 创建分类目录
        self.create_category_directories(directory)

        # 安全分类文件
        self.classify_files_safely(directory, app_directories)

        self.stats['end_time'] = time.time()
        self.print_summary()


# 交互式部分（与之前类似）
def main():
    """主函数"""
    print("=" * 60)
    print("🛡️  智能文件分类大师 - Smart File Classification Master")
    print("=" * 60)
    print("💡 特点: 自动识别和保护应用程序文件，避免破坏程序运行")

    # 这里简化交互部分，您可以根据需要添加完整的交互代码
    target_directory = "D:\\"  # 示例目录

    classifier = SmartFileClassifier(
        verbose=True,
        dry_run=True,  # 建议先模拟运行
        log_file="smart_classification.log"
    )

    classifier.classify_files(target_directory)


if __name__ == "__main__":
    main()