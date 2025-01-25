import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import wechat_pyautogui
from datetime import datetime
import threading

class WeChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("微信自动发送工具")
        
        # 创建输入框和标签
        ttk.Label(root, text="好友名称:").grid(row=0, column=0, padx=5, pady=5)
        self.friend_name = ttk.Entry(root)
        self.friend_name.grid(row=0, column=1, padx=5, pady=5)
        
        # 添加常用好友名称选项
        self.common_friends = ttk.Combobox(root, values=["Shan", "Feng", "HKUNY"])
        self.common_friends.grid(row=0, column=2, padx=5, pady=5)
        self.common_friends.bind("<<ComboboxSelected>>", self.select_common_friend)
        
        ttk.Label(root, text="发送内容:").grid(row=1, column=0, padx=5, pady=5)
        self.message = ttk.Entry(root)
        self.message.grid(row=1, column=1, padx=5, pady=5)
        
        # 添加常用消息内容选项
        self.common_messages = ttk.Combobox(root, values=["早上好！", "晚上好！", "你们在干嘛？"])
        self.common_messages.grid(row=1, column=2, padx=5, pady=5)
        self.common_messages.bind("<<ComboboxSelected>>", self.select_common_message)
        
        ttk.Label(root, text="重复次数:").grid(row=2, column=0, padx=5, pady=5)
        self.repeat = ttk.Entry(root)
        self.repeat.insert(0, "1")
        self.repeat.grid(row=2, column=1, padx=5, pady=5)
        
        # 添加定时发送选项
        self.schedule_var = tk.BooleanVar()
        self.schedule_check = ttk.Checkbutton(root, text="定时发送", variable=self.schedule_var, 
                                            command=self.toggle_schedule)
        self.schedule_check.grid(row=3, column=0, columnspan=2, pady=5)
        
        # 时间选择框架
        self.time_frame = ttk.Frame(root)
        self.time_frame.grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Label(self.time_frame, text="发送时间:").grid(row=0, column=0, padx=5, pady=5)
        self.send_time = ttk.Entry(self.time_frame)
        self.send_time.grid(row=0, column=1, padx=5, pady=5)
        self.send_time.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # 添加“自动发送”选项
        self.auto_send_var = tk.BooleanVar()
        self.auto_send_check = ttk.Checkbutton(root, text="在消息末尾添加“（自动发送）”", variable=self.auto_send_var)
        self.auto_send_check.grid(row=5, column=0, columnspan=2, pady=5)
        
        # 发送按钮
        self.send_button = ttk.Button(root, text="发送", command=self.send_message)
        self.send_button.grid(row=6, column=0, columnspan=2, pady=5)
        
    def select_common_friend(self, event):
        self.friend_name.delete(0, tk.END)
        self.friend_name.insert(0, self.common_friends.get())
        
    def select_common_message(self, event):
        self.message.delete(0, tk.END)
        self.message.insert(0, self.common_messages.get())
        
    def toggle_schedule(self):
        if self.schedule_var.get():
            self.time_frame.grid()
        else:
            self.time_frame.grid_remove()
        
    def send_message(self):
        friend_name = self.friend_name.get()
        message = self.message.get()
        repeat = int(self.repeat.get())
        if self.auto_send_var.get():
            message += "（自动发送）"
        if self.schedule_var.get():
            send_time = datetime.strptime(self.send_time.get(), "%Y-%m-%d %H:%M:%S")
            threading.Thread(target=wechat_pyautogui.run_at_specific_time, args=(send_time, friend_name, message, repeat)).start()
        else:
            threading.Thread(target=wechat_pyautogui.wechat_send_message, args=(friend_name, message, repeat)).start()
            messagebox.showinfo("提示", "消息预约发送成功！")

if __name__ == '__main__':
    root = tk.Tk()
    app = WeChatGUI(root)
    root.mainloop()