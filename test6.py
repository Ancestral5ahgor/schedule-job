import re

# 定义文件路径
file_path = 'F:/BaiduNetdiskDownload/schedule/a.txt'

# 读取文件并逐行处理
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 用于存储上一个时间戳和对应的内容
previous_timestamp = None
content_with_brackets = None

# 遍历文件中的所有行
for line in lines:
    # 检查行是否包含【】
    if '【' in line and '】' in line:
        # 如果包含【】，则保存这一行
        content_with_brackets = line.strip()
    else:
        # 检查是否有时间戳格式（5-2 23:21:04）
        timestamp_match = re.search(r'(\d+-\d+ \d{2}:\d{2}:\d{2})', line)
        if timestamp_match:
            # 如果有时间戳，且之前保存了带有【】的内容，则输出时间戳和内容
            if content_with_brackets:
                print(f"AOC在{previous_timestamp}发布了以下信息：")
                print(f"{content_with_brackets}")
                print()  # 输出一个空行以便于区分不同的匹配项
            # 更新上一个时间戳
            previous_timestamp = timestamp_match.group(1)
            # 重置带有【】的内容，等待下一个匹配项
            content_with_brackets = None

# 如果文件最后一行是带有【】的行，确保输出时间戳和内容
if content_with_brackets:
    print(f"AOC在{previous_timestamp}发布了以下信息：")
    print(f"{content_with_brackets}")
