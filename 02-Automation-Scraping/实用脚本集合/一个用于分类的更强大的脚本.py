#!/usr/bin/env python3
"""
终极文件整理大师 - Ultimate File Organizer
完全颠覆式整理，应用程序保持完整，其他文件按中文分类
"""

import os
import sys
import shutil
import stat
from pathlib import Path
import time


class UltimateFileOrganizer:
    def __init__(self):
        self.stats = {
            'total_files': 0,
            'moved_files': 0,
            'app_files': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

        # 纯中文分类目录
        self.chinese_categories = {
            '图片文件': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.ico', '.raw', '.heic'],
            '文档文件': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.md', '.epub',
                         '.mobi'],
            '压缩文件': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg'],
            '媒体文件': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.mp3', '.wav', '.flac', '.aac', '.m4a',
                         '.wma'],
            '代码文件': ['.py', '.java', '.cpp', '.c', '.h', '.hpp', '.js', '.ts', '.html', '.css', '.php', '.json',
                         '.xml', '.yml', '.yaml', '.sql'],
            '应用程序': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage', '.bat', '.cmd', '.ps1', '.sh'],
            '程序库文件': ['.dll', '.so', '.dylib', '.ocx', '.cpl', '.jar'],
            '配置文件': ['.ini', '.cfg', '.config', '.conf', '.setting', '.settings', '.properties'],
            '数据文件': ['.dat', '.db', '.sqlite', '.csv', '.tsv'],
            '字体文件': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
            '电子书': ['.epub', '.mobi', '.azw3', '.fb2', '.chm'],
            '设计文件': ['.psd', '.ai', '.sketch', '.fig', '.xd', '.ae', '.prproj']
        }

        # 应用程序相关扩展名（需要保持在一起）
        self.app_extensions = {'.exe', '.dll', '.so', '.dylib', '.ini', '.cfg', '.config', '.conf', '.dat', '.db'}

    def force_delete(self, path):
        """强制删除文件或目录"""
        try:
            if os.path.isfile(path):
                os.chmod(path, stat.S_IWRITE)
                os.remove(path)
            elif os.path.isdir(path):
                os.chmod(path, stat.S_IWRITE)
                shutil.rmtree(path)
        except:
            pass

    def force_move(self, src, dst):
        """强制移动文件，解决所有权限问题"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # 确保目标目录存在
                os.makedirs(os.path.dirname(dst), exist_ok=True)

                # 如果目标文件已存在，先删除
                if os.path.exists(dst):
                    self.force_delete(dst)

                # 移动文件
                shutil.move(src, dst)
                return True
            except PermissionError:
                # 修改权限后重试
                try:
                    os.chmod(src, stat.S_IWRITE)
                    if os.path.exists(dst):
                        os.chmod(dst, stat.S_IWRITE)
                    time.sleep(0.1)
                except:
                    pass
            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f"    ❌ 移动失败: {os.path.basename(src)} -> {e}")
                    return False
                time.sleep(0.1)
        return False

    def is_app_file(self, file_path):
        """判断是否是应用程序相关文件"""
        ext = Path(file_path).suffix.lower()
        return ext in self.app_extensions

    def find_app_executables(self, directory):
        """查找所有的应用程序可执行文件"""
        print("🔍 扫描应用程序文件...")
        executables = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.exe'):
                    exec_path = os.path.join(root, file)
                    executables.append(exec_path)

        print(f"   找到 {len(executables)} 个应用程序")
        return executables

    def get_app_files(self, directory, executables):
        """获取所有需要保持在一起的应用程序文件"""
        app_files = set()

        for exec_path in executables:
            exec_dir = os.path.dirname(exec_path)
            exec_name = Path(exec_path).stem

            # 把可执行文件所在目录的所有文件都视为应用程序文件
            for root, dirs, files in os.walk(exec_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    app_files.add(file_path)

        return app_files

    def create_new_structure(self, directory):
        """创建全新的目录结构"""
        print("📁 创建全新目录结构...")

        # 删除所有旧目录（除了我们要保留的文件）
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                # 跳过我们刚创建的分类目录
                if item not in self.chinese_categories and item != '应用程序集合':
                    try:
                        shutil.rmtree(item_path)
                        print(f"    🗑️ 删除旧目录: {item}")
                    except:
                        print(f"    ⚠️ 无法删除目录: {item}")

        # 创建所有中文分类目录
        for category in self.chinese_categories:
            category_path = os.path.join(directory, category)
            os.makedirs(category_path, exist_ok=True)
            print(f"    ✅ 创建目录: {category}")

        # 创建应用程序目录
        app_dir = os.path.join(directory, '应用程序集合')
        os.makedirs(app_dir, exist_ok=True)
        print(f"    ✅ 创建目录: 应用程序集合")

    def get_file_category(self, file_path, app_files):
        """获取文件的中文分类"""
        # 如果是应用程序文件，返回应用程序集合
        if file_path in app_files:
            return '应用程序集合'

        ext = Path(file_path).suffix.lower()

        for category, extensions in self.chinese_categories.items():
            if ext in extensions:
                return category

        return '其他文件'

    def organize_files(self, directory):
        """主整理函数"""
        self.stats['start_time'] = time.time()

        print("🚀 开始终极文件整理...")
        print("=" * 60)

        # 第一步：扫描所有文件
        print("📊 扫描所有文件...")
        all_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
                self.stats['total_files'] += 1

        print(f"   找到 {self.stats['total_files']} 个文件")

        # 第二步：识别应用程序
        executables = self.find_app_executables(directory)
        app_files = self.get_app_files(directory, executables)
        self.stats['app_files'] = len(app_files)

        # 第三步：创建全新结构
        self.create_new_structure(directory)

        # 第四步：移动所有文件
        print("🔄 移动文件中...")
        moved_count = 0

        for file_path in all_files:
            try:
                file_name = os.path.basename(file_path)

                # 获取文件分类
                category = self.get_file_category(file_path, app_files)
                target_dir = os.path.join(directory, category)

                # 处理文件名冲突
                base_name = Path(file_name).stem
                ext = Path(file_name).suffix
                new_file_name = file_name
                target_path = os.path.join(target_dir, new_file_name)

                counter = 1
                while os.path.exists(target_path):
                    new_file_name = f"{base_name}_{counter}{ext}"
                    target_path = os.path.join(target_dir, new_file_name)
                    counter += 1

                # 强制移动文件
                if self.force_move(file_path, target_path):
                    moved_count += 1
                    self.stats['moved_files'] += 1

                    if moved_count % 100 == 0:
                        print(f"   已移动 {moved_count} 个文件...")
                else:
                    self.stats['errors'] += 1

            except Exception as e:
                print(f"    ❌ 错误: {os.path.basename(file_path)} -> {e}")
                self.stats['errors'] += 1

        # 第五步：清理空目录
        print("🧹 清理空目录...")
        self.clean_empty_dirs(directory)

        self.stats['end_time'] = time.time()

        # 显示结果
        self.show_results(directory)

    def clean_empty_dirs(self, directory):
        """清理空目录"""
        for root, dirs, files in os.walk(directory, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    # 如果是空目录且不是我们的分类目录，就删除
                    if (not os.listdir(dir_path) and
                            dir_name not in self.chinese_categories and
                            dir_name != '应用程序集合'):
                        os.rmdir(dir_path)
                except:
                    pass

    def show_results(self, directory):
        """显示整理结果"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print("\n" + "=" * 60)
        print("🎉 终极文件整理完成！")
        print("=" * 60)
        print(f"📊 整理统计:")
        print(f"   文件总数: {self.stats['total_files']}")
        print(f"   成功移动: {self.stats['moved_files']}")
        print(f"   应用程序文件: {self.stats['app_files']}")
        print(f"   错误数量: {self.stats['errors']}")
        print(f"   耗时: {duration:.1f} 秒")
        print()

        print("📁 新的目录结构:")
        print("-" * 40)
        for item in sorted(os.listdir(directory)):
            if os.path.isdir(os.path.join(directory, item)):
                item_count = len([f for f in os.listdir(os.path.join(directory, item))
                                  if os.path.isfile(os.path.join(directory, item, f))])
                print(f"   📂 {item}: {item_count} 个文件")

        print("=" * 60)


def get_target_directory():
    """交互式获取目标目录"""
    print("🚀 终极文件整理大师")
    print("=" * 50)
    print("⚠️  警告: 此操作将完全颠覆现有目录结构！")
    print("⚠️  但不会删除任何文件")
    print("=" * 50)

    # 显示可用驱动器
    print("可用驱动器:")
    drives = []
    for drive in range(65, 91):
        drive_letter = chr(drive) + ":\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
            print(f"   {drive_letter}")

    while True:
        user_input = input("\n请输入要整理的目录路径 (例如: D:\\): ").strip()

        if not user_input:
            print("❌ 请输入有效的路径")
            continue

        # 处理 D: 这样的输入
        if len(user_input) == 2 and user_input[1] == ':':
            target_dir = user_input + "\\"
        else:
            target_dir = user_input

        # 确保路径格式正确
        if not target_dir.endswith('\\'):
            target_dir += "\\"

        if not os.path.exists(target_dir):
            print(f"❌ 目录不存在: {target_dir}")
            continue

        if not os.path.isdir(target_dir):
            print(f"❌ 这不是一个目录: {target_dir}")
            continue

        # 最终确认
        print(f"\n✅ 目标目录: {target_dir}")
        print(f"📁 目录内容: {len(os.listdir(target_dir))} 个项目")

        confirm = input("\n⚠️  确定要完全重构此目录吗？(输入 YES 确认): ")
        if confirm.upper() == 'YES':
            return target_dir
        else:
            print("❌ 操作取消")
            sys.exit(0)


def main():
    """主函数"""
    try:
        # 获取目标目录
        target_directory = get_target_directory()

        # 创建整理器并执行
        organizer = UltimateFileOrganizer()
        organizer.organize_files(target_directory)

        print("\n💡 整理完成！所有应用程序文件保存在'应用程序集合'目录")
        print("💡 其他文件已按中文分类整理")

    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main()