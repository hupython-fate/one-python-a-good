#!/usr/bin/env python3
"""
应用程序修复大师 - Application Repair Master
专门修复因文件分类而分离的应用程序和配置文件
"""

import os
import sys
import shutil
import logging
from pathlib import Path
import time


class ApplicationRepairMaster:
    def __init__(self, verbose=False, dry_run=False, log_file=None):
        self.verbose = verbose
        self.dry_run = dry_run
        self.stats = {
            'scanned_files': 0,
            'repaired_apps': 0,
            'moved_files': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

        # 应用程序文件关联规则
        self.app_file_associations = {
            # 可执行文件 -> 需要找回的文件类型
            '.exe': ['.dll', '.ini', '.cfg', '.config', '.json', '.xml', '.dat', '.db'],
            '.msi': ['.dll', '.ini', '.cfg'],
            '.dll': ['.exe'],  # DLL文件需要找回对应的EXE
            '.jar': ['.properties', '.xml', '.conf'],
            '.py': ['.py', '.ini', '.cfg', '.json', '.yaml', '.yml'],  # Python脚本和配置文件
            '.sh': ['.conf', '.cfg', '.ini', '.sh'],
            '.bat': ['.exe', '.dll', '.ini', '.cfg'],
            '.cmd': ['.exe', '.dll', '.ini', '.cfg']
        }

        # 应用程序目录模式
        self.app_directory_names = {
            'bin', 'app', 'application', 'program', 'software', 'tool',
            'game', 'utility', 'setup', 'install', 'runtime'
        }

        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        """配置日志系统"""
        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[]
        )

        self.logger = logging.getLogger('ApplicationRepairMaster')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if self.verbose else logging.WARNING)
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)

        self.logger.propagate = False

    def find_application_executables(self, directory):
        """在整个目录中查找所有的应用程序可执行文件"""
        print("🔍 扫描应用程序可执行文件...")

        executables = []
        classified_dirs = [
            'App-Executables(应用程序)', 'App-Libraries(程序库文件)',
            'App-Data(应用程序数据)', 'Code(代码文件)'
        ]

        # 扫描分类目录和原始目录
        search_paths = [directory]
        for classified_dir in classified_dirs:
            classified_path = os.path.join(directory, classified_dir)
            if os.path.exists(classified_path):
                search_paths.append(classified_path)

        for search_path in search_paths:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    file_ext = Path(file).suffix.lower()
                    if file_ext in ['.exe', '.msi', '.bat', '.cmd', '.jar']:
                        file_path = os.path.join(root, file)
                        executables.append({
                            'path': file_path,
                            'name': file,
                            'extension': file_ext,
                            'directory': root
                        })

        return executables

    def find_related_files(self, directory, executable_info):
        """查找与可执行文件相关的文件"""
        base_name = Path(executable_info['name']).stem
        related_extensions = self.app_file_associations.get(executable_info['extension'], [])

        related_files = []

        # 在整个目录中搜索相关文件
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()

                # 检查文件扩展名是否相关
                if file_ext in related_extensions:
                    # 检查文件名是否匹配
                    related_base_name = Path(file).stem
                    if (related_base_name == base_name or
                            base_name in related_base_name or
                            related_base_name in base_name):
                        related_files.append(file_path)

                # 特别处理：查找同名的配置文件
                if file_ext in ['.ini', '.cfg', '.config', '.json', '.xml']:
                    if Path(file).stem == base_name:
                        related_files.append(file_path)

        return related_files

    def determine_restoration_path(self, executable_info, related_files):
        """确定文件应该恢复到的目录"""
        exec_dir = executable_info['directory']
        exec_name = executable_info['name']

        # 如果可执行文件在分类目录中，创建专门的应用程序目录
        if any(x in exec_dir for x in ['App-Executables(应用程序)', 'App-Libraries(程序库文件)']):
            # 在原始目录中创建应用程序文件夹
            base_dir = os.path.dirname(exec_dir)
            if base_dir == exec_dir:  # 如果已经在根目录
                base_dir = exec_dir

            app_dir_name = f"App-{Path(exec_name).stem}"
            restoration_path = os.path.join(base_dir, app_dir_name)
        else:
            # 如果可执行文件还在原始位置，就使用原始目录
            restoration_path = exec_dir

        return restoration_path

    def restore_application_files(self, directory, executable_info, related_files):
        """恢复应用程序文件到正确位置"""
        restoration_path = self.determine_restoration_path(executable_info, related_files)

        print(f"\n🛠️  修复应用程序: {executable_info['name']}")
        print(f"   恢复位置: {os.path.basename(restoration_path)}")

        moved_files = 0

        # 确保恢复目录存在
        if not self.dry_run:
            os.makedirs(restoration_path, exist_ok=True)

        # 移动可执行文件（如果在分类目录中）
        if any(x in executable_info['directory'] for x in ['App-Executables(应用程序)', 'App-Libraries(程序库文件)']):
            if executable_info['directory'] != restoration_path:
                exec_source = executable_info['path']
                exec_target = os.path.join(restoration_path, executable_info['name'])

                if self.dry_run:
                    print(f"  📦 [模拟] 移动可执行文件: {executable_info['name']}")
                else:
                    try:
                        shutil.move(exec_source, exec_target)
                        print(f"  ✅ 移动可执行文件: {executable_info['name']}")
                        moved_files += 1
                    except Exception as e:
                        print(f"  ❌ 移动失败: {executable_info['name']} - {e}")

        # 移动相关文件
        for related_file in related_files:
            file_name = os.path.basename(related_file)
            target_path = os.path.join(restoration_path, file_name)

            # 跳过已经在目标位置的文件
            if os.path.dirname(related_file) == restoration_path:
                continue

            if self.dry_run:
                print(f"  📦 [模拟] 移动相关文件: {file_name}")
            else:
                try:
                    # 处理文件名冲突
                    counter = 1
                    base_name = Path(file_name).stem
                    ext = Path(file_name).suffix
                    while os.path.exists(target_path):
                        new_name = f"{base_name}_{counter}{ext}"
                        target_path = os.path.join(restoration_path, new_name)
                        counter += 1

                    shutil.move(related_file, target_path)
                    print(f"  ✅ 移动相关文件: {file_name}")
                    moved_files += 1
                except Exception as e:
                    print(f"  ❌ 移动失败: {file_name} - {e}")
                    self.stats['errors'] += 1

        return moved_files > 0

    def scan_for_orphaned_config_files(self, directory):
        """扫描孤立的配置文件（没有对应的可执行文件）"""
        print("\n🔍 扫描孤立的配置文件...")

        orphaned_files = []
        config_extensions = ['.ini', '.cfg', '.config', '.conf', '.xml', '.json']

        # 在数据目录中查找配置文件
        data_dirs = ['App-Data(应用程序数据)', 'Code(代码文件)', 'Others(其他文件)']

        for data_dir in data_dirs:
            data_path = os.path.join(directory, data_dir)
            if not os.path.exists(data_path):
                continue

            for root, dirs, files in os.walk(data_path):
                for file in files:
                    file_ext = Path(file).suffix.lower()
                    if file_ext in config_extensions:
                        file_path = os.path.join(root, file)
                        base_name = Path(file).stem

                        # 检查是否有对应的可执行文件
                        has_corresponding_exe = self.find_corresponding_executable(directory, base_name)
                        if not has_corresponding_exe:
                            orphaned_files.append({
                                'path': file_path,
                                'name': file,
                                'base_name': base_name
                            })

        return orphaned_files

    def find_corresponding_executable(self, directory, base_name):
        """查找对应的可执行文件"""
        exec_dirs = ['App-Executables(应用程序)', '.']

        for exec_dir in exec_dirs:
            exec_path = os.path.join(directory, exec_dir)
            if not os.path.exists(exec_path):
                continue

            for root, dirs, files in os.walk(exec_path):
                for file in files:
                    if Path(file).suffix.lower() in ['.exe', '.bat', '.cmd']:
                        if Path(file).stem == base_name:
                            return os.path.join(root, file)

        return None

    def repair_orphaned_files(self, directory, orphaned_files):
        """修复孤立的配置文件"""
        if not orphaned_files:
            print("✅ 未发现孤立的配置文件")
            return

        print(f"发现 {len(orphaned_files)} 个孤立的配置文件")

        restored_count = 0
        for orphaned_file in orphaned_files:
            print(f"\n📄 处理孤立文件: {orphaned_file['name']}")

            # 尝试在原始位置附近查找可能的应用程序目录
            possible_locations = self.find_possible_restoration_locations(directory, orphaned_file['base_name'])

            if possible_locations:
                # 选择最可能的位置
                restoration_path = possible_locations[0]

                if self.dry_run:
                    print(f"  📦 [模拟] 移动到: {os.path.basename(restoration_path)}")
                else:
                    try:
                        os.makedirs(restoration_path, exist_ok=True)
                        target_path = os.path.join(restoration_path, orphaned_file['name'])
                        shutil.move(orphaned_file['path'], target_path)
                        print(f"  ✅ 移动到: {os.path.basename(restoration_path)}")
                        restored_count += 1
                    except Exception as e:
                        print(f"  ❌ 移动失败: {e}")
            else:
                # 创建专门的配置目录
                config_dir = os.path.join(directory, "Recovered-Configs(恢复的配置)")
                if self.dry_run:
                    print(f"  📦 [模拟] 移动到恢复目录")
                else:
                    try:
                        os.makedirs(config_dir, exist_ok=True)
                        target_path = os.path.join(config_dir, orphaned_file['name'])
                        shutil.move(orphaned_file['path'], target_path)
                        print(f"  ✅ 移动到恢复目录")
                        restored_count += 1
                    except Exception as e:
                        print(f"  ❌ 移动失败: {e}")

        return restored_count

    def find_possible_restoration_locations(self, directory, base_name):
        """查找可能的恢复位置"""
        possible_locations = []

        # 查找包含相似名称的目录
        for root, dirs, files in os.walk(directory):
            dir_name = os.path.basename(root).lower()
            if (base_name.lower() in dir_name or
                    any(keyword in dir_name for keyword in self.app_directory_names)):
                possible_locations.append(root)

        return possible_locations

    def print_repair_plan(self, executables, orphaned_files):
        """打印修复计划"""
        print("\n📋 修复计划摘要")
        print("=" * 60)
        print(f"🔧 需要修复的应用程序: {len(executables)} 个")
        for exec_info in executables[:5]:  # 显示前5个
            print(f"  - {exec_info['name']} (在 {os.path.basename(exec_info['directory'])})")
        if len(executables) > 5:
            print(f"  ... 还有 {len(executables) - 5} 个应用程序")

        print(f"📄 孤立的配置文件: {len(orphaned_files)} 个")
        for orphaned in orphaned_files[:3]:
            print(f"  - {orphaned['name']}")
        if len(orphaned_files) > 3:
            print(f"  ... 还有 {len(orphaned_files) - 3} 个文件")
        print("=" * 60)

    def print_summary(self):
        """打印统计摘要"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print("\n" + "=" * 60)
        print("🎯 应用程序修复完成摘要")
        print("=" * 60)
        print(f"🔧 修复的应用程序: {self.stats['repaired_apps']} 个")
        print(f"📦 移动的文件数: {self.stats['moved_files']} 个")
        print(f"❌ 修复错误数: {self.stats['errors']} 个")
        print(f"⏱️  总耗时: {duration:.2f} 秒")

        if self.dry_run:
            print("💡 模式: 模拟运行（未实际移动文件）")
        else:
            print("💡 模式: 实际执行")
        print("=" * 60)

    def repair_applications(self, directory):
        """主修复函数"""
        self.stats['start_time'] = time.time()

        print(f"🎯 开始修复应用程序文件结构: {directory}")

        # 查找所有可执行文件
        executables = self.find_application_executables(directory)

        # 查找孤立的配置文件
        orphaned_files = self.scan_for_orphaned_config_files(directory)

        # 显示修复计划
        self.print_repair_plan(executables, orphaned_files)

        # 修复应用程序
        repaired_count = 0
        for executable in executables:
            related_files = self.find_related_files(directory, executable)
            if related_files:
                success = self.restore_application_files(directory, executable, related_files)
                if success:
                    repaired_count += 1
                    self.stats['repaired_apps'] += 1
                    self.stats['moved_files'] += len(related_files) + 1  # +1 for executable

        # 修复孤立文件
        orphaned_restored = self.repair_orphaned_files(directory, orphaned_files)
        self.stats['moved_files'] += orphaned_restored

        self.stats['end_time'] = time.time()
        self.print_summary()


def main():
    """主函数"""
    print("=" * 60)
    print("🔧 应用程序修复大师 - Application Repair Master")
    print("=" * 60)
    print("💡 专门修复因文件分类而分离的应用程序和配置文件")

    # 这里可以添加交互式目录选择
    target_directory = "D:\\"  # 示例目录

    repair_master = ApplicationRepairMaster(
        verbose=True,
        dry_run=False,  # 建议先模拟运行！
        log_file="app_repair.log"
    )

    repair_master.repair_applications(target_directory)

    print(f"\n💡 建议:")
    print("  1. 先模拟运行查看修复计划")
    print("  2. 确认修复计划合理后，设置 dry_run=False 进行实际修复")
    print("  3. 修复后测试关键应用程序是否正常工作")


if __name__ == "__main__":
    main()