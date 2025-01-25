import openai
import pyautogui
import pyperclip
import time

# 设置 OpenAI API 密钥
openai.api_key = 'your_openai_api_key'

def generate_reply(conversation_history):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=conversation_history,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def wechat_auto_reply(conversation_history):
    reply = generate_reply(conversation_history)
    pyperclip.copy(reply)
    pyautogui.hotkey('command', 'v')
    pyautogui.press('enter')
    print(f"自动回复: {reply}")

def get_conversation_history():
    # 这里需要实现获取对话历史的逻辑
    # 示例：从剪贴板获取对话历史
    pyautogui.hotkey('command', 'a')
    pyautogui.hotkey('command', 'c')
    time.sleep(0.5)
    conversation_history = pyperclip.paste()
    return conversation_history

if __name__ == '__main__':
    conversation_history = get_conversation_history()
    wechat_auto_reply(conversation_history)