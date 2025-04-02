import chardet
import codecs
import sys

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_to_utf8(file_path, original_encoding):
    """将文件从指定编码转换为UTF-8"""
    with codecs.open(file_path, 'r', encoding=original_encoding) as f:
        content = f.read()
    return content

def process_text_file(input_file):
    # 检查文件是否存在
    try:
        with open(input_file, 'rb'):
            pass
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    # 检测文件编码
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")

    # 读取文件内容
    if encoding.lower() in ['gb2312', 'gbk', 'gb18030']:
        content = convert_to_utf8(input_file, encoding)
    else:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Error: Unable to decode file with UTF-8, assuming {encoding}.")
            content = convert_to_utf8(input_file, encoding)

    # 分割成行
    lines = content.splitlines()

    # 处理问题编号
    question_count = 0
    new_lines = []
    for line in lines:
        if line.startswith('清远院区专属问题：'):
            question_count += 1
            new_line = f'#清远院区专属问题{question_count}：' + line[4:]  # 替换 "#问题：" 为 "#问题X："
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # 生成新文件名（原文件名 + #）
    output_file = input_file.rsplit('.', 1)[0] + '#.' + input_file.rsplit('.', 1)[1]

    # 将修改后的内容保存为新文件（UTF-8编码）
    with codecs.open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    print(f"Processed file saved as: {output_file}")

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    # 获取命令行输入的文件名
    input_file = sys.argv[1]
    process_text_file(input_file)