import os
import shutil
from pathlib import Path
import stat
import time


def safe_move_file(src_path, dst_dir, filename):
    """安全移动文件，处理长路径和特殊字符"""
    try:
        # 确保目标目录存在
        os.makedirs(dst_dir, exist_ok=True)

        # 处理长文件名 - 使用短路径方法
        if len(filename) > 100:  # 如果文件名太长
            file_ext = Path(filename).suffix
            file_stem = Path(filename).stem
            # 截断文件名但保留扩展名
            if len(file_stem) > 50:
                file_stem = file_stem[:50] + "_truncated"
            filename = file_stem + file_ext

        dst_path = os.path.join(dst_dir, filename)

        # 处理目标路径冲突
        counter = 1
        base_name = Path(filename).stem
        file_ext = Path(filename).suffix

        while os.path.exists(dst_path):
            new_filename = f"{base_name}_{counter}{file_ext}"
            dst_path = os.path.join(dst_dir, new_filename)
            counter += 1
            if counter > 100:  # 防止无限循环
                break

        # 使用 shutil.move 而不是 os.rename，它更健壮
        shutil.move(src_path, dst_path)
        return True, None
    except Exception as e:
        return False, str(e)


def categorize_files_safe(directory):
    """按文件类型分类文件，增强错误处理"""
    print("\n正在按类型分类文件...")

    # 定义文件类型分类
    categories = {
        'Images图片文件': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.ico'],
        'Documents文档文件': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.md'],
        'Archives压缩文件': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'Programs程序文件': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage', '.bat', '.cmd', '.ps1'],
        'Media媒体文件': ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.wav', '.flac', '.aac', '.m4a'],
        'Code代码文件': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.json', '.xml', '.yml', '.yaml'],
        'Data数据文件': ['.csv', '.tsv', '.sql', '.db', '.sqlite', '.dat'],
        'Fonts字体文件': ['.ttf', '.otf', '.woff', '.woff2'],
        'System_Files': ['.dll', '.sys', '.drv', '.ocx', '.cpl'],
        'Headers头文件': ['.h', '.hpp', '.hxx']  # 专门处理头文件
    }

    # 跳过这些系统目录
    skip_dirs = {
        '$Recycle.Bin', 'System Volume Information', 'Windows',
        'Program Files', 'ProgramData', 'Recovery'
    }

    # 创建分类文件夹
    for category in categories:
        category_path = os.path.join(directory, category)
        os.makedirs(category_path, exist_ok=True)

    moved_files = 0
    error_files = 0
    skipped_files = 0

    # 先扫描所有文件
    all_files = []
    for root, dirs, files in os.walk(directory):
        # 跳过系统目录和我们创建的分类文件夹
        if (any(skip in root for skip in skip_dirs) or
                any(category in root for category in categories)):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            all_files.append((root, file, file_path))

    print(f"找到 {len(all_files)} 个需要处理的文件")

    # 分批处理文件
    batch_size = 100
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i + batch_size]
        print(f"处理批次 {i // batch_size + 1}/{(len(all_files) - 1) // batch_size + 1}...")

        for root, file, file_path in batch:
            file_ext = Path(file).suffix.lower()

            # 跳过一些系统文件
            if file.lower() in ['desktop.ini', 'thumbs.db', 'autorun.inf']:
                skipped_files += 1
                continue

            # 查找对应的分类
            target_category = 'Others'
            for category, extensions in categories.items():
                if file_ext in extensions:
                    target_category = category
                    break

            # 目标路径
            target_dir = os.path.join(directory, target_category)

            success, error_msg = safe_move_file(file_path, target_dir, file)

            if success:
                moved_files += 1
                if moved_files % 50 == 0:  # 每50个文件显示一次进度
                    print(f"  已移动 {moved_files} 个文件...")
            else:
                error_files += 1
                # 只显示前10个错误，避免输出太多
                if error_files <= 10:
                    print(f"  ✗ 错误移动: {file} - {error_msg}")

    print(f"\n分类完成:")
    print(f"  ✓ 成功移动: {moved_files} 个文件")
    print(f"  ✗ 移动失败: {error_files} 个文件")
    print(f"  ⚠ 跳过文件: {skipped_files} 个文件")

    # 如果有很多错误，提供建议
    if error_files > 0:
        print(f"\n建议:")
        print("  1. 某些文件可能被系统锁定，请关闭所有程序后重试")
        print("  2. 文件名或路径可能过长，建议手动处理这些文件")
        print("  3. 可以尝试以管理员身份运行此脚本")


def delete_empty_files(directory):
    """删除所有空文件，处理权限问题"""
    print("正在扫描空文件...")
    empty_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getsize(file_path) == 0:
                    empty_files.append(file_path)
            except:
                pass

    if empty_files:
        print(f"找到 {len(empty_files)} 个空文件")
        deleted_count = 0
        for file in empty_files:
            try:
                os.remove(file)
                deleted_count += 1
            except:
                pass
        print(f"成功删除 {deleted_count} 个空文件")
    else:
        print("未找到空文件")


def main_optimized():
    """优化的主函数"""
    target_directory = r"D:"

    if not os.path.exists(target_directory):
        print(f"目录不存在: {target_directory}")
        return

    print(f"开始整理目录: {target_directory}")
    print("=" * 50)

    try:
        # 只执行分类功能，跳过空文件删除（可能引起权限问题）
        categorize_files_safe(target_directory)

        print("\n" + "=" * 50)
        print("文件整理完成！")
        print("\n注意: 空文件删除功能已跳过，以避免权限问题")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main_optimized()