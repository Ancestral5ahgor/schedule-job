import time
import pygetwindow as gw
import psutil
import pyautogui

group_name = "chenghaibo"
message = "This is a test message!!"

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def is_wechat_running():
    # 微信进程名称
    wechat_process_name = "WeChat.exe"
    
    # 获取所有正在运行的窗口
    all_windows = gw.getAllWindows()
    
    # 检查是否有微信窗口存在
    for window in all_windows:
        if window.title.startswith("微信"):
            return True
    
    # 如果没有微信窗口，则检查是否有微信进程在运行
    return is_process_running(wechat_process_name)

def restore_wechat_to_desktop():
    # 尝试获取微信窗口
    wechat_windows = gw.getWindowsWithTitle("微信")
    
    # 如果没有找到微信窗口，则不执行后续操作
    if not wechat_windows:
        print("未找到微信窗口")
        return
    
    # 获取第一个微信窗口
    wechat_window = wechat_windows[0]
    
    # 最小化微信窗口
    #wechat_window.minimize()
    
    # 恢复微信窗口
    wechat_window.restore()
    time.sleep(3)
    # 调用函数发送消息
    send_message_to_group(group_name, message)
      
    # 移动鼠标到微信窗口的标题栏
    #pyautogui.moveTo(wechat_window.left + 13500, wechat_window.top + 10, duration=0.5)
    
    # 点击标题栏
    #pyautogui.click()


def send_message_to_group(group_name, message):
   
    # 打开搜索框
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)

    # 输入群聊名称并搜索
    pyautogui.typewrite(group_name)
    time.sleep(3)

    pyautogui.press('enter')
    time.sleep(1)

    # 选中指定的群聊
    pyautogui.click(x=700, y=300)  # 假设你要选中的群聊在屏幕上的位置是 (200, 200)
    time.sleep(1)

    # 输入消息并发送
    pyautogui.typewrite(message)
    time.sleep(1)
    pyautogui.press('enter')

if __name__ == "__main__":
    while True:
        if is_wechat_running():
            print("微信正在运行")
            restore_wechat_to_desktop()
                     
        else:
            print("微信未运行")
        time.sleep(5)  # 每5秒检测一次
