import os
import re
import argparse
from tqdm import tqdm

def remove_chinese_comments(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # 情况1：以 # 开头，前面只有空白字符或无字符
        if re.match(r'^\s*#', line):
            if re.search(r'[\u4e00-\u9fff]', line):
                continue  # 含中文的整行注释移除
            new_lines.append(line)
        else:
            # 情况2：查找行内 #，前面有内容
            match = re.search(r'^(.*?)(#.*)$', line)
            if match:
                code_part = match.group(1).rstrip()
                comment_part = match.group(2)
                # 检查代码部分是否为空，且注释部分是否含双引号或三引号
                if code_part.strip() and not re.search(r'"""|\'\'\'|"', comment_part):
                    if re.search(r'[\u4e00-\u9fff]', comment_part):
                        # 前面有代码，注释不含引号且有中文，只保留代码部分
                        new_lines.append(code_part)
                    else:
                        new_lines.append(line)  # 不含中文的注释保留
                else:
                    new_lines.append(line)  # 含引号的（可能是字符串）保留
            else:
                new_lines.append(line)  # 没有 # 的行保留

    new_content = '\n'.join(new_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def get_all_py_files(input_dir):
    py_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

def process_directory(input_dir, base_output_dir):
    input_dir_name = os.path.basename(os.path.normpath(input_dir))
    output_dir = os.path.join(base_output_dir, input_dir_name + '_deploy')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    py_files = get_all_py_files(input_dir)
    
    with tqdm(total=len(py_files), desc="Processing files", unit="file") as pbar:
        for input_path in py_files:
            rel_path = os.path.relpath(input_path, input_dir)
            output_path = os.path.join(output_dir, rel_path)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            remove_chinese_comments(input_path, output_path)
            file_name = os.path.basename(input_path)
            pbar.set_description(f"Processing: {file_name}")
            pbar.update(1)
    
    return output_dir

def main():
    # 命令行参数解析
    # python remove_comments.py ./source ./output
    parser = argparse.ArgumentParser(description='Remove Chinese comments starting with # from Python files')
    parser.add_argument('input_dir', help='Input directory containing Python files')
    parser.add_argument('output_dir', help='Base output directory for processed files')
    args = parser.parse_args()
    
    final_output_dir = process_directory(args.input_dir, args.output_dir)
    print(f"\nProcessing complete. Output saved to: {final_output_dir}")

if __name__ == "__main__":
    main()

