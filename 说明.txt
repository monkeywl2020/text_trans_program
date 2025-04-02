----1:
base64_2_utf8.py  作用：base64内容转成 utf8的，用于llama-index的docstore文档
# 命令使用示范
python base64_2_utf8.py docstore.json


----2：markitdown_path.py   作用：将word的文档转成markdown格式。
# 命令使用示范，遍历目录+子目录
python convert_doc_to_md.py /home/user/documents /home/user/markdown_output


----3：txt_gb2312_to_utf8.py   作用：将 gb2312的txt文档转成utf8格式。
# 命令使用示范，遍历目录+子目录
python convert_doc_to_md.py /home/user/documents /home/user/markdown_output


----4：txt_gb2312_to_utf8_add_No.py 作用：将 gb2312的txt文档转成utf8格式。同时将问题根据问题块添加序号
# 命令使用示范
python txt_gb2312_to_utf8_add_No.py 


----5：markitdown_path.py  作用： 批量转换文档目录下的word格式转成 markdown格式
# 命令使用示范
 python convert_doc_to_md.py /home/user/documents /home/user/markdown_output
 
----6：get_request_from_txt.py 作用： 读取txt文件，将其中的 问题部分获取出来。
# 格式1 & 格式2：匹配“问题：”开头，提取整行
# 格式3：匹配“问：”开头，提取整行
# 格式4：匹配“数字.”开头的问题（已有逻辑保留）

# 命令使用示范
python extract_questions.py /path/to/input/folder /path/to/output/folder

----7：remove_python_comments.py 作用： 批量转去除py中的 #中文注释
# 命令使用示范
python remove_comments.py ./source ./output

----8： txt_split_recursive_chunksize.py 作用： 批量将文件夹中的文本按照 chunk_size 大小的中文文字进行切分文档。
注意，一个问答块超过了这个大小不会被拆分。 问题是通过 两个 #来拆分的
# 命令使用示范
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

