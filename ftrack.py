import argparse
from file_tracker.core import FileTracker
import os
from tqdm import tqdm
from colorama import init, Fore, Style
from tabulate import tabulate
from file_tracker.utils import format_size, count_files

# 初始化 colorama
init()

def format_item_for_table(item):
    """格式化单个条目为表格行"""
    # 路径显示（带图标）
    filepath = item['filepath']
    type_str = "📁 " if item['filetype'] == 'directory' else "📄 "
    if item['filetype'] == 'directory':
        filepath_display = f"{Fore.GREEN}{type_str}{filepath}{Style.RESET_ALL}"
    else:
        filepath_display = f"{Fore.WHITE}{type_str}{filepath}{Style.RESET_ALL}"
    
    # 标签显示
    tags = item.get('tags', [])
    tags_str = f"{Fore.YELLOW}{', '.join(tags)}{Style.RESET_ALL}" if tags else ""
    
    # 大小显示（人类可读格式）
    size_str = format_size(item['filesize'])
    
    # 时间信息
    created = item['create_time']
    modified = item['modify_time']
    
    # 创建者显示
    creator = item['creator']
    creator_str = f"{creator['name']} ({creator['uid']})"
    
    return [
        filepath_display,
        tags_str,
        size_str,
        created,
        modified,
        creator_str
    ]

def display_results(items, title=None):
    """以表格形式显示结果"""
    if title:
        print(f"\n{title}")
    
    if not items:
        print(f"{Fore.YELLOW}No items found.{Style.RESET_ALL}")
        return
        
    table_data = [format_item_for_table(item) for item in items]
    headers = [
        "Path",
        "Tags",
        "Size",
        "Created",
        "Modified",
        "Creator"
    ]
    print(tabulate(table_data, headers=headers, tablefmt="simple", showindex=False))
    print(f"\nTotal: {Fore.WHITE}{len(items)}{Style.RESET_ALL} items")

def display_meta(meta_info):
    """以表格形式显示元数据信息"""
    if not meta_info:
        print(f"{Fore.RED}File not found in tracking database{Style.RESET_ALL}")
        return
        
    print("\nFile Metadata:")
    for section, data in meta_info.items():
        print(f"\n{Fore.CYAN}{section}:{Style.RESET_ALL}")
        section_data = [[k, f"{Fore.WHITE}{v}{Style.RESET_ALL}"] for k, v in data.items()]
        print(tabulate(section_data, tablefmt="simple"))

def process_directory(tracker, target_path, recursive=False):
    """处理目录添加逻辑"""
    print(f"Processing: {Fore.CYAN}{target_path}{Style.RESET_ALL}")
    
    if not recursive:
        return tracker.add_file(target_path)
        
    print("Calculating directory size...")
    with tqdm(desc="Scanning directory") as pbar:
        total_files = count_files(target_path)
        pbar.update(1)
    
    print(f"Found {Fore.GREEN}{total_files}{Style.RESET_ALL} files to process")
    
    processed_files = 0
    with tqdm(total=total_files, desc="Adding files") as pbar:
        for root, _, files in os.walk(target_path):
            for file in files:
                file_path = os.path.join(root, file)
                if tracker.add_file(file_path):
                    processed_files += 1
                pbar.update(1)
    
    print(f"\nSuccessfully added {Fore.GREEN}{processed_files}{Style.RESET_ALL} files")
    if processed_files < total_files:
        failed = total_files - processed_files
        print(f"Failed to add {Fore.RED}{failed}{Style.RESET_ALL} files")
    
    return processed_files > 0

def main():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()
    
    # 添加参数
    add_basic_arguments(parser)
    add_search_arguments(parser)
    add_tag_arguments(parser)
    add_remove_arguments(parser)
    add_meta_arguments(parser)
    
    # 解析参数
    args = parser.parse_args()
    
    # 检查是否有操作参数，如果没有则显示帮助信息
    if not has_operations(args):
        parser.print_help()  # 使用 parser 对象而不是 args 来打印帮助信息
        return
        
    tracker = FileTracker(db_path=args.db_path)
    handle_operations(tracker, args)

def add_basic_arguments(parser):
    """添加基本参数"""
    parser.add_argument('-a', '--add', help='Add a file or directory to track')
    parser.add_argument('-r', '--recursive', action='store_true', 
                       help='Recursively add files in directory')
    parser.add_argument('--db', dest='db_path', help='Specify database file path')
    parser.add_argument('path', nargs='?', help='Path to add (optional)')
    parser.add_argument('-l', '--list', action='store_true', 
                       help='List all tracked files')
    parser.add_argument('--update', action='store_true',
                       help='Update database: refresh file information')

def add_search_arguments(parser):
    """添加搜索相关参数"""
    parser.add_argument('-n', '--search-name', help='Search files by name')
    parser.add_argument('-t', '--search-tag', help='Search files by tag')

def add_tag_arguments(parser):
    """添加标签管理相关参数"""
    parser.add_argument('--tag', nargs=2, metavar=('FILE_PATH', 'TAG'), 
                       help='Add a tag to a file')
    parser.add_argument('--rm-tag', nargs=2, metavar=('FILE_PATH', 'TAG'),
                       help='Remove a tag from a file')

def add_remove_arguments(parser):
    """添加删除相关参数"""
    parser.add_argument('--rm', help='Remove a file or directory from tracking')
    parser.add_argument('--rm-recursive', action='store_true',
                       help='Recursively remove directory and its contents')

def add_meta_arguments(parser):
    """添加元数据相关参数"""
    parser.add_argument('--meta', help='Show detailed metadata for a file')

def has_operations(args):
    """检查是否有任何操作参数"""
    operations = {
        'path': args.path,
        'add': args.add,
        'search_name': args.search_name,
        'search_tag': args.search_tag,
        'tag': args.tag,
        'list': args.list,
        'rm': args.rm,
        'rm_tag': args.rm_tag,
        'meta': args.meta,
        'update': args.update
    }
    return any(operations.values())

def handle_operations(tracker, args):
    """处理所有操作"""
    if args.update:
        results = tracker.update_database()
        print(f"\nDatabase update results:")
        print(f"Updated: {Fore.GREEN}{results['updated']}{Style.RESET_ALL} files")
        print(f"Failed: {Fore.RED}{results['failed']}{Style.RESET_ALL} files")
        print(f"Total: {results['total']} files")
        return
        
    if args.list:
        results = tracker.list_files()
        display_results(results, "All tracked files")
        return
    
    if args.path or args.add:
        handle_add_operation(tracker, args)
    
    if args.search_name:
        handle_search_name(tracker, args.search_name)
        
    if args.search_tag:
        handle_search_tag(tracker, args.search_tag)
        
    if args.tag:
        handle_tag_operation(tracker, args.tag[0], args.tag[1])
        
    if args.rm_tag:
        handle_remove_tag_operation(tracker, args.rm_tag[0], args.rm_tag[1])

def handle_add_operation(tracker, args):
    """处理添加文件/目录操作"""
    target_path = args.path or args.add
    if os.path.isdir(target_path):
        process_directory(tracker, target_path, args.recursive)
    else:
        if tracker.add_file(target_path):
            print(f"Successfully added: {Fore.GREEN}{target_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to add: {target_path}{Style.RESET_ALL}")

def handle_search_name(tracker, name):
    """处理按名称搜索操作"""
    results = tracker.search_by_name(name)
    display_results(results, f"Search results for: {name}")

def handle_search_tag(tracker, tag):
    """处理按标签搜索操作"""
    results = tracker.search_by_tag(tag)
    display_results(results, f"Files tagged with: {tag}")

def handle_tag_operation(tracker, filepath, tag):
    """处理添加标签操作"""
    # 确保文件存在且被追踪
    if not os.path.exists(filepath):
        print(f"{Fore.RED}Error: File not found: {filepath}{Style.RESET_ALL}")
        return
        
    # 如果文件还未被追踪，先添加到追踪系统
    if not tracker.file_exists(filepath):
        if not tracker.add_file(filepath):
            print(f"{Fore.RED}Error: Could not add file to tracking system{Style.RESET_ALL}")
            return
    
    # 添加标签
    if tracker.add_tag(filepath, tag):
        print(f"Added tag '{Fore.YELLOW}{tag}{Style.RESET_ALL}' to {filepath}")
    else:
        print(f"{Fore.RED}Failed to add tag{Style.RESET_ALL}")

def handle_remove_tag_operation(tracker, filepath, tag):
    """处理移除标签操作"""
    if tracker.remove_tag(filepath, tag):
        print(f"Removed tag '{Fore.YELLOW}{tag}{Style.RESET_ALL}' from {filepath}")
    else:
        print(f"{Fore.RED}Failed to remove tag{Style.RESET_ALL}")

if __name__ == '__main__':
    main() 