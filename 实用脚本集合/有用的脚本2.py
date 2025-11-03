import os
import shutil
from pathlib import Path
import stat
import time


def delete_empty_files(directory):
    """删除所有空文件，处理权限问题"""
    print("正在扫描空文件...")
    empty_files = []
    permission_errors = []
    other_errors = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # 检查文件大小是否为0
                if os.path.getsize(file_path) == 0:
                    empty_files.append(file_path)
            except (OSError, PermissionError) as e:
                permission_errors.append((file_path, str(e)))
            except Exception as e:
                other_errors.append((file_path, str(e)))

    # 显示并删除空文件
    if empty_files:
        print(f"找到 {len(empty_files)} 个空文件:")
        deleted_count = 0
        for file in empty_files:
            try:
                # 尝试修改文件权限后再删除
                os.chmod(file, stat.S_IWRITE)
                os.remove(file)
                print(f"  ✓ 删除: {os.path.basename(file)}")
                deleted_count += 1
            except PermissionError:
                print(f"  ✗ 权限拒绝: {os.path.basename(file)}")
            except Exception as e:
                print(f"  ✗ 错误: {os.path.basename(file)} - {e}")

        print(f"成功删除 {deleted_count} 个空文件")

    # 显示错误信息
    if permission_errors:
        print(f"\n权限错误 ({len(permission_errors)} 个文件):")
        for file, error in permission_errors[:5]:  # 只显示前5个
            print(f"  {os.path.basename(file)}: {error}")

    if other_errors:
        print(f"\n其他错误 ({len(other_errors)} 个文件):")
        for file, error in other_errors[:3]:
            print(f"  {os.path.basename(file)}: {error}")


def delete_empty_dirs(directory):
    """删除所有空目录（从最深层的开始），处理权限问题"""
    print("\n正在扫描空目录...")
    deleted_dirs = []
    error_dirs = []

    max_attempts = 3
    for attempt in range(max_attempts):
        empty_dirs_found = False

        for root, dirs, files in os.walk(directory, topdown=False):
            # 跳过一些系统目录
            if any(skip in root for skip in ['$Recycle.Bin', 'System Volume Information']):
                continue

            # 如果当前目录为空（没有文件也没有子目录）
            if not dirs and not files:
                # 避免删除根目录和重要目录
                if root != directory and not any(protected in root for protected in ['Windows', 'Program Files']):
                    try:
                        os.rmdir(root)
                        print(f"  ✓ 删除空目录: {os.path.basename(root)}")
                        deleted_dirs.append(root)
                        empty_dirs_found = True
                    except (OSError, PermissionError) as e:
                        error_dirs.append((root, str(e)))
                        # 尝试修改权限
                        try:
                            os.chmod(root, stat.S_IWRITE)
                            os.rmdir(root)
                            print(f"  ✓ 删除空目录(修改权限后): {os.path.basename(root)}")
                            deleted_dirs.append(root)
                            empty_dirs_found = True
                        except:
                            pass

        # 如果没有找到空目录，退出循环
        if not empty_dirs_found:
            break

        print(f"  第 {attempt + 1} 轮扫描完成，找到 {len([d for d in deleted_dirs if d])} 个空目录")
        time.sleep(1)  # 稍作延迟

    if deleted_dirs:
        print(f"总共删除了 {len(deleted_dirs)} 个空目录")
    else:
        print("未找到空目录")

    if error_dirs:
        print(f"无法删除的目录 ({len(error_dirs)} 个):")
        for dir_path, error in error_dirs[:5]:
            print(f"  {os.path.basename(dir_path)}: {error}")


def categorize_files(directory):
    """按文件类型分类文件，跳过系统文件"""
    print("\n正在按类型分类文件...")

    # 定义文件类型分类
    categories = {
        'Images图片文件': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
        'Documents文档文件': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.md'],
        'Archives压缩文件': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'Programs程序文件': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
        'Media媒体文件': ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.wav', '.flac', '.aac', '.m4a'],
        'Code代码文件': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.json', '.xml', '.yml', '.yaml'],
        'Data数据文件': ['.csv', '.tsv', '.sql', '.db', '.sqlite'],
        'Fonts字体文件': ['.ttf', '.otf', '.woff', '.woff2']
    }

    # 跳过这些系统目录
    skip_dirs = {'$Recycle.Bin', 'System Volume Information', 'Windows', 'Program Files', 'ProgramData'}

    # 创建分类文件夹
    for category in categories:
        category_path = os.path.join(directory, category)
        os.makedirs(category_path, exist_ok=True)

    moved_files = 0
    error_files = 0

    for root, dirs, files in os.walk(directory):
        # 跳过系统目录和我们创建的分类文件夹
        current_dir = os.path.basename(root)
        if (any(skip in root for skip in skip_dirs) or
                any(category in root for category in categories)):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower()

            # 跳过一些系统文件
            if file in ['desktop.ini', 'thumbs.db']:
                continue

            # 查找对应的分类
            target_category = 'Others'
            for category, extensions in categories.items():
                if file_ext in extensions:
                    target_category = category
                    break

            # 目标路径
            target_dir = os.path.join(directory, target_category)

            try:
                # 处理文件名冲突
                base_name = Path(file).stem
                counter = 0
                new_file_name = file
                target_path = os.path.join(target_dir, new_file_name)

                while os.path.exists(target_path):
                    counter += 1
                    new_file_name = f"{base_name}_{counter}{file_ext}"
                    target_path = os.path.join(target_dir, new_file_name)

                # 移动文件
                shutil.move(file_path, target_path)
                print(f"  ✓ 移动: {file} -> {target_category}/")
                moved_files += 1

            except Exception as e:
                print(f"  ✗ 错误移动: {file} - {e}")
                error_files += 1

    print(f"\n分类完成: 成功移动 {moved_files} 个文件, 失败 {error_files} 个文件")


def analyze_directory(directory):
    """分析目录内容"""
    print("正在分析目录内容...")

    file_types = {}
    total_size = 0
    total_files = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower() or '无扩展名'

            try:
                size = os.path.getsize(file_path)
                total_size += size
                total_files += 1

                if file_ext in file_types:
                    file_types[file_ext]['count'] += 1
                    file_types[file_ext]['size'] += size
                else:
                    file_types[file_ext] = {'count': 1, 'size': size}
            except:
                pass

    print(f"\n目录分析结果:")
    print(f"总文件数: {total_files}")
    print(f"总大小: {total_size / (1024 * 1024):.2f} MB")
    print(f"\n文件类型分布:")
    for ext, info in sorted(file_types.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
        print(f"  {ext:8} {info['count']:4} 个文件, {info['size'] / (1024 * 1024):8.2f} MB")


def main():
    """主函数"""
    # 设置要整理的目录
    target_directory = r"D:"  # 您可以根据需要修改

    if not os.path.exists(target_directory):
        print(f"目录不存在: {target_directory}")
        return

    print(f"开始整理目录: {target_directory}")
    print("=" * 50)

    # 先分析目录
    analyze_directory(target_directory)

    # 确认是否继续
    response = input("\n是否继续整理？(y/n): ")
    if response.lower() != 'y':
        print("操作已取消")
        return

    try:
        # 执行三个步骤
        delete_empty_files(target_directory)
        delete_empty_dirs(target_directory)
        categorize_files(target_directory)

        print("\n" + "=" * 50)
        print("文件整理完成！")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()