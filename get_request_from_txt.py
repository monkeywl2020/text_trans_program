import os
import sys
import re
from loguru import logger

# 配置 loguru，输出到控制台
logger.remove()  # 移除默认配置
logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", colorize=True)

def extract_questions(file_path):
    """从单个文件中提取问题部分"""
    questions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # 格式1 & 格式2：匹配“问题：”开头，提取整行
            pattern1 = r'^问题：(.+)$'  # 匹配“问题：”开头的一整行
            matches1 = re.findall(pattern1, content, re.MULTILINE)

            # 格式3：匹配“问：”开头，提取整行
            pattern2 = r'^问：(.+)$'  # 匹配“问：”开头的一整行
            matches2 = re.findall(pattern2, content, re.MULTILINE)

            # 格式4：匹配“数字.”开头的问题（已有逻辑保留）
            pattern3 = r'^\d+\.\s*(.+?)(?=\n回答：|\n\d+\.|$)'  # 以数字加点开头
            matches3 = re.findall(pattern3, content, re.MULTILINE | re.DOTALL)

            # 合并所有格式的问题
            for match in matches1:
                question = match.strip()
                if question:
                    questions.append(question)
            for match in matches2:
                question = match.strip()
                if question and question not in questions:  # 避免重复
                    questions.append(question)
            for match in matches3:
                question = match.strip()
                if question and question not in questions:  # 避免重复
                    questions.append(question)

    except Exception as e:
        logger.error(f"读取文件 {file_path} 时出错: {e}")
    return questions

def process_folder(input_folder, output_folder):
    """遍历输入文件夹及其子文件夹，处理所有txt文件，并将结果保存到输出文件夹"""
    if not os.path.isdir(input_folder):
        logger.error(f"{input_folder} 不是一个有效的文件夹路径")
        return

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹及其子文件夹
    for root, _, files in os.walk(input_folder):
        # 计算相对路径并创建对应的输出子文件夹
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        os.makedirs(output_subfolder, exist_ok=True)

        for file_name in files:
            if file_name.lower().endswith('.txt'):
                input_file_path = os.path.join(root, file_name)
                output_file_path = os.path.join(output_subfolder, f"questions_{file_name}")
                logger.info(f"处理文件: {input_file_path}")
                
                questions = extract_questions(input_file_path)
                if questions:
                    # 将提取的问题写入输出文件，每个文件从1开始编号
                    try:
                        with open(output_file_path, 'w', encoding='utf-8') as output_file:
                            for idx, question in enumerate(questions, 1):  # 从1开始编号
                                output_line = f"{idx}. {question}\n"
                                output_file.write(output_line)
                                logger.info(f"{output_line.strip()} (已写入 {output_file_path})")
                    except Exception as e:
                        logger.error(f"写入文件 {output_file_path} 时出错: {e}")
                else:
                    logger.warning(f"在 {input_file_path} 中未找到任何问题")

def main():
    # 检查命令行参数
    # 例子：
    # python extract_questions.py /path/to/input/folder /path/to/output/folder
    if len(sys.argv) != 3:
        logger.error("用法: python script.py <输入文件夹路径> <输出文件夹路径>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    logger.info(f"输入文件夹: {input_folder}")
    logger.info(f"输出文件夹: {output_folder}")
    process_folder(input_folder, output_folder)
    logger.info("处理完成")

if __name__ == "__main__":
    main()