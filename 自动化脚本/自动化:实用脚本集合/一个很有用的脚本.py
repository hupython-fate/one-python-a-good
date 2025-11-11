import os
import shutil
from pathlib import Path


def delete_empty_files(directory):
    """删除所有空文件"""
    print("正在扫描空文件...")
    empty_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 检查文件大小是否为0
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_path)

    # 显示并删除空文件
    if empty_files:
        print(f"找到 {len(empty_files)} 个空文件:")
        for file in empty_files:
            print(f"  删除: {file}")
            os.remove(file)
    else:
        print("未找到空文件")


def delete_empty_dirs(directory):
    """删除所有空目录（从最深层的开始）"""
    print("\n正在扫描空目录...")
    deleted_dirs = []

    # 需要多次遍历，直到没有空目录为止
    while True:
        empty_dirs_found = False

        for root, dirs, files in os.walk(directory, topdown=False):
            # 如果当前目录为空（没有文件也没有子目录）
            if not dirs and not files:
                # 避免删除根目录
                if root != directory:
                    print(f"  删除空目录: {root}")
                    os.rmdir(root)
                    deleted_dirs.append(root)
                    empty_dirs_found = True

        # 如果没有找到空目录，退出循环
        if not empty_dirs_found:
            break

    if deleted_dirs:
        print(f"删除了 {len(deleted_dirs)} 个空目录")
    else:
        print("未找到空目录")


def categorize_files(directory):
    """按文件类型分类文件"""
    print("\n正在按类型分类文件...")

    # 定义文件类型分类
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Programs': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
        'Media': ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.wav', '.flac'],
        'Code': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.json', '.xml']
    }

    # 创建分类文件夹
    for category in categories:
        category_path = os.path.join(directory, category)
        os.makedirs(category_path, exist_ok=True)

    moved_files = 0

    for root, dirs, files in os.walk(directory):
        # 跳过我们刚刚创建的分类文件夹
        if any(category in root for category in categories):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower()  # 获取文件扩展名

            # 查找对应的分类
            target_category = 'Others'  # 默认分类
            for category, extensions in categories.items():
                if file_ext in extensions:
                    target_category = category
                    break

            # 目标路径
            target_dir = os.path.join(directory, target_category)
            target_path = os.path.join(target_dir, file)

            # 移动文件（避免覆盖）
            if not os.path.exists(target_path):
                shutil.move(file_path, target_path)
                print(f"  移动: {file} -> {target_category}/")
                moved_files += 1
            else:
                print(f"  跳过（文件已存在）: {file}")

    print(f"分类完成了 {moved_files} 个文件")


def main():
    """主函数"""
    # 设置要整理的目录
    target_directory = r"D:"  # 您可以根据需要修改

    if not os.path.exists(target_directory):
        print(f"目录不存在: {target_directory}")
        return

    print(f"开始整理目录: {target_directory}")
    print("=" * 50)

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