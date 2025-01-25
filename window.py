import pyautogui
import time
import datetime
import os
import subprocess
import re
from tools import try_find_image

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
    click_x, click_y = try_find_image(img_path, max_attempts=3, buffer = 20, type = 2)

    # 点击图片
    pyautogui.click(click_x, click_y)


## 测试代码
if __name__ == '__main__':
    maximize_window()