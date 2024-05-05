import time
import pygetwindow as gw
import psutil
import pyautogui
import pyperclip
import re

group_name = "shenzhenjichang"

# 假设的聊天窗口坐标
TEXT_BOX_START_X = 1632
TEXT_BOX_START_Y = 1018
SCROLL_AMOUNT = 20  # 每次滚动的像素量
SCROLL_INCREMENT = 10  # 每次增加滚动的像素量
MAX_SCROLL = 1000  # 最大的滚动量

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def is_wechat_running():
    #深圳空港进程名称
    wechat_process_name = "szairport_wxwork.exe"
    
    # 获取所有正在运行的窗口
    all_windows = gw.getAllWindows()
    
    # 检查是否有深圳空港窗口存在
    for window in all_windows:
        if window.title.startswith("深圳空港"):
            return True
    
    # 如果没有深圳空港窗口，则检查是否有深圳空港进程在运行
    return is_process_running(wechat_process_name)

def restore_wechat_to_desktop():
    # 尝试获取深圳空港窗口
    wechat_windows = gw.getWindowsWithTitle("深圳空港")
    
    # 如果没有找到深圳空港窗口，则不执行后续操作
    if not wechat_windows:
        print("未找到深圳空港窗口")
        return
    
    # 获取第一个深圳空港窗口
    wechat_window = wechat_windows[0]
       
    # 恢复深圳空港窗口
    wechat_window.restore()
    time.sleep(3)
    # 调用函数尝试复制消息
    copy_chat_from_group(group_name)


    # 最小化深圳空港窗口
    wechat_window.minimize()
      
    # 移动鼠标到深圳空港窗口的标题栏
    #pyautogui.moveTo(wechat_window.left + 13500, wechat_window.top + 10, duration=0.5)
    
    # 点击标题栏
    #pyautogui.click()

def copy_chat_from_group(group_name):

    # 打开搜索框
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)

    # 输入群聊名称并搜索
    pyautogui.typewrite(group_name)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(1)

    # 选中指定的群聊
    pyautogui.click(x=200, y=90)  # 假设你要选中的群聊在屏幕上的位置是 (200, 200)
    time.sleep(1)

    # 选中群聊中打开消息记录
    pyautogui.click(x=1750, y=765)  # 假设你要选中的群聊在屏幕上的位置是 (200, 200)
    time.sleep(1)

    # 移动到起始位置并按下鼠标左键
    pyautogui.moveTo(TEXT_BOX_START_X, TEXT_BOX_START_Y)
    pyautogui.mouseDown(button='left')

    # 拖拽操作选中一部分文本
    pyautogui.moveTo(TEXT_BOX_START_X - 35, TEXT_BOX_START_Y - 65)

    # 释放鼠标左键
    #pyautogui.mouseUp(button='left')

    # 开始向上滚动
    current_scroll = 0
    while current_scroll < MAX_SCROLL:
        # 向上滚动
        pyautogui.scroll(SCROLL_AMOUNT)
        current_scroll += SCROLL_AMOUNT
    
        # 可能需要一些延迟来确保滚动被正确处理
        #time.sleep(0.5)

    # 完成后，确保释放所有鼠标按钮
    pyautogui.mouseUp(button='left')

    # 选择消息记录然后右单机复制
    #pyautogui.mouseDown(x=1595, y=1018)  # 假设你要选中的群聊在屏幕上的位置是 (200, 200)

    # 复制选中的内容
    pyautogui.hotkey('ctrl', 'c')

    # 等待一段时间以确保内容已经复制到剪贴板
    time.sleep(0.5)

    # 从剪贴板获取文本
    text_from_clipboard = pyperclip.paste()

    # 将内容写入到文件中
    file_path = 'F:/BaiduNetdiskDownload/schedule/a.txt'  # 输出的文件路径
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_from_clipboard)

    # 输出完成信息
    print(f"内容已写入到 {file_path}")

    # 复制完毕后关闭消息记录
    pyautogui.click(x=1523, y=775) 
    time.sleep(3) 


def extract():
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



if __name__ == "__main__":
    while True:
        if is_wechat_running():
            print("深圳空港正在运行")
            restore_wechat_to_desktop()
            extract()
                     
        else:
            print("深圳空港未运行")
        time.sleep(30)  # 每5秒检测一次
