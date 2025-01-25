import pyautogui
import time
import datetime
import os
import subprocess
import re

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
def try_find_image(img_path, max_attempts=3, buffer = 100, confidence = 0.9):
    for attempt in range(max_attempts):
        try:
            print(f"尝试第 {attempt + 1} 次查找图片: {img_path}")
            location = pyautogui.locateOnScreen(img_path, confidence=confidence)
            print(f"图片位置: {location}")
            if location:
                width, height = pyautogui.size()
                initial_width, initial_height = get_physical_display_resolution()
                print(f"物理分辨率: {initial_width}x{initial_height}")
                scaling_width = initial_width / width
                scaling_height = initial_height / height
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

def maximize_window():
    time.sleep(2)

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 根据当前时间选择合适的图片
    current_hour = datetime.datetime.now().hour
    img_name = 'fillBlack.png' if (current_hour >= 18 or current_hour < 6) else 'fill.png'
    img_path = os.path.join(current_dir, img_name)
    
    print(f"当前时间: {current_hour}点")
    print(f"图片完整路径: {img_path}")

    # 尝试找到图片
    click_x, click_y = try_find_image(img_path, 3, 20)
    # 点击图片
    pyautogui.click(click_x, click_y)



if __name__ == '__main__':
    maximize_window()