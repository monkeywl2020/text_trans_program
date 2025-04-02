import os
from markitdown import MarkItDown
from loguru import logger
import argparse
from tqdm import tqdm

def convert_to_markdown(input_dir, output_dir):
    """
    遍历指定目录，将所有 .docx 和 .doc 文件转换为 Markdown 格式，并显示进度条。
    
    参数:
        input_dir (str): 输入目录路径
        output_dir (str): 输出目录路径
    """
    # 确保输入目录存在
    if not os.path.exists(input_dir):
        logger.error(f"输入目录不存在: {input_dir}")
        raise FileNotFoundError(f"输入目录不存在: {input_dir}")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化 MarkItDown 实例
    md_converter = MarkItDown()
    
    # 支持的文件扩展名
    supported_extensions = ('.docx', '.doc')
    
    # 统计需要处理的文件总数
    total_files = sum(
        len([f for f in files if f.lower().endswith(supported_extensions)])
        for _, _, files in os.walk(input_dir)
    )
    
    # 如果没有符合条件的文件，直接返回
    if total_files == 0:
        logger.info("没有找到 .docx 或 .doc 文件需要转换")
        print("没有找到需要转换的文件")
        return
    
    # 使用 tqdm 显示进度条
    with tqdm(total=total_files, desc="转换进度", unit="file") as pbar:
        # 遍历目录
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    input_path = os.path.join(root, file)
                    # 构造输出文件路径，保持相对目录结构
                    relative_path = os.path.relpath(root, input_dir)
                    output_subdir = os.path.join(output_dir, relative_path)
                    os.makedirs(output_subdir, exist_ok=True)
                    
                    output_file = os.path.splitext(file)[0] + '.md'
                    output_path = os.path.join(output_subdir, output_file)
                    
                    try:
                        # 执行转换
                        result = md_converter.convert(input_path)
                        # 将转换结果写入文件
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(result.text_content)
                        logger.info(f"成功转换: {input_path} -> {output_path}")
                    except Exception as e:
                        logger.error(f"转换失败: {input_path} - 错误: {str(e)}")
                    finally:
                        # 更新进度条
                        pbar.update(1)

def main():
    # 配置命令行参数解析
    # python convert_doc_to_md.py /home/user/documents /home/user/markdown_output
    parser = argparse.ArgumentParser(description="将指定目录中的 .docx 和 .doc 文件转换为 Markdown 格式")
    parser.add_argument("input_dir", help="输入目录路径")
    parser.add_argument("output_dir", help="输出目录路径")
    
    # 解析用户输入
    args = parser.parse_args()
    
    # 调用转换函数
    convert_to_markdown(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()