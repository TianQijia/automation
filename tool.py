import subprocess
import re
import pyautogui
import time
import pyperclip


def get_physical_display_resolution():
    output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).decode("utf-8")
    for line in output.split("\n"):
        if "Resolution:" in line:
            # 用正则提取"XXXX x XXXX" 形式的分辨率
            match = re.search(r'(\d+)\s*x\s*(\d+)', line)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
                return width, height
    return None, None


def duplicate_return(duration = 1):
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.keyDown('enter')
    time.sleep(0.5)
    pyautogui.keyUp('enter')
    time.sleep(duration)  

def command_key_press(key,duration=1):
    pyautogui.keyDown('command')
    pyautogui.press(key)
    pyautogui.keyUp('command')
    time.sleep(duration)

# 添加重试机制的函数
def try_find_image(img_path, max_attempts=3, buffer = 100, confidence = 0.9, type = 1):
    for attempt in range(max_attempts):
        try:
            print(f"尝试第 {attempt + 1} 次查找图片: {img_path}")
            # 降低匹配阈值
            location = pyautogui.locateOnScreen(img_path, confidence = confidence)
            print(f"图片位置: {location}")
            if location:
                width, height = pyautogui.size()
                initial_width, initial_height = get_physical_display_resolution()
                print(f"物理分辨率: {initial_width}x{initial_height}")
                scaling_width = initial_width / width
                scaling_height = initial_height / height
                match type:
                    # wechat input box
                    case 1:
                        click_x = location.left / scaling_width + buffer
                        click_y = location.top / scaling_height + buffer
                    # fullscreen button
                    case 2:
                        l = (location.left + buffer) / scaling_width
                        r = (location.left + location.width + buffer) / scaling_width
                        t = location.top / scaling_height
                        b = (location.top + location.height) / scaling_height
                        click_x = (l + 2*r) / 3
                        click_y = (t + b) / 2
                print(f"Adjusted location: ({click_x}, {click_y})")
                return click_x, click_y
            else:
                print("图片未找到")
            time.sleep(2)
        except Exception as e:
            print(f"尝试定位图片失败 {attempt + 1}/{max_attempts}: {str(e)}")
            print(f"错误详情: {type(e).__name__}")
    raise Exception("无法找到目标图片")


# 添加打开 Spotlight 的函数
def try_open_spotlight(max_attempts=3, input_content = 'wechat'):
    for attempt in range(max_attempts):
        try:
            print(f"尝试第 {attempt + 1} 次打开 Spotlight")
            command_key_press('space', 2)
            
            # 尝试输入一个字符并删除，验证搜索框是否打开
            pyautogui.write('test')
            time.sleep(0.5)
            pyautogui.press('backspace', presses=5)
            
            # 如果搜索框打开，继续操作
            pyperclip.copy(input_content)
            command_key_press('v', 1)  # Command+V 粘贴
            duplicate_return()
            return True
        
        except Exception as e:
            print(f"Spotlight 打开失败 {attempt + 1}/{max_attempts}: {str(e)}")
            # 如果失败，按 Esc 关闭可能的搜索框
            pyautogui.press('esc')
            time.sleep(1)
    raise Exception("无法打开 Spotlight 搜索")

