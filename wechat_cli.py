import argparse
import wechat_pyautogui
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='微信自动发送消息工具')
    parser.add_argument('friend_name', help='好友名称')
    parser.add_argument('message', help='要发送的消息')
    parser.add_argument('--repeat', type=int, default=1, help='重复发送次数')
    parser.add_argument('--schedule', help='定时发送时间 (格式: HH:MM)', default=None)

    args = parser.parse_args()

    try:
        if args.schedule:
            # 解析时间
            hour, minute = map(int, args.schedule.split(':'))
            target_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if target_time < datetime.now():
                target_time = target_time.replace(day=target_time.day + 1)
            
            print(f"消息将在 {target_time.strftime('%Y-%m-%d %H:%M')} 发送")
            wechat_pyautogui.run_at_specific_time(
                target_time,
                args.friend_name,
                args.message,
                repeat=args.repeat
            )
        else:
            wechat_pyautogui.wechat_send_message(
                args.friend_name,
                args.message,
                repeat=args.repeat
            )
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main() 