import time
import pygetwindow as gw
import re


def extract():
    # 定义文件路径
    file_path = 'F:/BaiduNetdiskDownload/schedule/a.txt'

    # 初始化一个列表来保存匹配行的上一行
    previous_lines = []

    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 检查行是否包含【
            if '【' in line:
                # 如果previous_lines中有内容（即当前行不是文件的第一行），则处理上一行
                if previous_lines:
                    # 假设事件点位于上一行的末尾，这里简单地通过正则表达式查找
                    event_point = re.search(r'\d{2}:\d{2}:\d{2}$', previous_lines[-1])
                    if event_point:
                        # 如果找到了事件点，则将其与当前行合并
                        extracted_line = event_point.group() + line
                        print(extracted_line.strip())  # 输出到控制台
                        with open('extracted_lines.txt', 'a', encoding='utf-8') as extracted_file:
                            extracted_file.write(extracted_line)  # 写入新文件
                # 将当前行添加到previous_lines中，以便下一轮迭代使用
                previous_lines.append(line)
            else:
                # 如果当前行不包含【，则移除previous_lines中的最后一行（因为它不是我们感兴趣的行）
                if previous_lines:
                    previous_lines.pop()

# 关闭文件并结束程序


# 运行主函数
if __name__ == "__main__":
    extract()