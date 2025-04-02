import os
import argparse
import chardet

# 定义转换函数
def convert_to_utf8(input_file, output_file):
    with open(input_file, 'r', encoding='gb2312') as infile:
        content = infile.read()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

# 判断文件编码是否为UTF-8
def is_utf8_encoded(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding.lower() == 'utf-8'

# 批量转换函数
def batch_convert(folder_path, output_folder):
    # 遍历指定文件夹
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # 只处理txt文件
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(output_folder, filename)
            
            # 检查文件编码是否为UTF-8
            if is_utf8_encoded(input_file):
                print(f"{input_file} is already in UTF-8 encoding. Skipping...")
            else:
                print(f"Converting {input_file}...")
                convert_to_utf8(input_file, output_file)
                print(f"Converted {input_file} to UTF-8.")

# 主函数
def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Batch convert .txt files from GB2312 to UTF-8 encoding.")
    parser.add_argument('folder_path', type=str, help="The folder path containing .txt files to convert.")
    
    args = parser.parse_args()
    
    folder_path = args.folder_path
    
    # 检查输入的文件夹路径是否有效
    if os.path.isdir(folder_path):
        # 创建新的输出文件夹，名称为原文件夹名 + 'utf8'
        output_folder = folder_path + '_utf8'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 调用批量转换函数
        batch_convert(folder_path, output_folder)
    else:
        print(f"The specified path '{folder_path}' is not a valid folder.")

# 启动程序
if __name__ == "__main__":
    main()
