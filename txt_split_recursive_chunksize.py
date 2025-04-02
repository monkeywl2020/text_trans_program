import os
import argparse
from tqdm import tqdm  # 用于显示进度条

def split_text_to_files(input_file, output_file_dir, chunk_size=250):
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用单个 # 分割问题
    questions = content.split('#')[1:]  # 去掉第一个空块
    # 将问题内容提取出来，去掉两端空白和换行
    questions = [q.strip() for q in questions if q.strip()]  # 过滤掉空块

    # 获取输入文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # 当前文件编号
    file_index = 1
    current_chunk = ''
    char_count = 0

    # 确保输出目录存在
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)

    # 遍历每个问题
    for question in questions:
        # 确保每个问题以 # 开头
        formatted_question = f"#{question}"
        question_len = len(formatted_question)
        
        # 如果当前块加上新问题会超过chunk_size，并且当前块不为空，则保存当前块
        if char_count + question_len > chunk_size and current_chunk:
            output_file = os.path.join(output_file_dir, f"{base_name}_{file_index}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(current_chunk.rstrip())  # 去掉末尾多余换行
            file_index += 1
            current_chunk = formatted_question
            char_count = question_len
        else:
            # 如果当前问题本身就超过chunk_size，则单独保存
            if question_len > chunk_size:
                if current_chunk:  # 如果当前块有内容，先保存
                    output_file = os.path.join(output_file_dir, f"{base_name}_{file_index}.txt")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(current_chunk.rstrip())  # 去掉末尾多余换行
                    file_index += 1
                # 保存当前问题
                output_file = os.path.join(output_file_dir, f"{base_name}_{file_index}.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(formatted_question.strip())
                file_index += 1
                current_chunk = ''
                char_count = 0
            else:
                # 添加到当前块，不同问题之间用两个换行符分隔
                if current_chunk:
                    current_chunk += '\n\n' + formatted_question
                    char_count += 2 + question_len  # +2 为两个换行符
                else:
                    current_chunk = formatted_question
                    char_count = question_len

    # 保存最后一个块（如果有内容）
    if current_chunk:
        output_file = os.path.join(output_file_dir, f"{base_name}_{file_index}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(current_chunk.rstrip())  # 去掉末尾多余换行

def count_files(input_dir):
    # 计算目录及其子目录下的 .txt 文件总数
    total_files = 0
    for root, _, files in os.walk(input_dir):
        total_files += sum(1 for f in files if f.endswith('.txt'))
    return total_files

def process_directory(input_dir, output_dir, chunk_size=250):
    # 计算总文件数用于进度条
    total_files = count_files(input_dir)
    
    # 遍历输入目录及其子目录，显示进度条
    file_count = 0
    with tqdm(total=total_files, desc="处理文件中", unit="file") as pbar:
        for root, dirs, files in os.walk(input_dir):
            # 计算相对路径
            relative_path = os.path.relpath(root, input_dir)
            # 对应的输出目录
            current_output_dir = os.path.join(output_dir, relative_path) if relative_path != '.' else output_dir

            # 处理当前目录下的所有 .txt 文件
            for filename in files:
                if filename.endswith('.txt'):
                    input_file = os.path.join(root, filename)
                    print(f"正在处理文件: {input_file} (块大小: {chunk_size})")
                    split_text_to_files(input_file, current_output_dir, chunk_size)
                    print(f"文件 {filename} 处理完成，输出到 {current_output_dir}")
                    file_count += 1
                    pbar.update(1)  # 更新进度条

def main():
    # 设置命令行参数
    #-------------------------------------------------------------
    # 指定输出目录和块大小（例如 ./output_folder）:
    # python txt_split_recursive_chunksize.py ./input_folder ./output_folder --chunk_size 300
    #-------------------------------------------------------------
    # 不指定输出目录（使用默认值，例如 ./input_folder_300）
    # python txt_split_recursive_chunksize.py ./input_folder --chunk_size 300
    #-------------------------------------------------------------
    # 使用默认块大小（250）和默认输出目录（例如 ./input_folder_250）：
    # python txt_split_recursive_chunksize.py ./input_folder
    #-------------------------------------------------------------
    parser = argparse.ArgumentParser(description="将文本文件按指定字符数分割并保存到新文件夹，保持目录结构")
    parser.add_argument('input_dir', help="输入文件夹路径")
    parser.add_argument('output_dir', nargs='?', default=None, help="输出文件夹路径（可选，默认使用 输入目录名称_块大小）")
    parser.add_argument('--chunk_size', type=int, default=250, help="每块的最大字符数，默认250")

    # 解析命令行参数
    args = parser.parse_args()

    # 如果未指定输出目录，使用 输入目录名称_块大小
    if args.output_dir is None:
        input_dir_name = os.path.basename(os.path.normpath(args.input_dir))
        args.output_dir = f"{input_dir_name}_{args.chunk_size}"
    
    # 确保输出目录路径是绝对路径
    args.output_dir = os.path.abspath(args.output_dir)
    print(f"输出目录: {args.output_dir}")

    # 处理目录
    process_directory(args.input_dir, args.output_dir, args.chunk_size)

if __name__ == "__main__":
    main()