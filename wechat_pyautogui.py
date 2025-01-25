import pyautogui
import time
import datetime
import os
import pyperclip
from tool import duplicate_return, command_key_press, try_find_image, try_open_spotlight




def wechat_send_message(friend_name, message, repeat=1):
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 根据当前时间选择合适的图片
    current_hour = datetime.datetime.now().hour
    img_name = 'wechatBlack.png' if (current_hour >= 18 or current_hour < 6) else 'wechat.png'
    img_path = os.path.join(current_dir, img_name)
    
    print(f"当前时间: {current_hour}点")
    print(f"图片完整路径: {img_path}")
    
    # 检查文件是否存在
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"找不到图片文件: {img_path}")
    
    try:
        # 使用新的打开微信函数
        try_open_spotlight()

        # 搜索好友
        command_key_press('f', 1.5)
        pyperclip.copy(friend_name)
        command_key_press('v', 1)  # Command+V 粘贴
        time.sleep(1.5)
        duplicate_return(2)
        print('正在查找好友...')

        # 定位对话框
        # 使用重试机制查找图片
        click_x, click_y = try_find_image(img_path)
        
        # 发送消息
        for i in range(repeat):
            try:
                pyautogui.moveTo(click_x, click_y, duration=0.5)  # 添加移动动画
                time.sleep(1)
                pyautogui.click()
                time.sleep(1.5)
                
                # 使用剪贴板来处理中文
                pyperclip.copy(message)
                command_key_press('v', 1)  # Command+V 粘贴
                
                time.sleep(1.5)
                # 发送消息
                duplicate_return(2)
                
                time.sleep(1.5)
                print(f'消息发送成功 ({i+1}/{repeat})')
            
            except Exception as e:
                print(f"发送消息失败: {str(e)}")
                continue

        # 关闭微信
        time.sleep(1)
        command_key_press('w', 1)
        print('微信已关闭')

    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        # 可以在这里添加重试逻辑


def run_at_specific_time(specific_time, friend_name, message, repeat = 1):
    now = datetime.datetime.now()
    while now < specific_time:
        now = datetime.datetime.now()
        time.sleep(20)  # 每20秒检查一次
    
    print(now)
    # same hour and minute
    if now.hour == specific_time.hour and now.minute == specific_time.minute:
        wechat_send_message(friend_name, message, repeat)

        


# example usage
if __name__ == '__main__':
    w = 3840
    h = 2160
    # tommorow 06:00
    tmr06 = datetime.datetime.now().replace(hour=6, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    # today 23:00
    today23 = datetime.datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
    # today 09:00
    today09 = datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    #run_at_specific_time(today09, 'HKUNY', 'Good Morning! It is 09:00! A wonderful day begin', buffer=100, logical_width=w, logical_height=h, repeat = 3, img_path = 'wechat.png')
    wechat_send_message('HKUNY', 'Oh no, Shan I can\'t publish the album.', repeat = 3)
    print('Finish!')
