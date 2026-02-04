#!/usr/bin/env python3
"""
目录扁平化大师 - Directory Flattening Master
专门处理深层嵌套和冗余目录结构
"""

import os
import sys
import shutil
import logging
from pathlib import Path
import time


class DirectoryFlatteningMaster:
    def __init__(self, verbose=False, dry_run=False, log_file=None):
        self.verbose = verbose
        self.dry_run = dry_run
        self.stats = {
            'scanned_dirs': 0,
            'flattened_dirs': 0,
            'moved_files': 0,
            'removed_empty_dirs': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        """配置日志系统"""
        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[]
        )

        self.logger = logging.getLogger('DirectoryFlatteningMaster')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if self.verbose else logging.WARNING)
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)

        self.logger.propagate = False

    def analyze_directory_structure(self, directory):
        """分析目录结构，识别冗余嵌套"""
        redundant_paths = []

        for root, dirs, files in os.walk(directory):
            self.stats['scanned_dirs'] += 1

            # 跳过已经处理过的目录和系统目录
            dirs[:] = [d for d in dirs if not any(x in d for x in ['(扁平化)', '(已处理)'])]

            # 情况1: 单文件目录 - 目录中只有一个文件，没有子目录
            if len(files) == 1 and len(dirs) == 0:
                redundant_paths.append({
                    'type': 'single_file_dir',
                    'path': root,
                    'file_count': 1,
                    'depth': root.count(os.sep)
                })

            # 情况2: 单子目录 - 目录中只有一个子目录，没有文件
            elif len(dirs) == 1 and len(files) == 0:
                redundant_paths.append({
                    'type': 'single_subdir',
                    'path': root,
                    'file_count': 0,
                    'depth': root.count(os.sep)
                })

            # 情况3: 深层嵌套 - 深度超过3层且文件很少
            depth = root.count(os.sep) - directory.count(os.sep)
            if depth >= 3 and (len(files) + len(dirs)) <= 5:
                redundant_paths.append({
                    'type': 'deep_nesting',
                    'path': root,
                    'file_count': len(files),
                    'dir_count': len(dirs),
                    'depth': depth
                })

        return redundant_paths

    def should_flatten_directory(self, dir_info, parent_dir):
        """判断是否应该扁平化这个目录"""
        dir_path = dir_info['path']

        # 跳过根目录和系统目录
        if dir_path == parent_dir:
            return False

        system_dirs = {'windows', 'program files', 'programdata', 'system32'}
        dir_name = os.path.basename(dir_path).lower()
        if any(system_dir in dir_name for system_dir in system_dirs):
            return False

        # 根据不同类型决定
        if dir_info['type'] == 'single_file_dir':
            return True
        elif dir_info['type'] == 'single_subdir':
            return True
        elif dir_info['type'] == 'deep_nesting' and dir_info['depth'] >= 3:
            return True

        return False

    def flatten_single_file_directory(self, dir_path, target_dir):
        """扁平化单文件目录"""
        try:
            files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
            if len(files) != 1:
                return False, "不是单文件目录"

            file_name = files[0]
            source_path = os.path.join(dir_path, file_name)

            # 生成新文件名（包含原目录信息）
            dir_name = os.path.basename(dir_path)
            new_file_name = f"{dir_name}_{file_name}"
            target_path = os.path.join(target_dir, new_file_name)

            # 处理文件名冲突
            counter = 1
            base_name = Path(new_file_name).stem
            ext = Path(new_file_name).suffix
            while os.path.exists(target_path):
                new_file_name = f"{base_name}_{counter}{ext}"
                target_path = os.path.join(target_dir, new_file_name)
                counter += 1

            if self.dry_run:
                self.logger.info(f"[模拟] 移动文件: {file_name} -> {new_file_name}")
                # 模拟删除空目录
                if len(os.listdir(dir_path)) == 1:  # 只有这一个文件
                    self.logger.info(f"[模拟] 删除空目录: {dir_path}")
                return True, "模拟完成"
            else:
                # 移动文件
                shutil.move(source_path, target_path)
                self.stats['moved_files'] += 1

                # 删除空目录
                if len(os.listdir(dir_path)) == 0:
                    os.rmdir(dir_path)
                    self.stats['removed_empty_dirs'] += 1

                return True, "扁平化完成"

        except Exception as e:
            return False, f"错误: {e}"

    def flatten_single_subdir_directory(self, dir_path, target_dir):
        """扁平化单子目录结构"""
        try:
            subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
            if len(subdirs) != 1:
                return False, "不是单子目录"

            subdir_path = os.path.join(dir_path, subdirs[0])

            # 移动所有子目录中的内容到当前目录
            moved_count = 0
            for item in os.listdir(subdir_path):
                source = os.path.join(subdir_path, item)
                target = os.path.join(dir_path, item)

                # 处理名称冲突
                counter = 1
                base_name = Path(item).stem
                ext = Path(item).suffix if os.path.isfile(source) else ""
                new_target = target
                while os.path.exists(new_target):
                    if os.path.isfile(source):
                        new_item = f"{base_name}_{counter}{ext}"
                    else:
                        new_item = f"{base_name}_{counter}"
                    new_target = os.path.join(dir_path, new_item)
                    counter += 1

                if self.dry_run:
                    self.logger.info(f"[模拟] 移动: {item} -> {os.path.basename(dir_path)}/")
                else:
                    shutil.move(source, new_target)
                    moved_count += 1

            if not self.dry_run:
                self.stats['moved_files'] += moved_count

                # 删除空的子目录
                if len(os.listdir(subdir_path)) == 0:
                    os.rmdir(subdir_path)
                    self.stats['removed_empty_dirs'] += 1

            return True, f"移动了 {moved_count} 个项目"

        except Exception as e:
            return False, f"错误: {e}"

    def flatten_deep_nesting(self, dir_path, target_dir, max_depth=2):
        """扁平化深层嵌套目录"""
        try:
            # 收集所有文件
            all_files = []
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算相对路径用于新文件名
                    rel_path = os.path.relpath(root, dir_path)
                    if rel_path == '.':
                        new_name = file
                    else:
                        # 将路径信息编码到文件名中
                        path_part = rel_path.replace(os.sep, '_')
                        new_name = f"{path_part}_{file}"
                    all_files.append((file_path, new_name))

            moved_count = 0
            for source_path, new_name in all_files:
                target_path = os.path.join(target_dir, new_name)

                # 处理文件名冲突
                counter = 1
                base_name = Path(new_name).stem
                ext = Path(new_name).suffix
                while os.path.exists(target_path):
                    new_name = f"{base_name}_{counter}{ext}"
                    target_path = os.path.join(target_dir, new_name)
                    counter += 1

                if self.dry_run:
                    self.logger.info(f"[模拟] 移动: {os.path.basename(source_path)} -> {new_name}")
                else:
                    shutil.move(source_path, target_path)
                    moved_count += 1

            if not self.dry_run:
                self.stats['moved_files'] += moved_count

                # 删除空目录（从最深層开始）
                for root, dirs, files in os.walk(dir_path, topdown=False):
                    if root != dir_path and len(os.listdir(root)) == 0:
                        os.rmdir(root)
                        self.stats['removed_empty_dirs'] += 1

            return True, f"移动了 {moved_count} 个文件"

        except Exception as e:
            return False, f"错误: {e}"

    def process_redundant_directories(self, directory, redundant_paths):
        """处理所有冗余目录"""
        print("🔄 开始扁平化冗余目录...")

        processed = 0
        errors = 0

        # 按深度排序，先处理最深层的
        redundant_paths.sort(key=lambda x: x['depth'], reverse=True)

        for dir_info in redundant_paths:
            if not self.should_flatten_directory(dir_info, directory):
                continue

            dir_path = dir_info['path']
            parent_dir = os.path.dirname(dir_path)

            self.logger.info(f"处理: {dir_path} ({dir_info['type']})")

            success = False
            message = ""

            if dir_info['type'] == 'single_file_dir':
                success, message = self.flatten_single_file_directory(dir_path, parent_dir)
            elif dir_info['type'] == 'single_subdir':
                success, message = self.flatten_single_subdir_directory(dir_path, parent_dir)
            elif dir_info['type'] == 'deep_nesting':
                success, message = self.flatten_deep_nesting(dir_path, parent_dir)

            if success:
                processed += 1
                self.stats['flattened_dirs'] += 1
                self.logger.info(f"  ✅ 成功: {message}")
            else:
                errors += 1
                self.stats['errors'] += 1
                self.logger.info(f"  ❌ 失败: {message}")

        return processed, errors

    def print_analysis_report(self, redundant_paths):
        """打印分析报告"""
        print("\n📊 目录结构分析报告:")
        print("=" * 60)

        by_type = {}
        for item in redundant_paths:
            if item['type'] not in by_type:
                by_type[item['type']] = []
            by_type[item['type']].append(item)

        for type_name, items in by_type.items():
            type_desc = {
                'single_file_dir': '单文件目录',
                'single_subdir': '单子目录',
                'deep_nesting': '深层嵌套'
            }.get(type_name, type_name)

            print(f"  {type_desc}: {len(items)} 个")
            for item in items[:3]:  # 显示前3个例子
                depth = item.get('depth', 0)
                file_count = item.get('file_count', 0)
                print(f"    - {os.path.basename(item['path'])} (深度: {depth}, 文件: {file_count})")
            if len(items) > 3:
                print(f"    ... 还有 {len(items) - 3} 个")

        print("=" * 60)

    def print_summary(self):
        """打印统计摘要"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print("\n" + "=" * 60)
        print("🎯 目录扁平化完成摘要")
        print("=" * 60)
        print(f"📁 扫描目录总数: {self.stats['scanned_dirs']:,}")
        print(f"🔄 扁平化目录数: {self.stats['flattened_dirs']:,}")
        print(f"📄 移动文件数量: {self.stats['moved_files']:,}")
        print(f"🗑️  删除空目录数: {self.stats['removed_empty_dirs']:,}")
        print(f"❌ 处理错误数: {self.stats['errors']:,}")
        print(f"⏱️  总耗时: {duration:.2f} 秒")

        if self.dry_run:
            print("💡 模式: 模拟运行（未实际操作）")
        else:
            print("💡 模式: 实际执行")
        print("=" * 60)

    def flatten_directories(self, directory):
        """主扁平化函数"""
        self.stats['start_time'] = time.time()

        print(f"🎯 开始分析目录结构: {directory}")

        # 分析目录结构
        redundant_paths = self.analyze_directory_structure(directory)

        if not redundant_paths:
            print("✅ 未发现需要扁平化的冗余目录")
            return

        # 显示分析报告
        self.print_analysis_report(redundant_paths)

        # 处理冗余目录
        processed, errors = self.process_redundant_directories(directory, redundant_paths)

        self.stats['end_time'] = time.time()

        # 打印结果
        self.print_summary()


# 交互式部分（与之前类似，略去重复代码）
def get_user_directory():
    """交互式获取目录"""
    print("🚀 目录扁平化大师 - 目录选择")
    print("=" * 50)

    # ... (与之前相同的目录选择代码)
    return "D:\\"  # 示例返回


def get_flattening_options():
    """获取扁平化选项"""
    print("\n🛠️  扁平化选项设置")
    print("-" * 30)

    dry_run = input("启用模拟运行模式？(y/N): ").strip().lower() in ['y', 'yes']
    verbose = input("启用详细输出模式？(y/N): ").strip().lower() in ['y', 'yes']

    return dry_run, verbose


def main():
    """主函数"""
    print("=" * 60)
    print("📁 目录扁平化大师 - Directory Flattening Master")
    print("=" * 60)

    try:
        target_directory = get_user_directory()
        dry_run, verbose = get_flattening_options()

        print(f"\n📋 开始处理: {target_directory}")

        flattener = DirectoryFlatteningMaster(
            verbose=verbose,
            dry_run=dry_run,
            log_file="directory_flattening.log"
        )

        flattener.flatten_directories(target_directory)

        print(f"\n✅ 目录扁平化完成！")

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main()